from enum import Enum
from dataclasses import dataclass

class RequestType(Enum):
    Unknown = 0
    New = 1
    Modify = 2
    Cancel = 3

class ResponseType(Enum):
    Unknown = 0
    Accept = 1
    Reject = 2

@dataclass
class OrderRequest:
    m_symbolId: int
    m_price: float
    m_qty: int
    m_side: str
    m_orderId: int

@dataclass
class OrderResponse:
    m_orderId: int
    m_responseType: ResponseType
    
