import os
import sys
from pandas import DataFrame
from shipping_price.exception import ShippingException
from shipping_price.logger import logging
from typing import Tuple
from sklearn.model_selection import train_test_split
from shipping_price.configuration.mongo_operations import MongoDBOperation
from shipping_price.entity.config_entity import DataIngestionConfig
from shipping_price.entity.artifacts_entity import DataIngestionArtifacts
from shipping_price.constant import TEST_SIZE

class DataIngestion:
    def __init__(self,
                 data_ingestion_config: DataIngestionConfig, mongo_op: MongoDBOperation):
        self.data_ingestion_config = data_ingestion_config
        self.mongo_op = mongo_op
        
        
    def get_data_from_mongodb(self) -> DataFrame:
        """
        Method Name: get_data_from_mongodb
        
        Description: This method fetches data from MongoDB database.
        
        Output: DataFrame
        """
        logging.info("Entered get_data_from_mongodb method of Data Ingestion class")
        try:
            logging.info("Getting the dataframe from mongodb")
            
            # getting collection from MongoDB database
            df = self.mongo_op.get_collection_as_dataframe(
                self.data_ingestion_config.DB_NAME,
                self.data_ingestion_config.COLLECTION_NAME,
            )
            
            logging.info("Got the dataframe from MongoDB")
            logging.info("Exited the get_data_from_mongodb method of Data Ingestion class")
            return df
        
        except Exception as e:
            raise ShippingException(e, sys) from e
        
        
    # This method will split the data
    def split_data_as_train_test(self, df: DataFrame) -> Tuple[DataFrame, DataFrame]:
        """
        Method Name: split_data_as_train_test
        
        Description: This method splits the dataframe into train set and test set based on split ratio.
        
        Output: Train DataFrame and Test DataFrame
        """
        
        logging.info("Entered split_data_as_train_test method of Data Ingestion class")
        try:
            # Creating Data Ingestion Artifacts directory inside Artifact folder
            os.makedirs(
                self.data_ingestion_config.DATA_INGESTION_ARTIFACTS_DIR, exist_ok=True
            )
            
            # Splitting the data into train and test set
            train_set, test_set = train_test_split(df, test_size=TEST_SIZE)
            logging.info("Performed train test split on the dataframe")
            
            # Creating train directory under data ingestion artifacts directory
            os.makedirs(
                self.data_ingestion_config.TRAIN_DATA_ARTIFACTS_FILE_DIR, exist_ok=True
            )
            logging.info(
                f"Created {os.path.basename(self.data_ingestion_config.TRAIN_DATA_ARTIFACTS_FILE_DIR)} directory"
            )
            
            # Creating test directory under data ingestion artifacts directory
            os.makedirs(
                self.data_ingestion_config.TEST_DATA_ARTIFACTS_FILE_DIR, exist_ok=True
            )
            logging.info(
                f"Created {os.path.basename(self.data_ingestion_config.TEST_DATA_ARTIFACTS_FILE_DIR)} directory"
            )
            
            # Saving train.csv file to train directory
            train_set.to_csv(
                self.data_ingestion_config.TRAIN_DATA_FILE_PATH,
                index=False,
                header=True,
            )
            
            # Saving test.csv file to test directory
            test_set.to_csv(
                self.data_ingestion_config.TEST_DATA_FILE_PATH,
                index=False,
                header=True,
            )
            
            logging.info("Converted Train DataFrame and Test DataFrame into csv format")
            logging.info(
                f"Saved {os.path.basename(self.data_ingestion_config.TRAIN_DATA_FILE_PATH)},\
                  {os.path.basename(self.data_ingestion_config.TEST_DATA_FILE_PATH)} in\
                      {os.path.basename(self.data_ingestion_config.DATA_INGESTION_ARTIFACTS_DIR)}."
            )
            
            logging.info("Exited the split_data_as_train_test method of Data Ingestion class")
            
            return train_set, test_set

        except Exception as e:
            raise ShippingException(e, sys) from e
        
    # This method initiates data ingestion
    def initiate_data_ingestion(self) -> DataIngestionArtifacts:
        """
        Method Name: initiate_data_ingestion
        
        Description: This method initiates data ingestion
        
        Output: Data Ingestion Artifact Object
        """
        logging.info("Entered initiate_data_ingestion method of Data Ingestion class") 
        try:
            # Getting data from mongodb
            df  = self.get_data_from_mongodb()
            
            # Dropping the unnecessary columns from dataframe
            df1 = df.drop(self.data_ingestion_config.DROP_COLS, axis=1)
            df1 = df1.dropna()
            logging.info("Got the data from mongodb")
            
            # Splitting the data into train and test set
            self.split_data_as_train_test(df1)
            logging.info("Exited initiate_data_ingestion method of Data Ingestion class")
            
            # Saving data ingestion artifacts
            data_ingestion_artifact = DataIngestionArtifacts(
                train_data_file_path=self.data_ingestion_config.TRAIN_DATA_FILE_PATH,
                test_data_file_path=self.data_ingestion_config.TEST_DATA_FILE_PATH,
            )
            
            return data_ingestion_artifact
        except Exception as e:
            raise ShippingException(e, sys) from e


