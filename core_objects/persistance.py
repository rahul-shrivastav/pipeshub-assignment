import sqlite3
import threading

class Persistence:
    def __init__(self, db_file="responses.db"):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.lock = threading.Lock()
        self._init_db()

    def _init_db(self):
        with self.conn:
            query = "CREATE TABLE IF NOT EXISTS order_responses (order_id INTEGER PRIMARY KEY,response TEXT,latency_ms REAL)"
            self.conn.execute(query)

    def record_response(self, order_id, resp_type, latency_ms):
        with self.lock:
            with self.conn:
                query = "INSERT OR REPLACE INTO order_responses(order_id, response, latency_ms) VALUES (?, ?, ?)"
                self.conn.execute(query,(order_id, resp_type.name, latency_ms))