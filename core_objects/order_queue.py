import threading
from collections import OrderedDict
from models.order_model import OrderRequest

class OrderQueue:
    def __init__(self):
        self._queue = OrderedDict()
        self._lock = threading.Lock()

    def enqueue(self, order: OrderRequest):
        with self._lock:
            self._queue[order.m_orderId] = order

    def dequeue(self):
        with self._lock:
            if self._queue:
                _, order = self._queue.popitem(last=False)
                return order
            return None

    def modify(self,order_id,price,qty):
        with self._lock:
            if order_id in self._queue:
                order = self._queue[order_id]
                order.m_price = price
                order.m_qty = qty

    def cancel(self, order_id):
        with self._lock:
            if order_id in self._queue:
                del self._queue[order_id]

    def __len__(self):
        with self._lock:
            return len(self._queue)