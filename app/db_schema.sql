/* This file contains the schema for an sqlite3 database */
DROP TABLE IF EXISTS plant;
DROP TABLE IF EXISTS moisture_reading;

CREATE TABLE plant (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    common_name TEXT NOT NULL,
    species TEXT NOT NULL,
    moisture_max INTEGER NOT NULL,
    moisture_min INTEGER NOT NULL,
    moisture_ideal INTEGER NOT NULL
);

CREATE TABLE moisture_reading (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plant_id INTEGER NOT NULL,
    reading INTEGER NOT NULL,
    recorded_at TIMESTAMP NOT NULL,
    FOREIGN KEY (plant_id) REFERENCES plant(id)
);

INSERT INTO plant (name, common_name, species, moisture_max, moisture_min, moisture_ideal)
VALUES ('Fred', 'Chinese Money Plant', 'Pilea peperomioides', 7, 4, 6);



