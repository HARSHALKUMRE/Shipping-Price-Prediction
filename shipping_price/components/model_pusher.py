import os
import sys
from shipping_price.exception import ShippingException
from shipping_price.logger import logging
from shipping_price.entity.artifacts_entity import (
    DataTransformationArtifacts,
    ModelPusherArtifacts,
    ModelTrainerArtifacts
)
from shipping_price.entity.config_entity import ModelPusherConfig
from shipping_price.configuration.s3_operations import S3Operation


class ModelPusher:
    def __init__(
        self,
        model_pusher_config: ModelPusherConfig,
        model_trainer_artifact: ModelTrainerArtifacts,
        data_transformation_artifact: DataTransformationArtifacts,
        s3: S3Operation
    ):
        self.model_pusher_config = model_pusher_config
        self.model_trainer_artifact = model_trainer_artifact
        self.data_transformation_artifact = data_transformation_artifact
        self.s3 = s3
        
    # This method is used to initiate model pusher
    def initiate_model_pusher(self) -> ModelPusherArtifacts:
        """
        Method Name: initiate_model_pusher
        
        Description: This method initiates model pusher
        
        Output: Model Pusher Artifacts
        """
        logging.info("Entered initiate_model_pusher method for Model Pusher class") 
        try:
            # Uploading the best model to s3 bucket
            self.s3.upload_file(
                self.model_trainer_artifact.trained_model_file_path,
                self.model_pusher_config.S3_MODEL_KEY_PATH,
                self.model_pusher_config.BUCKET_NAME,
                remove=False,
            )
            logging.info("Uploaded best model to s3 bucket")
            logging.info("Exited initiate_model_pusher method for Model Pusher class")
            
            # Saving the model pusher artifacts
            model_pusher_artifact = ModelPusherArtifacts(
                bucket_name=self.model_pusher_config.BUCKET_NAME,
                s3_model_path=self.model_pusher_config.S3_MODEL_KEY_PATH,
            )
            
            return model_pusher_artifact
        except Exception as e:
            raise ShippingException(e, sys) from e