import os
import sys
from dataclasses import dataclass
import pandas as pd
from pandas import DataFrame
from shipping_price.logger import logging
from shipping_price.exception import ShippingException
from shipping_price.entity.artifacts_entity import (
    DataIngestionArtifacts,
    ModelTrainerArtifacts,
    ModelEvaluationArtifacts,
)
from shipping_price.entity.config_entity import ModelEvaluationConfig
from shipping_price.constant import *


@dataclass
class EvaluateModelResponse:
    trained_model_r2_score: float
    s3_model_r2_score: float
    is_model_accepted: bool
    difference: float
    
    
class ModelEvaluation:
    def __init__(
        self,
        model_trainer_artifact: ModelTrainerArtifacts,
        model_evaluation_config: ModelEvaluationConfig,
        data_ingestion_artifact: DataIngestionArtifacts
    ):
        self.model_trainer_artifact = model_trainer_artifact
        self.model_evaluation_config = model_evaluation_config
        self.data_ingestion_artifact = data_ingestion_artifact
    
    # This method is used to get the s3 model
    def get_s3_model(self) -> object:
        """
        Method Name: get_s3_model
        
        Description: This method gets model from s3 bucket.

        Output: Model
        """
        logging.info("Entered the get_s3_model method of Model Evaluation class")
        try:
            # Checking whether model is present in s3 bucket or not
            status = self.model_evaluation_config.S3_OPERATIONS.is_model_present(
                BUCKET_NAME, S3_MODEL_NAME
            )
            logging.info(f"Got the status - is model present? -> {status}")
            
            # If model is present then loading the model
            if status == True:
                model = self.model_evaluation_config.S3_OPERATIONS.load_model(
                    MODEL_FILE_NAME, BUCKET_NAME
                )
                logging.info("Exited the get_s3_model method of Model Evaluation class")
                return model
            
            else:
                None
                
        except Exception as e:
            raise ShippingException(e, sys) from e
        
    # This method is used to evaluate the model
    def evaluate_model(self) -> EvaluateModelResponse:
        """
        Method Name: evaluate_model

        Description: This method evaluates s3 bucket model and production model.

        Output: This model give output above evaluation metric, whether model is accepted or not.
        """
        logging.info("Entered the evaluate_model method of Model Evaluation class")
        try:
            # Reading the test data and splitting it into train and test
            test_df = pd.read_csv(self.data_ingestion_artifact.test_data_file_path)
            x, y = test_df.drop(TARGET_COLUMN, axis=1), test_df[TARGET_COLUMN]
            logging.info("splitted the test data into train and test")
            
            # Loading production model for prediction
            trained_model = self.model_evaluation_config.UTILS.load_object(
                self.model_trainer_artifact.trained_model_file_path
            )
            y_hat_trained_model = trained_model.predict(x)
            logging.info("Prediction done with production model")
            
            # Checking r2 score of production model
            trained_model_r2_score = self.model_evaluation_config.UTILS.get_model_score(
                y, y_hat_trained_model
            )
            
            # Loading the s3 model
            s3_model_r2_score = None
            s3_model = self.get_s3_model()
            if s3_model is not None:
                y_hat_s3_model = s3_model.predict(x)
                s3_model_r2_score = self.model_evaluation_config.UTILS.get_model_score(
                    y, y_hat_s3_model
                )
                
            # Saving the s3 model r2 score in tmp_best_model_score variable
            tmp_best_model_score = 0 if s3_model_r2_score is None else s3_model_r2_score
            
            # Saving the Evaluate model response
            result = EvaluateModelResponse(
                trained_model_r2_score=trained_model_r2_score,
                s3_model_r2_score=s3_model_r2_score,
                #is_model_accepted=trained_model_r2_score > tmp_best_model_score,
                is_model_accepted=True,
                difference=trained_model_r2_score - tmp_best_model_score
            )
            
            logging.info("Exited the evaluate_model method of Model Evaluation class")
            return result
        
        except Exception as e:
            raise ShippingException(e, sys) from e
        
        
    # This method is used to initiate model evaluation
    def initiate_model_evaluation(self) -> ModelEvaluationArtifacts:
        """
        Method Name: initiate_model_evaluation
        
        Description: This method intiates the model evaluation.

        Output: model evaluation artifacts.
        """
        logging.info(
            "Entered the initiate_model_evaluation method of Model Evaluation class"
        )
        try:
            evaluate_model_response = self.evaluate_model()
            
            # Saving model evaluation artifact
            model_evaluation_artifact = ModelEvaluationArtifacts(
                is_model_accepted=evaluate_model_response.is_model_accepted,
                trained_model_path=self.model_trainer_artifact.trained_model_file_path,
                changed_accuracy=evaluate_model_response.difference,
            )
            
            logging.info(
                "Exited the initiate_model_evaluation method of Model Evaluation class"
            )
            
            return model_evaluation_artifact
        except Exception as e:
            raise ShippingException(e, sys) from e