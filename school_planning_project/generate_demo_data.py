import json
import random
from pathlib import Path

import pandas as pd
from shapely.geometry import Polygon

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
random.seed(42)


def rect(lon1, lat1, lon2, lat2):
    return [
        [lon1, lat1],
        [lon2, lat1],
        [lon2, lat2],
        [lon1, lat2],
        [lon1, lat1],
    ]


def save_geojson(features, path):
    collection = {"type": "FeatureCollection", "features": features}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(collection, f, indent=2)


def build_planning_units():
    units = [
        {
            "planning_unit_id": "PU-101",
            "name": "Northwest Growth Area",
            "expected_growth_pct": 7.5,
            "coordinates": rect(-78.98, 36.02, -78.95, 36.05),
        },
        {
            "planning_unit_id": "PU-102",
            "name": "Southwest Stable Area",
            "expected_growth_pct": 2.1,
            "coordinates": rect(-78.98, 35.99, -78.95, 36.02),
        },
        {
            "planning_unit_id": "PU-201",
            "name": "Northeast Redevelopment Area",
            "expected_growth_pct": 9.3,
            "coordinates": rect(-78.95, 36.02, -78.92, 36.05),
        },
        {
            "planning_unit_id": "PU-202",
            "name": "Southeast Stable Area",
            "expected_growth_pct": 3.0,
            "coordinates": rect(-78.95, 35.99, -78.92, 36.02),
        },
    ]
    features = []
    for u in units:
        features.append(
            {
                "type": "Feature",
                "properties": {
                    "planning_unit_id": u["planning_unit_id"],
                    "name": u["name"],
                    "expected_growth_pct": u["expected_growth_pct"],
                },
                "geometry": {"type": "Polygon", "coordinates": [u["coordinates"]]},
            }
        )
    save_geojson(features, DATA_DIR / "planning_units.geojson")


def build_attendance_boundaries():
    boundaries = [
        {
            "boundary_id": "B-1",
            "school_id": "SCH-01",
            "school_name": "Riverdale Elementary",
            "coordinates": rect(-78.98, 35.99, -78.95, 36.05),
        },
        {
            "boundary_id": "B-2",
            "school_id": "SCH-02",
            "school_name": "Oakridge Elementary",
            "coordinates": rect(-78.95, 35.99, -78.92, 36.05),
        },
    ]
    features = []
    for b in boundaries:
        features.append(
            {
                "type": "Feature",
                "properties": {
                    "boundary_id": b["boundary_id"],
                    "school_id": b["school_id"],
                    "school_name": b["school_name"],
                },
                "geometry": {"type": "Polygon", "coordinates": [b["coordinates"]]},
            }
        )
    save_geojson(features, DATA_DIR / "attendance_boundaries.geojson")


def build_schools():
    schools = pd.DataFrame(
        [
            {
                "school_id": "SCH-01",
                "school_name": "Riverdale Elementary",
                "grade_span": "K-5",
                "capacity": 185,
                "principal": "A. Brooks",
                "lon": -78.965,
                "lat": 36.015,
            },
            {
                "school_id": "SCH-02",
                "school_name": "Oakridge Elementary",
                "grade_span": "K-5",
                "capacity": 170,
                "principal": "L. Carter",
                "lon": -78.935,
                "lat": 36.035,
            },
        ]
    )
    schools.to_csv(DATA_DIR / "schools.csv", index=False)


def build_parcels_and_students():
    planning_units = [
        ("PU-101", -78.979, -78.951, 36.021, 36.049, 32),
        ("PU-102", -78.979, -78.951, 35.991, 36.019, 22),
        ("PU-201", -78.949, -78.921, 36.021, 36.049, 40),
        ("PU-202", -78.949, -78.921, 35.991, 36.019, 18),
    ]

    parcels = []
    students = []
    parcel_counter = 1
    student_counter = 1
    grades = ["K", "1", "2", "3", "4", "5"]

    for unit_id, min_lon, max_lon, min_lat, max_lat, homes in planning_units:
        for _ in range(homes):
            lon = round(random.uniform(min_lon, max_lon), 6)
            lat = round(random.uniform(min_lat, max_lat), 6)
            parcel_id = f"PAR-{parcel_counter:03d}"
            house_no = random.randint(100, 999)
            street = random.choice(
                [
                    "Maple St",
                    "Pine Ave",
                    "Cedar Dr",
                    "Elm Rd",
                    "Willow Ln",
                    "Oak St",
                ]
            )
            parcels.append(
                {
                    "parcel_id": parcel_id,
                    "planning_unit_hint": unit_id,
                    "address": f"{house_no} {street}",
                    "lon": lon,
                    "lat": lat,
                }
            )

            student_count = random.choices([1, 2, 3], weights=[0.55, 0.35, 0.10])[0]
            for _ in range(student_count):
                students.append(
                    {
                        "student_id": f"STU-{student_counter:04d}",
                        "parcel_id": parcel_id,
                        "student_name": random.choice(
                            [
                                "Ava",
                                "Liam",
                                "Noah",
                                "Mia",
                                "Sophia",
                                "Lucas",
                                "Emma",
                                "Ethan",
                                "Mason",
                                "Isla",
                            ]
                        )
                        + " "
                        + random.choice(
                            [
                                "Johnson",
                                "Smith",
                                "Brown",
                                "Wilson",
                                "Davis",
                                "Thomas",
                                "Lee",
                            ]
                        ),
                        "grade": random.choice(grades),
                        "lon": lon,
                        "lat": lat,
                    }
                )
                student_counter += 1
            parcel_counter += 1

    pd.DataFrame(parcels).to_csv(DATA_DIR / "parcels.csv", index=False)
    pd.DataFrame(students).to_csv(DATA_DIR / "students.csv", index=False)


if __name__ == "__main__":
    DATA_DIR.mkdir(exist_ok=True)
    build_planning_units()
    build_attendance_boundaries()
    build_schools()
    build_parcels_and_students()
    print("Demo GIS and student data created in the data/ folder.")
