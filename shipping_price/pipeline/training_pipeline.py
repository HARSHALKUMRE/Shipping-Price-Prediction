import sys
from shipping_price.exception import ShippingException
from shipping_price.logger import logging
from shipping_price.configuration.mongo_operations import MongoDBOperation
from shipping_price.entity.config_entity import DataIngestionConfig
from shipping_price.entity.artifacts_entity import DataIngestionArtifacts
from shipping_price.components.data_ingestion import DataIngestion


class TrainingPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.mongo_op = MongoDBOperation()
        
    
    # This method is used to start the data ingestion
    def start_data_ingestion(self) -> DataIngestionArtifacts:
        logging.info("Entered the start_data_ingestion method of TrainingPipeline class")
        try:
            logging.info("Getting the data from mongodb")
            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config,
                mongo_op=self.mongo_op
            )
            
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Got the train_set and test_set from mongodb")
            logging.info("Exited the start_data_ingestion method of TrainingPipeline Class")
            return data_ingestion_artifact
        except Exception as e:
            raise ShippingException(e, sys) from e
        
        
    # This method is used to start the training pipeline
    def run_pipeline(self) -> None:
        logging.info("Entered the run_pipeline method of TrainingPipeline class")
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            
            logging.info("Exited the run_pipeline method of TrainingPipeline class")
        except Exception as e:
            raise ShippingException(e, sys) from e