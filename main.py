import time
import config
import logging
from datetime import time as dt_time

from core_objects.oms import OrderManagement
from models.order_model import OrderRequest, OrderResponse, RequestType, ResponseType
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

if __name__ == "__main__":
    #_initialize Order Management System
    oms = OrderManagement(start_time=config.SESSION_START, end_time=config.SESSION_END, throttle_limit=config.THROTTLE_LIMIT)

    #_simulate upstream orders
    for i in range(10):
        #dummy request
        req = OrderRequest(1, 100.5+i, 10, 'B', i)
        oms.onData(req, RequestType.New)

    time.sleep(1)
    
    #_simulate exchange responses
    for i in range(10):
        #dummy response
        resp = OrderResponse(i, ResponseType.Accept)
        oms.onResponse(resp)

    oms.stop()
