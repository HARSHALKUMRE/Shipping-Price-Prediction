import os
from dotenv import load_dotenv

load_dotenv()

MODEL_CONFIG_FILE = "configs/model.yaml"

DB_URL = os.getenv("MONGODB_URL")