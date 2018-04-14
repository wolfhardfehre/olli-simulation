#!/bin/sh -e

# simple script to load vehicle states into a postgresql database. Put
# vehicle states in resources then execute from root

createdb open_olli
psql open_olli <<EOF
CREATE TABLE vehicle_states (id integer PRIMARY KEY, vehicle_id text, latitude numeric, longitude numeric, theta numeric, speed numeric, battery numeric, doors boolean, last_seen Timestamp, created_at Timestamp);
EOF

psql open_olli -c "copy vehicle_states from STDIN WITH CSV HEADER DELIMITER ';'" < resources/vehicle_states.csv;

psql open_olli <<EOF
ALTER TABLE vehicle_states ADD COLUMN geometry Geography;
ALTER TABLE vehicle_states ADD COLUMN seen_on Date;
CREATE EXTENSION postgis;
UPDATE vehicle_states SET geometry = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326);
UPDATE vehicle_states SET seen_on = last_seen::Date;
CREATE INDEX ON vehicle_states (last_seen);
CREATE INDEX ON vehicle_states (seen_on);
EOF
