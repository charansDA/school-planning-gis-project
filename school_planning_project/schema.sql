CREATE TABLE schools (
    school_id VARCHAR(20) PRIMARY KEY,
    school_name VARCHAR(100),
    grade_span VARCHAR(20),
    capacity INT,
    principal VARCHAR(100),
    lon NUMERIC,
    lat NUMERIC
);

CREATE TABLE parcels (
    parcel_id VARCHAR(20) PRIMARY KEY,
    planning_unit_hint VARCHAR(20),
    address VARCHAR(150),
    lon NUMERIC,
    lat NUMERIC
);

CREATE TABLE students (
    student_id VARCHAR(20) PRIMARY KEY,
    parcel_id VARCHAR(20),
    student_name VARCHAR(100),
    grade VARCHAR(5),
    lon NUMERIC,
    lat NUMERIC,
    FOREIGN KEY (parcel_id) REFERENCES parcels(parcel_id)
);

-- Useful interview query:
SELECT school_name, COUNT(*) AS student_count
FROM student_assignments
GROUP BY school_name
ORDER BY student_count DESC;
