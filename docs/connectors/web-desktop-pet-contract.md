# Web Desktop Pet Connector Contract

The My Stand desktop pet is a first-class Xiaoban connector. It must not be a
thin textarea that passes recent frontend memory into a prompt.

## Ownership

- My Stand frontend owns the UI.
- My Stand backend owns session authentication and trusted user identity.
- Xiaoban-Agent owns normalized conversation, task, memory, tool policy, and
  connector responses.

The first integration should be implemented by My Stand backend proxying to a
local Xiaoban service. The browser must not call Xiaoban directly with trusted
roles or module permissions.

## Inbound Message Envelope

```ts
type WebDesktopPetMessage = {
  channel: 'web-desktop-pet';
  conversationId: string;
  messageId: string;
  clientTs: string;
  userId: string;
  siteId?: string;
  workspaceId?: string;
  text: string;
  pageContext?: PageContextEnvelope;
  moduleContext?: ModuleContextEnvelope;
  references?: ReferenceEnvelope[];
  attachments?: AttachmentEnvelope[];
  action?: 'send' | 'retry' | 'interrupt' | 'new_conversation' | 'continue_conversation';
};
```

`userId`, `siteId`, `workspaceId`, and role information are hints from the
browser. My Stand backend must replace or verify them from the server session
before forwarding to Xiaoban.

## Conversation Controls

The connector must support:

- New conversation.
- Continue conversation.
- Retry a failed user message.
- Interrupt a running generation or tool loop.
- Restore messages and task state after refresh.

The frontend should not send “recent 12 messages” as the authority for context.
It should send stable IDs; Xiaoban and My Stand durable stores recover state.

## Attachments

Supported first-class types:

- image
- PDF
- Word
- Excel
- Markdown
- TXT

Attachments go through the My Stand file and Parser pipeline first. The desktop
pet sends file identifiers and parser summaries:

```ts
type AttachmentEnvelope = {
  fileId: string;
  name: string;
  mimeType: string;
  sizeBytes: number;
  parserJobId?: string;
  parserStatus: 'pending' | 'ready' | 'failed';
  parserSummaryRef?: string;
};
```

The frontend must not paste raw file content into the prompt as the security
boundary.

## Reference IDs

The desktop pet should reuse My Stand `ReferenceIdPicker` and send structured
references:

```ts
type ReferenceEnvelope = {
  referenceId: string;
  kind: string;
  moduleId?: string;
  recordId?: string;
  label?: string;
};
```

My Stand backend resolves references by permission. Xiaoban receives summaries
or authorized context handles, not arbitrary client-composed prompt text.

## Page and Module Context

```ts
type PageContextEnvelope = {
  pathname: string;
  title?: string;
  selectedText?: string;
};

type ModuleContextEnvelope = {
  moduleId?: string;
  objectId?: string;
  objectType?: string;
  graphId?: string;
  tableId?: string;
  eventId?: string;
};
```

Only structured clues should be sent by default. Do not push whole company data,
raw source files, or unrestricted module records into the conversation.

## MMCC and Approval UI

The desktop pet must be able to display:

- Tool call in progress.
- Waiting for confirmation.
- Denied by permission.
- Failed, retryable.
- Completed.

Writes, external sends, deletes, exports, permission changes, production
publishing, and M coin billing require explicit confirmation contracts.

Xiaoban must call module tools only through MMCC:

```txt
My Stand module manifest -> mmcc.agent.tools -> ToolRegistry -> SubagentGateway
```

No connector may import module internals directly.

## Response Envelope

```ts
type WebDesktopPetResponse = {
  ok: boolean;
  conversationId: string;
  messageId: string;
  assistantMessageId?: string;
  status: 'accepted' | 'duplicate' | 'running' | 'waiting_confirmation' | 'failed' | 'completed';
  text?: string;
  toolEvents?: ToolEventEnvelope[];
  error?: { code: string; message: string };
};
```

Production responses must not include raw prompt envelopes, runtime internals,
provider payloads, secrets, or raw source.
