# School Planning GIS Project

## Overview
This project simulates a school district planning workflow for assigning students to school attendance boundaries and analyzing enrollment patterns.

## Features
- Student geocoding (simulated)
- Spatial join of students to school boundaries and planning units
- Enrollment analysis by school and planning unit
- Grade-level distribution analysis
- Interactive map visualization

## Tools Used
- Python
- Pandas
- GeoPandas
- Folium

## Outputs
- Enrollment by school
- Enrollment by planning unit
- Grade mix by school
- Student assignment dataset
- Planning memo
- Interactive HTML map

## How to Run
1. Install dependencies:
   pip install -r requirements.txt

2. Generate demo data:
   python generate_demo_data.py

3. Run pipeline:
   python run_pipeline.py
