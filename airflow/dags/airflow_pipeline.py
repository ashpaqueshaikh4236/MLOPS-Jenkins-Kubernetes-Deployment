from airflow import DAG
from airflow.operators.python import PythonOperator
import logging
from usvisa.pipeline.training_pipeline import TrainPipeline
from datetime import datetime
today = datetime.today()

training_pipeline = TrainPipeline()

# Task 1: Data Ingestion
def data_ingestion(**kwargs):
    ti = kwargs['ti']
    try:
        data_ingestion_artifact, data_value = training_pipeline.start_data_ingestion()
        ti.xcom_push("data_ingestion_artifact", data_ingestion_artifact)
        ti.xcom_push("data_value", data_value)
    except Exception as e:
        logging.error(f"Error during data ingestion: {str(e)}")
        raise e

# Task 2: Data validation and Data Drift Checking
def data_validation_and_data_drift_checking(**kwargs):
    ti = kwargs['ti']
    try:
        data_value = ti.xcom_pull(task_ids="data_ingestion", key="data_value")
        if not data_value:
            logging.info("No data change detected. Skipping all subsequent tasks.")
            return
        
        data_ingestion_artifact = ti.xcom_pull(task_ids="data_ingestion", key="data_ingestion_artifact")
        data_validation_artifact, drift_status = training_pipeline.start_data_validation(data_ingestion_artifact)
        ti.xcom_push("data_validation_artifact", data_validation_artifact)
        ti.xcom_push("drift_status", drift_status)
    except Exception as e:
        logging.error(f"Error during data validation: {str(e)}")
        raise e

# Task 3: Model Drift Checking & Data Transformation and Model Training
def model_drift_checking_data_transformation_and_model_training(**kwargs):
    ti = kwargs['ti']
    try:
        #drift_status = ti.xcom_pull(task_ids="data_validation_and_data_drift_checking", key="drift_status")
        data_value = ti.xcom_pull(task_ids="data_ingestion", key="data_value")
        if not data_value:
            logging.info("No data change detected. Skipping all subsequent tasks.")
            return 
        drift_status=True
        data_ingestion_artifact = ti.xcom_pull(task_ids="data_ingestion", key="data_ingestion_artifact")
        data_validation_artifact = ti.xcom_pull(task_ids="data_validation_and_data_drift_checking", key="data_validation_artifact")

        if drift_status:
            logging.info("Drift detected! Performing data transformation and model training...")
            data_transformation_artifact = training_pipeline.start_data_transformation(data_ingestion_artifact, data_validation_artifact)
            model_trainer_artifact = training_pipeline.start_model_trainer(data_transformation_artifact)
            ti.xcom_push("model_trainer_artifact", model_trainer_artifact)
            ti.xcom_push("data_transformation_artifact", data_transformation_artifact)
        else:
            logging.info("No drift detected, validating model performance on new data...")
            model_validate_artifact = training_pipeline.start_model_validate(data_ingestion_artifact=data_ingestion_artifact, model_trainer_artifact=None)
            ti.xcom_push("model_validate_artifact", model_validate_artifact)

            if model_validate_artifact is None or not model_validate_artifact.is_model_accepted:
                logging.info("Model performance degraded or no valid model found! Retraining required...")
                data_transformation_artifact = training_pipeline.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact, data_validation_artifact=data_validation_artifact)
                model_trainer_artifact = training_pipeline.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
                ti.xcom_push("model_trainer_artifact", model_trainer_artifact)
            else:
                logging.info("Model is performing well, skipping pipeline.")
    except Exception as e:
        logging.error(f"Error during data transformation and model training: {str(e)}")
        raise e

# Task 4: Model Validation
def model_validation(**kwargs):
    ti = kwargs['ti']
    try:

        data_value = ti.xcom_pull(task_ids="data_ingestion", key="data_value")
        if not data_value:
            logging.info("No data change detected. Skipping all subsequent tasks.")
            return
        
        model_trainer_artifact = ti.xcom_pull(task_ids="model_drift_checking_data_transformation_and_model_training", key="model_trainer_artifact")
        if model_trainer_artifact:
            logging.info("Validating the model...")

            f1_score = model_trainer_artifact.test_data_metric_artifact.get('f1_score') if isinstance(model_trainer_artifact.test_data_metric_artifact, dict) else model_trainer_artifact.test_data_metric_artifact.f1_score

            if f1_score > training_pipeline.model_trainer_config.expected_f1_score_test_data:
                model_validate_artifact = training_pipeline.start_model_validate(
                    data_ingestion_artifact=ti.xcom_pull(task_ids="data_ingestion", key="data_ingestion_artifact"),
                    model_trainer_artifact=model_trainer_artifact,
                )
                ti.xcom_push("model_validate_artifact", model_validate_artifact)
            else:
                logging.info(f"Model F1-score ({f1_score}) is not better than expected ({training_pipeline.model_trainer_config.expected_f1_score_test_data}), skipping pipeline.")
                ti.xcom_push("model_validate_artifact", None) 
        else:
            logging.info("Model is performing well So No model to validate.")
            ti.xcom_push("model_validate_artifact", None) 
    except Exception as e:
        logging.error(f"Error during model validation: {str(e)}")
        raise e

# Task 5: Model Pusher
def model_pusher(**kwargs):
    ti = kwargs['ti']
    try:
        data_value = ti.xcom_pull(task_ids="data_ingestion", key="data_value")
        if not data_value:
            logging.info("No data change detected. Skipping all subsequent tasks.")
            return

        model_validate_artifact = ti.xcom_pull(task_ids="model_validation", key="model_validate_artifact")
        if model_validate_artifact and model_validate_artifact.is_model_accepted:
            logging.info("Pushing model to production...")
            model_pusher_artifact = training_pipeline.start_model_pusher(model_validate_artifact=model_validate_artifact)
            logging.info("Model successfully pushed to production.")
        else:
            logging.info("Model is performing well // Model not accepted  skipping push to production.") 
    except Exception as e:
        logging.error(f"Error during model pusher: {str(e)}")
        raise e


# Airflow DAG setup
with DAG(
    "training_pipeline",
    default_args={"retries": 0},
    description="Training pipeline for model validation and deployment",
    schedule_interval="@daily",  
    start_date=datetime(today.year, today.month, today.day),
    catchup=False,
    tags=["machine_learning", "model_training", "usvisa"],
) as dag:

    # Task 1: Data Ingestion
    data_ingestion_task = PythonOperator(
        task_id="data_ingestion",
        python_callable=data_ingestion,
    )

    # Task 2: Data validation and Data Drift Checking
    data_validation_and_data_drift_checking_task = PythonOperator(
        task_id="data_validation_and_data_drift_checking",
        python_callable=data_validation_and_data_drift_checking,
    )

    # Task 3: Model Drift Checking & Data Transformation and Model Training
    model_drift_checking_data_transformation_and_model_training_task = PythonOperator(
        task_id="model_drift_checking_data_transformation_and_model_training",
        python_callable=model_drift_checking_data_transformation_and_model_training,
    )

    # Task 4: Model Validation
    model_validation_task = PythonOperator(
        task_id="model_validation",
        python_callable=model_validation,
    )

    # Task 5: Model Pusher
    model_pusher_task = PythonOperator(
        task_id="model_pusher",
        python_callable=model_pusher,
    )
    
    # Task Dependencies
    data_ingestion_task >> data_validation_and_data_drift_checking_task >> model_drift_checking_data_transformation_and_model_training_task >> model_validation_task >> model_pusher_task
