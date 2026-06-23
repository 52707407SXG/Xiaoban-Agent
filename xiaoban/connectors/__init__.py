"""Connector contracts for Xiaoban-Agent."""

from .events import DeliveryKey, DurableReceiveResult, NormalizedInboundEvent
from .durable_receive import DurableReceiveStore, InMemoryDurableReceiveStore
from .response import build_connector_response

__all__ = [
    "DeliveryKey",
    "DurableReceiveResult",
    "DurableReceiveStore",
    "InMemoryDurableReceiveStore",
    "NormalizedInboundEvent",
    "build_connector_response",
]
