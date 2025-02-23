#!/bin/bash
airflow scheduler &

# Step 4: Start the Airflow webserver
airflow webserver