# !/bin/bash
airflow scheduler &

# Start the Airflow webserver
airflow webserver