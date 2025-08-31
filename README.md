# pipeshub-assignment

## Order Management System

I implemented this simplified Order Management System (OMS) in Python.
The OMS receives orders from upstream systems, applies business rules, and sends them to an exchange. The system enforces trading session windows, throttling, and handles order modifications and cancellations.

## Requirements Covered

-   Orders only accepted within a configurable time window.
-   Throttle: only X orders per second can be sent; overflow queued.
-   Support Modify (update price/qty) and Cancel requests for queued orders.
-   Handle exchange responses, compute round-trip latency, and persist results.
-   Thread-safe design to handle bursts and concurrency.
-   Persistence layer using SQLite.

## Design & Architecture (with image)

<img width="919" height="1175" alt="Screenshot 2025-08-31 232905" src="https://github.com/user-attachments/assets/b04774fd-3105-42e4-8816-a9d165451707" />

## Key Asumption

-   Modify/Cancel affect only queued orders (not in-flight).

-   Exchange always sends a response eventually (no timeout logic implemented).

Assumption on `onData` Methods

The assignment specifies two overloads of the method onData:

-   onData(OrderRequest) – invoked when an upstream system sends a new/modify/cancel request.
-   onData(OrderResponse) – invoked when the exchange sends a response back.

In C++/Java this is possible because those languages support method overloading by parameter type.
In Python, method overloading is not supported, so we cannot define two onData functions with different signatures.

To resolve this,in my implementation, I used

`onData(request: OrderRequest) for upstream orders, and`

`onResponse(response: OrderResponse) for exchange responses.`
