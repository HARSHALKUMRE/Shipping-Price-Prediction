from shipping_price.logger import logging
import sys
from shipping_price.exception import ShippingException
from shipping_price.pipeline.training_pipeline import TrainingPipeline

try:
    pipeline = TrainingPipeline()
    pipeline.run_pipeline()
except Exception as e:
    raise ShippingException(e, sys) from e