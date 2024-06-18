from shipping_price.logger import logging
import sys
from shipping_price.exception import ShippingException

logging.info("Hello World")

try:
    a = 2 + '3'
    print(a)
except Exception as e:
    raise ShippingException(e, sys) from e