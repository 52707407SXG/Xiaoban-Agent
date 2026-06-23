"""Durable receive store contract.

The in-memory store is for local smoke tests and dev-only operation. Production
must replace it with SQLite or My Stand's server-side durable store before
public traffic is allowed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from .events import DeliveryKey, DurableReceiveResult, NormalizedInboundEvent


class DurableReceiveStore(Protocol):
    """Production replaceable receive de-duplication contract."""

    def accept(self, event: NormalizedInboundEvent) -> DurableReceiveResult:
        """Record or reject one normalized inbound event."""

    def has_seen(self, key: DeliveryKey) -> bool:
        """Return whether the stable delivery key was already accepted."""


@dataclass
class InMemoryDurableReceiveStore:
    """Volatile dev/smoke store.

    This class loses state on process restart. It is safe for local smoke tests
    only; production must provide SQLite or My Stand host persistence.
    """

    seen: set[str] = field(default_factory=set)

    def accept(self, event: NormalizedInboundEvent) -> DurableReceiveResult:
        key = event.delivery_key
        stable = key.stable_key
        if stable in self.seen:
            return DurableReceiveResult(accepted=False, delivery_key=key, status="duplicate")
        self.seen.add(stable)
        return DurableReceiveResult(accepted=True, delivery_key=key, status="accepted")

    def has_seen(self, key: DeliveryKey) -> bool:
        return key.stable_key in self.seen
