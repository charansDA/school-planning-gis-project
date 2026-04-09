# School Attendance Planning and Enrollment Pressure Project

## Why this project fits the GIS & Data Analyst role
This project mirrors a school-planning workflow:
- builds and maintains planning-unit and attendance-boundary spatial data
- processes student locations and assigns them to school zones
- summarizes enrollment by school and planning unit
- generates planning outputs: CSV tables, a memo, and an interactive map
- demonstrates Python, GIS logic, data management, and reporting

## Project idea
A fictional district wants to understand which elementary school attendance boundary is under the most enrollment pressure and which planning unit is likely to grow fastest.

The project creates a reproducible workflow that:
1. generates demo district data
2. geocodes student records using synthetic coordinates
3. assigns students to planning units and school attendance boundaries
4. compares enrollment against school capacity
5. exports tables, a memo, and an HTML map for leadership review

## Tools used
- Python
- pandas
- shapely
- folium
- SQL schema example
- optional: QGIS to inspect the GeoJSON layers visually

## Folder structure
```text
school_planning_project/
│
├── data/
│   ├── attendance_boundaries.geojson
│   ├── planning_units.geojson
│   ├── parcels.csv
│   ├── schools.csv
│   └── students.csv
│
├── output/
│   ├── enrollment_by_planning_unit.csv
│   ├── enrollment_by_school.csv
│   ├── grade_mix_by_school.csv
│   ├── interactive_school_planning_map.html
│   ├── parcel_inventory.csv
│   ├── planning_memo.txt
│   └── student_assignments.csv
│
├── generate_demo_data.py
├── run_pipeline.py
├── requirements.txt
└── schema.sql
```

## How to run
### 1. Create a virtual environment
Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

Mac/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install packages
```bash
pip install -r requirements.txt
```

### 3. Generate demo data
```bash
python generate_demo_data.py
```

### 4. Run the planning pipeline
```bash
python run_pipeline.py
```

### 5. Open the outputs
- open `output/interactive_school_planning_map.html` in your browser
- review `output/enrollment_by_school.csv`
- read `output/planning_memo.txt`

## What to say in an interview
“I built a school planning prototype that simulates a district workflow. I created planning-unit and attendance-boundary layers, generated student point data, assigned each student to a school zone using spatial logic, compared enrollment to capacity, and exported planning-ready outputs including a memo, summary tables, and an interactive map. The same workflow could be connected to real district data from SQL or GIS systems.”

## Beginner explanation of the workflow
- `generate_demo_data.py` creates fake but realistic district data so the project runs without private district files.
- `run_pipeline.py` reads the data and checks which polygon each student point falls into.
- That is the core GIS idea: point-in-polygon matching.
- After that, the script counts how many students belong to each school.
- Then it compares those counts to school capacity.
- Finally, it writes outputs that a planner or district leader can review.

## Optional QGIS step
If you install QGIS, drag these files into QGIS:
- `data/planning_units.geojson`
- `data/attendance_boundaries.geojson`
- `data/students.csv` as a delimited text layer using lon/lat
- `data/schools.csv` as a delimited text layer using lon/lat

That lets you visually inspect the same layers used by the Python pipeline.
