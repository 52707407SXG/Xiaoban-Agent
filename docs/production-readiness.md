# Xiaoban-Agent Production Readiness

`f4db0f5-fix1` is a server baseline repair package. It is not a production
deployment approval.

## Ready In This Package

- Repository-root CLI launch works through `./bin/xiaoban`.
- No-key server smoke exists.
- MMCC fixtures validate without enabling module tools.
- My Stand default channel surface is narrowed.
- In-memory stores are labeled dev/smoke only.
- Web desktop pet and cross-channel sync contracts are documented.

## Not Production Ready Yet

- In-memory durable receive and identity stores must be replaced.
- Web/WeChat/Feishu connectors must run behind My Stand host authentication.
- Gateway responses must stay redacted in production mode.
- Module tools must be enabled only through MMCC, capability checks, dataScopes,
  idempotency keys, and audit logs.
- Attachments must go through My Stand file and Parser pipelines.
- No connector may trust `userId`, `role`, or `workspaceId` from a browser or
  external channel payload.

## Required Production Stores

- `DeliveryStore`: message receive de-duplication and replay protection.
- `IdentityStore`: channel identity to My Stand user binding.
- `ConversationStore`: durable conversation log.
- `TaskStateStore`: resumable task state and interrupt/retry state.
- `AuditStore`: tool call, approval, failure, and delivery audit.

The production implementation can use SQLite or My Stand host APIs, but it must
survive process restarts and multiple connector retries.

## MMCC Boundary

Xiaoban-Agent consumes `Mystand Module Capability Contract v0.1`.

- ToolRegistry registers only `mmcc.agent.tools`.
- ContextBuilder reads only `mmcc.agent.contextProviders`.
- SubagentGateway is the only module tool execution path.
- Connectors normalize messages and identities; they do not make business
  decisions.

First production experiments should be low-risk and read-only, such as a Feature
Store catalog summary. Do not begin with passwords, finance, business archives,
attachments, or external sending tools.
