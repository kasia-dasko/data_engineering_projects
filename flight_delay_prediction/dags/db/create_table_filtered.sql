CREATE TABLE IF NOT EXISTS flights_filtered (
    flight_date DATE,
    airline_name VARCHAR(100),
    dep_iata VARCHAR(10),
    min_delay_dep INTEGER,
    is_delayed INTEGER
);