import sys
from shipping_price.exception import ShippingException
from shipping_price.logger import logging
from shipping_price.configuration.mongo_operations import MongoDBOperation
from shipping_price.entity.config_entity import (DataIngestionConfig,
                                                 DataValidationConfig,
                                                 DataTransformationConfig)
from shipping_price.entity.artifacts_entity import (DataIngestionArtifacts,
                                                    DataValidationArtifacts,
                                                    DataTransformationArtifacts)
from shipping_price.components.data_ingestion import DataIngestion
from shipping_price.components.data_validation import DataValidation
from shipping_price.components.data_transformation import DataTransformation


class TrainingPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
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
        
    # This method is used to start the data validation
    def start_data_validation(
        self, data_ingestion_artifacts: DataIngestionArtifacts   
    ) -> DataValidationArtifacts:
        logging.info("Entered the start_data_validation method of TrainingPipeline class") 
        try:
            data_validation = DataValidation(
                data_ingestion_artifacts=data_ingestion_artifacts,
                data_validation_config=self.data_validation_config
            )
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("Performed data validation operation")
            logging.info("Exited the start_data_validation method of TrainingPipeline class")
            return data_validation_artifact
        except Exception as e:
            raise ShippingException(e, sys) from e
        
    # This method is used to start the data Transformation
    def start_data_transformation(
        self, data_ingestion_artifacts: DataIngestionArtifacts
    ) -> DataTransformationArtifacts:
        logging.info("Entered the start_data_transformation method of TrainingPipeline class")
        try:
            data_transformation = DataTransformation(
                data_ingestion_artifacts=data_ingestion_artifacts,
                data_transformation_config=self.data_transformation_config
            )
            data_transformation_artifact = (
                data_transformation.initiate_data_transformation()
            )
            logging.info(
                "Exited the start_data_transformation method of TrainingPipeline class"
            )
            return data_transformation_artifact
        except Exception as e:
            raise ShippingException(e, sys) from e
        
        
    # This method is used to start the training pipeline
    def run_pipeline(self) -> None:
        logging.info("Entered the run_pipeline method of TrainingPipeline class")
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            
            data_validation_artifact = self.start_data_validation(
                data_ingestion_artifacts=data_ingestion_artifact
            )
            
            data_transformation_artifact = self.start_data_transformation(
                data_ingestion_artifacts=data_ingestion_artifact
            )
            
            logging.info("Exited the run_pipeline method of TrainingPipeline class")
        except Exception as e:
            raise ShippingException(e, sys) from e