"""Connector contracts for Xiaoban-Agent."""

from .events import DeliveryKey, DurableReceiveResult, NormalizedInboundEvent
from .durable_receive import DurableReceiveStore, InMemoryDurableReceiveStore
from .response import build_connector_response
from .web_desktop_pet import (
    build_web_desktop_pet_response,
    normalize_web_desktop_pet_event,
    parse_web_desktop_pet_envelope,
)

__all__ = [
    "DeliveryKey",
    "DurableReceiveResult",
    "DurableReceiveStore",
    "InMemoryDurableReceiveStore",
    "NormalizedInboundEvent",
    "build_connector_response",
    "build_web_desktop_pet_response",
    "normalize_web_desktop_pet_event",
    "parse_web_desktop_pet_envelope",
]
