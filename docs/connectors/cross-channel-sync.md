# Cross-Channel Conversation Sync

Xiaoban should share one service-side conversation brain across website desktop
pet, WeChat, Feishu, Enterprise WeChat, QQ, CLI, and webhook connectors.

## Core Rule

Channels are entrances. ConversationLog, TaskState, Memory, ToolRegistry, and
MMCC policy live on the server.

## Channel Binding

```ts
type ChannelBinding = {
  userId: string;
  siteId: string;
  channel: 'web-desktop-pet' | 'weixin' | 'feishu' | 'wecom' | 'qqbot' | 'cli' | 'webhook';
  externalUserId: string;
  externalChatId: string;
  defaultConversationId: string;
  bindingStatus: 'pending' | 'verified' | 'revoked';
  createdAt: string;
  lastSeenAt: string;
};
```

WeChat binding must prove ownership through a My Stand login or an approved
pairing flow. Knowing a `userId` is not enough to join a conversation.

## Conversation Log

```ts
type ConversationLogRow = {
  conversationId: string;
  messageId: string;
  channel: string;
  userId: string;
  text?: string;
  attachments?: unknown[];
  references?: unknown[];
  clientTs: string;
  serverTs: string;
  status: 'accepted' | 'duplicate' | 'running' | 'failed' | 'completed';
};
```

Every connector writes to the same log before runtime execution. Duplicate
delivery keys do not re-run tools.

## Delivery Key

```txt
channel + channelAccountId + externalChatId + externalMessageId
```

This prevents collisions across multiple public accounts, Feishu apps, groups,
or browser sessions.

## Sync Modes

- `shared_context`: share context silently without pushing every message.
- `notify`: send important progress or final result to another channel.
- `mirror`: show all messages in another channel.

Recommended default:

- Website desktop pet shows all messages in the active conversation.
- WeChat receives important status and final results only, unless the user opts
  into full mirroring.

## Web Realtime

The desktop pet should use SSE or WebSocket:

1. Web connects with authenticated My Stand session.
2. Backend subscribes to conversation events.
3. WeChat message lands in ConversationLog.
4. Desktop pet receives task and message events.
5. User can continue from the web UI without losing context.

## Acceptance

- User says in WeChat: “继续刚才网站上那个任务”.
- Xiaoban resolves the user's verified ChannelBinding.
- Xiaoban finds the same `conversationId` and `taskId`.
- Website desktop pet shows the WeChat-triggered task state.
- Duplicate WeChat retries do not duplicate events, M coin billing, or module
  writes.
