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