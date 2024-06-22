import os
from dotenv import load_dotenv
from datetime import datetime
from from_root.root import from_root

load_dotenv()

TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

MODEL_CONFIG_FILE = "configs/model.yaml"
SCHEMA_CONFIG_FILE = "configs/schema.yaml"

DB_URL = os.getenv("MONGODB_URL")

TARGET_COLUMN = "Cost"
DB_NAME = "iNeuron"
COLLECTION_NAME = "shipping_price"
TEST_SIZE = 0.2

ARTIFACTS_DIR = os.path.join(from_root(), "artifacts", TIMESTAMP)

"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_ARTIFACTS_DIR = "DataIngestionArtifacts"
DATA_INGESTION_TRAIN_DIR = "Train"
DATA_INGESTION_TEST_DIR = "Test"
DATA_INGESTION_TRAIN_FILE_NAME = "train.csv"
DATA_INGESTION_TEST_FILE_NAME = "test.csv"

"""
Data Validation related constant start with DATA_VALIDATION VAR NAME
"""
DATA_VALIDATION_ARTIFACTS_DIR = "DataValidationArtifacts"
DATA_DRIFT_FILE_NAME = "DataDriftReport.yaml"

"""
Data Transformation related constant start with DATA_TRANSFORMATION VAR NAME
"""
DATA_TRANSFORMATION_ARTIFACTS_DIR = "DataTransformationArtifacts"
TRANSFORMED_TRAIN_DATA_DIR = "TransformedTrain"
TRANSFORMED_TEST_DATA_DIR = "TransformedTest"
TRANSFORMED_TRAIN_DATA_FILE_NAME = "transformed_train_data.npz"
TRANSFORMED_TEST_DATA_FILE_NAME = "transformed_test_data.npz"
PREPROCESSOR_OBJECT_FILE_NAME = "shipping_preprocessor.pkl"

"""
Model Trainer related constant start with MODEL_TRAINER VAR NAME
"""
MODEL_TRAINER_ARTIFACTS_DIR = "ModelTrainerArtifacts"
MODEL_FILE_NAME = "shipping_price_model.pkl"
MODEL_SAVE_FORMAT = ".pkl"