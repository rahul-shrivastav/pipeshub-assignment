import threading
import logging,time
from .order_queue import OrderQueue
from .persistance import Persistence
from datetime import datetime,time as dt_time
from models.order_model import OrderRequest,OrderResponse,RequestType

class OrderManagement:
    def __init__(self, start_time: dt_time, end_time: dt_time, throttle_limit=100):
        self.start_time = start_time
        self.end_time = end_time
        self.throttle_limit = throttle_limit
        self.running = True

        #instantiate core components
        self.queue = OrderQueue()
        self.db = Persistence()

        #already sent orders to exchange.
        self.in_flight = {}

        #necessary locks for thread safety
        self.in_flight_lock = threading.Lock()
        self.send_lock = threading.Lock()

        #thread that sends orders to exchange
        self.sender_thread = threading.Thread(target=self.sender_loop, daemon=True)
        self.sender_thread.start()

    def _is_session_open(self):
        curr_time = datetime.now().time()
        return self.start_time <= curr_time <= self.end_time

    def onData(self, request: OrderRequest, req_type: RequestType):
        if not self._is_session_open():
            logging.info(f"Rejecting order {request.m_orderId}, outside session period")
            return

        if req_type == RequestType.New:
            self.queue.enqueue(request)
        elif req_type == RequestType.Modify:
            self.queue.modify(request.m_orderId, request.m_price, request.m_qty)
        elif req_type == RequestType.Cancel:
            self.queue.cancel(request.m_orderId)

    def onResponse(self, response: OrderResponse):
        now = time.monotonic()
        with self.in_flight_lock:
            send_ts = self.in_flight.pop(response.m_orderId, None)
        if send_ts:
            latency_ms = (now - send_ts) * 1000
            self.db.record_response(response.m_orderId, response.m_responseType, latency_ms)
            logging.info(f"Recorded response for order {response.m_orderId}, latency {latency_ms:.2f}ms")

    def sender_loop(self):
        while self.running:
            sent_this_second = 0
            start_sec = int(time.time())

            while int(time.time()) == start_sec:
                if sent_this_second >= self.throttle_limit:
                    time.sleep(0.01)
                    continue

                order = self.queue.dequeue()
                
                if order:
                    with self.send_lock:
                        self.send(order)
                    with self.in_flight_lock:
                        self.in_flight[order.m_orderId] = time.monotonic()
                    sent_this_second += 1
                else:
                    time.sleep(0.01)

    def send(self, request: OrderRequest):
        logging.info(f"Sending order {request.m_orderId} to exchange")

    def sendLogon(self):
        logging.info("Sending Logon message")

    def sendLogout(self):
        logging.info("Sending Logout message")

    def stop(self):
        self.running = False
        self.sender_thread.join()
