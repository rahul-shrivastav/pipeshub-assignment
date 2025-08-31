# pipeshub-assignment

Order Management System

This project implements a simplified Order Management System (OMS) in Python.
The OMS receives orders from upstream systems, applies business rules, and sends them to an exchange. The system enforces trading session windows, throttling, and handles order modifications and cancellations.

🎯 Requirements Covered

✔ Orders only accepted within a configurable time window (session).
✔ Logon at start and Logout at end of session.
✔ Throttle: only X orders per second can be sent; overflow queued.
✔ Support Modify (update price/qty) and Cancel requests for queued orders.
✔ Handle exchange responses, compute round-trip latency, and persist results.
✔ Thread-safe design to handle bursts and concurrency.
✔ Persistence layer using SQLite (standard library).

🏗️ Design & Architecture
🔹 Components

OrderQueue (core/order_queue.py)
FIFO queue with O(1) lookup by orderId using OrderedDict. Supports modify/cancel.

OrderManagement (core/oms.py)
Central orchestrator:

Accepts upstream orders (onData).

Maintains a sender thread with throttling (\_sender_loop).

Tracks in-flight orders for latency calculation.

Handles exchange responses (onResponse).

Calls persistence layer for storage.

Persistence (core/persistence.py)
Stores responses in SQLite with (orderId, responseType, latency_ms).

Models (models/)
Dataclasses for OrderRequest, OrderResponse, Logon, Logout. Enums for RequestType, ResponseType.

Utils (utils/logger.py)
Central logging setup.

Tests (tests/)
Unit tests for queue, throttle, session, and end-to-end integration.

🔹 Concurrency Model

Sender thread

Runs independently, enforces X orders/sec, sends orders from queue.

Main thread

Receives orders (onData) and responses (onResponse).

Locks

send_lock: ensures non-thread-safe send() is protected.

queue_lock: protects queue operations.

in_flight_lock: protects in-flight order dict.

db_lock: protects SQLite writes.
