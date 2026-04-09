import json
from pathlib import Path

import folium
import pandas as pd
from shapely.geometry import Point, shape

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"


def load_geojson(path):
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    records = []
    for feature in raw["features"]:
        rec = feature["properties"].copy()
        rec["geometry"] = shape(feature["geometry"])
        records.append(rec)
    return records, raw


def assign_polygon(point, records, key_fields):
    for rec in records:
        if point.within(rec["geometry"]) or point.touches(rec["geometry"]):
            return {k: rec[k] for k in key_fields}
    return {k: None for k in key_fields}


def utilization_status(utilization):
    if utilization >= 100:
        return "Over capacity"
    if utilization >= 90:
        return "Near capacity"
    return "Healthy"


def color_for_status(status):
    return {
        "Over capacity": "#d73027",
        "Near capacity": "#fdae61",
        "Healthy": "#1a9850",
    }.get(status, "#4575b4")


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    planning_units, planning_units_geojson = load_geojson(DATA_DIR / "planning_units.geojson")
    boundaries, boundaries_geojson = load_geojson(DATA_DIR / "attendance_boundaries.geojson")
    schools = pd.read_csv(DATA_DIR / "schools.csv")
    students = pd.read_csv(DATA_DIR / "students.csv")
    parcels = pd.read_csv(DATA_DIR / "parcels.csv")

    students["geometry"] = students.apply(lambda r: Point(r["lon"], r["lat"]), axis=1)

    unit_assignments = students["geometry"].apply(
        lambda pt: assign_polygon(pt, planning_units, ["planning_unit_id", "name", "expected_growth_pct"])
    )
    boundary_assignments = students["geometry"].apply(
        lambda pt: assign_polygon(pt, boundaries, ["boundary_id", "school_id", "school_name"])
    )

    students = pd.concat([students, pd.DataFrame(unit_assignments.tolist()), pd.DataFrame(boundary_assignments.tolist())], axis=1)

    enrollment_by_school = (
        students.groupby(["school_id", "school_name"]).size().reset_index(name="student_count")
        .merge(schools[["school_id", "capacity", "principal"]], on="school_id", how="left")
    )
    enrollment_by_school["utilization_pct"] = round(
        enrollment_by_school["student_count"] / enrollment_by_school["capacity"] * 100, 1
    )
    enrollment_by_school["status"] = enrollment_by_school["utilization_pct"].apply(utilization_status)
    enrollment_by_school = enrollment_by_school.sort_values("utilization_pct", ascending=False)
    enrollment_by_school.to_csv(OUTPUT_DIR / "enrollment_by_school.csv", index=False)

    enrollment_by_unit = (
        students.groupby(["planning_unit_id", "name", "expected_growth_pct", "school_name"])
        .size()
        .reset_index(name="student_count")
        .sort_values(["expected_growth_pct", "student_count"], ascending=[False, False])
    )
    enrollment_by_unit.to_csv(OUTPUT_DIR / "enrollment_by_planning_unit.csv", index=False)

    grade_mix = (
        students.groupby(["school_name", "grade"]).size().reset_index(name="student_count")
        .sort_values(["school_name", "grade"])
    )
    grade_mix.to_csv(OUTPUT_DIR / "grade_mix_by_school.csv", index=False)

    parcels.to_csv(OUTPUT_DIR / "parcel_inventory.csv", index=False)
    students.drop(columns=["geometry"]).to_csv(OUTPUT_DIR / "student_assignments.csv", index=False)

    memo_lines = []
    top_school = enrollment_by_school.iloc[0]
    top_growth_unit = enrollment_by_unit.iloc[0]
    memo_lines.append("School Planning Analysis Memo")
    memo_lines.append("=" * 32)
    memo_lines.append("")
    memo_lines.append("Project summary:")
    memo_lines.append(
        "This prototype geocodes student points, assigns them to planning units and school attendance boundaries, "
        "and summarizes enrollment pressure for district planning."
    )
    memo_lines.append("")
    memo_lines.append("Key findings:")
    memo_lines.append(
        f"1. {top_school['school_name']} has {int(top_school['student_count'])} students against a capacity of {int(top_school['capacity'])} "
        f"({top_school['utilization_pct']}% utilization), making it the highest-pressure campus."
    )
    memo_lines.append(
        f"2. {top_growth_unit['name']} is the strongest growth area with an expected growth rate of {top_growth_unit['expected_growth_pct']}% "
        f"and currently feeds {top_growth_unit['school_name']}."
    )
    memo_lines.append(
        "3. This workflow creates reusable outputs for planning memos, dashboard tables, and school locator maintenance."
    )
    memo_lines.append("")
    memo_lines.append("Recommended next steps:")
    memo_lines.append("- Validate addresses before geocoding to reduce assignment errors.")
    memo_lines.append("- Monitor redevelopment-heavy planning units each semester.")
    memo_lines.append("- Review whether attendance boundary adjustments or capacity changes are needed.")

    (OUTPUT_DIR / "planning_memo.txt").write_text("\n".join(memo_lines), encoding="utf-8")

    school_status_lookup = enrollment_by_school.set_index("school_id").to_dict("index")
    for feature in boundaries_geojson["features"]:
        school_id = feature["properties"]["school_id"]
        row = school_status_lookup[school_id]
        feature["properties"]["utilization_pct"] = row["utilization_pct"]
        feature["properties"]["status"] = row["status"]
        feature["properties"]["student_count"] = int(row["student_count"])
        feature["properties"]["capacity"] = int(row["capacity"])

    m = folium.Map(location=[36.025, -78.95], zoom_start=13, tiles="cartodbpositron")

    folium.GeoJson(
        boundaries_geojson,
        style_function=lambda feat: {
            "fillColor": color_for_status(feat["properties"]["status"]),
            "color": "black",
            "weight": 2,
            "fillOpacity": 0.45,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["school_name", "student_count", "capacity", "utilization_pct", "status"],
            aliases=["School", "Students", "Capacity", "Utilization %", "Status"],
        ),
        name="Attendance boundaries",
    ).add_to(m)

    for _, school in schools.iterrows():
        school_stats = school_status_lookup[school["school_id"]]
        popup = (
            f"<b>{school['school_name']}</b><br>Capacity: {int(school['capacity'])}<br>"
            f"Students: {int(school_stats['student_count'])}<br>"
            f"Utilization: {school_stats['utilization_pct']}%<br>"
            f"Status: {school_stats['status']}"
        )
        folium.Marker(
            location=[school["lat"], school["lon"]],
            popup=popup,
            tooltip=school["school_name"],
        ).add_to(m)

    sample_students = students.head(80)
    for _, row in sample_students.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=2,
            fill=True,
            fill_opacity=0.6,
            popup=f"{row['student_id']} | Grade {row['grade']} | {row['school_name']}",
        ).add_to(m)

    folium.LayerControl().add_to(m)
    m.save(str(OUTPUT_DIR / "interactive_school_planning_map.html"))

    print("Pipeline complete. Check the output/ folder for CSVs, memo, and map.")


if __name__ == "__main__":
    main()
