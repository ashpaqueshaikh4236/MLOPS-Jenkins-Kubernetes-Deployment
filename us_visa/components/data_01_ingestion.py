import os
import sys
import pandas as pd
from typing import Union,Tuple

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from us_visa.constants import FILE_NAME
from us_visa.entity.config_entity import DataIngestionConfig
from us_visa.entity.artifact_entity import DataIngestionArtifact
from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.data_access.usvisa_data import USvisaData




class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig=DataIngestionConfig()):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise USvisaException(e,sys)
        


    def export_data_into_feature_store(self) -> Union[Tuple[pd.DataFrame, bool], pd.DataFrame]:
        try:
            logging.info("Exporting data from MongoDB")

            usvisa_data = USvisaData()
            dataframe = usvisa_data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)

            feature_store_file_path = self.data_ingestion_config.feature_store_file_path

            if not os.path.exists(feature_store_file_path):
                logging.info(f"{FILE_NAME} file does not exist. Creating and saving new file.")
                dir_path = os.path.dirname(feature_store_file_path)
                os.makedirs(dir_path, exist_ok=True)
                dataframe.to_csv(feature_store_file_path, index=False, header=True)
                logging.info(f"Exported data to {feature_store_file_path}, total records: {len(dataframe)}")
                return dataframe, True 

            else:
                logging.info(f"{FILE_NAME} file exists. Comparing data sizes.")
                df = pd.read_csv(feature_store_file_path)
                logging.info(f"Existing data size: {len(df)}")
                logging.info(f"New extracted data size: {len(dataframe)}")

                if len(dataframe) > len(df):
                    logging.info("New data is larger. Overwriting the file.")
                    dir_path = os.path.dirname(feature_store_file_path)
                    os.makedirs(dir_path, exist_ok=True)
                    dataframe.to_csv(feature_store_file_path, index=False, header=True)
                    logging.info(f"Exported data to {feature_store_file_path}, total records: {len(dataframe)}")
                    return dataframe, True


                else:
                    logging.info("No Data changed.")
                    return dataframe, False

        except Exception as e:
            logging.error(f"An error occurred: {e}")
            raise USvisaException(e, sys)
    
        

    def split_data_as_train_test(self,dataframe: DataFrame) ->None:
        logging.info("Entered split_data_as_train_test method of Data_Ingestion class")

        try:
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed train test split on the dataframe")
            logging.info("Exited split_data_as_train_test method of Data_Ingestion class")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            
            logging.info(f"Exporting train and test file path and shape.")
            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)
            
            logging.info(f"Shape of train_set {train_set.shape}")
            logging.info(f"Shape of test_set {test_set.shape}")

            logging.info(f"Exported train and test file path and shape.")
        except Exception as e:
            raise USvisaException(e, sys) from e
        


    
    def initiate_data_ingestion(self) ->DataIngestionArtifact:
        logging.info("Entered initiate_data_ingestion method of Data_Ingestion class")

        try:
            dataframe,data_value = self.export_data_into_feature_store()
            if data_value:
                logging.info("Got the data from MongoDB and it was updated.")
                self.split_data_as_train_test(dataframe)
                logging.info("Performed train-test split on the dataset.")
            else:
                logging.info("No data update detected. Skipping train-test split.")
            logging.info("Exited initiate_data_ingestion method of Data_Ingestion class")

            data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,test_file_path=self.data_ingestion_config.testing_file_path)
            if data_value:
                logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact, data_value
        except Exception as e:
            raise USvisaException(e, sys) from e