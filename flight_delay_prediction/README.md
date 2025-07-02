### 1. ETL Pipeline for Flight Data
- **Description:**  
This project builds a simple ETL pipeline that extracts flight data from an API, transforms it by cleaning and selecting relevant features, and loads it into a PostgreSQL database.
Flight delays are a critical issue in airline operations, causing increased costs and passenger dissatisfaction. The goal of this project is to build a predictive model based on random forests that can estimate flight delay flags earlier, helping airlines to reduce losses and improve operational efficiency.
Project is still a work in progress and requires further development, but it demonstrates understanding of key foundational concepts in data engineering and pipeline orchestration.
- **Technologies:**  
  - Apache Airflow (for orchestration)  
  - Docker (for containerization)  
  - Python (for data extraction and transformation)  
  - PostgreSQL (as data warehouse)
  - SQL (for building tables)
- **Key Skills Demonstrated:**  
  - Data ingestion from APIs  
  - Building data pipelines with Airflow  
  - Containerization using Docker  
  - SQL and database management 


This guide will help you set up and run the project locally using **Docker** and **Apache Airflow**.

---

### 1. Prerequisites

- Make sure **Docker** is installed and running on your machine.  
  If you don’t have it yet, download and install it from:  
  https://docs.docker.com/get-docker/  
- Start Docker before proceeding.

---

### 2. Start PostgreSQL and Redis Services

Run the following command to launch the database services:

docker-compose up -d postgres redis

---

### 3. Initialize the Airflow Database

Initialize Airflow’s metadata database by running:

docker-compose run --rm airflow-webserver airflow db init

---

### 4. Start All Services

Start Airflow webserver, scheduler, worker, plus postgres and redis:

docker-compose up -d

> Wait about **30 seconds** for all services to fully start.

---

### 5. Access Airflow UI

Open your browser and navigate to:  
http://localhost:8080

---

### 6. Create an Admin User

Run the following command to create an admin user for Airflow:

docker-compose run --rm airflow-webserver airflow users create \  
  --username admin \  
  --firstname Admin \  
  --lastname User \  
  --role Admin \  
  --email admin@example.com \  
  --password admin

You can now log in to the UI at http://localhost:8080 using:  
**Username:** admin  
**Password:** admin

---

### 7. Configure Airflow Connections

1. In the Airflow UI, go to **Admin → Connections**.  
2. Click the **➕** button to add a new connection.  
3. Fill in the form with the following details:  
   - **Conn Id:** postgres_default  
   - **Conn Type:** Postgres  
   - **Host:** postgres  
   - **Schema:** airflow  
   - **Login:** airflow  
   - **Password:** airflow  
   - **Port:** 5432  
4. Save the connection.

---

### 8. Run the Data Pipeline

Locate the DAG named **flight_data_pipeline** in the Airflow UI and trigger it to start the pipeline.
