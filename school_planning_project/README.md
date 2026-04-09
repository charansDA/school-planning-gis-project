# School Planning GIS Project

## Project Goal
This project simulates how a school district can use GIS and Python to support enrollment planning, attendance boundary analysis, and reporting.

## Overview
This project assigns student locations to school attendance boundaries and planning units, then summarizes enrollment patterns.

## How It Works
1. Generate demo student and school boundary data
2. Assign student points to school zones
3. Summarize enrollment by school and planning unit
4. Export outputs like CSV files, memo, and interactive map

## Tools Used
- Python
- Pandas
- GeoPandas
- Folium

## Outputs
- enrollment_by_school.csv
- enrollment_by_planning_unit.csv
- grade_mix_by_school.csv
- student_assignments.csv
- planning_memo.txt
- interactive_school_planning_map.html

## Business Value
This workflow helps school planners understand student distribution, enrollment patterns, and planning needs.

## How to Run
```bash
pip install -r requirements.txt
python generate_demo_data.py
python run_pipeline.pyby the Python pipeline.
