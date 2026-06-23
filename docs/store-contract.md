# Store Contract

Xiaoban-Agent can run smoke tests with in-memory stores, but production must use
durable storage from SQLite or My Stand host APIs.

## Dev-Only Stores

- `InMemoryDurableReceiveStore`: local duplicate-message smoke only.
- `InMemoryIdentityDirectory`: local identity-binding smoke only.

Both lose state on restart and are not safe for public traffic.

## Required Interfaces

### DeliveryStore

Accepts or rejects inbound events by stable delivery key:

```txt
channel + channelAccountId + externalChatId + externalMessageId
```

It prevents duplicate tool calls, duplicate M coin billing, and duplicate event
creation when channels retry messages.

### IdentityStore

Maps external channel identities to trusted My Stand users. It must be backed by
My Stand authentication and binding flows, not browser-submitted `userId`.

### ConversationStore

Persists normalized user and assistant messages across web, WeChat, Feishu,
Enterprise WeChat, QQ, CLI, and webhook connectors.

### TaskStateStore

Persists running tasks, interruptions, retries, approvals, and recovery points.

### AuditStore

Records tool calls, approvals, redacted inputs/outputs, errors, duration, and
idempotency keys.

## Production Rule

The connector can receive a message only after durable receive is written. The
runtime can call a module tool only through SubagentGateway after MMCC policy,
capability, dataScope, sideEffect, and idempotency checks pass.
