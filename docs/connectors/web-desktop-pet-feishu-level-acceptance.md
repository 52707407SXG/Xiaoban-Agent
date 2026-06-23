# Web Desktop Pet Feishu-Level Acceptance

The web desktop pet must have the same core Agent capability as Feishu for My
Stand work. UI style can differ, but task capability should not be downgraded.

## Required Parity Tasks

1. Read reference material.
   - Web: select a Reference ID in the desktop pet.
   - Feishu: send the same Reference ID or bound object.
   - Expected: both resolve through the same permission and context pipeline.

2. Analyze an uploaded file.
   - Web: upload Excel/PDF/Word/image/Markdown/TXT.
   - Feishu: send equivalent attachment if channel allows.
   - Expected: both go through My Stand Parser and produce structured summaries.

3. Explain the current page.
   - Web: page/module context is automatic.
   - Feishu: user supplies the page/module reference.
   - Expected: Xiaoban uses MMCC context providers and help-center summaries.

4. Create an event.
   - Web: tool approval appears in the desktop pet.
   - Feishu: approval appears as channel-appropriate confirmation.
   - Expected: both use stable `messageId` / idempotency key and do not duplicate.

5. Resume after disconnect.
   - Web: refresh the page.
   - Feishu: reconnect or retry delivery.
   - Expected: ConversationLog and TaskState restore the task.

## Not Acceptable

- Web relies on frontend recent-message memory while Feishu uses server history.
- Web cannot upload files when Feishu can.
- Web cannot show tool status or confirmations.
- Web sends raw references in prompt text instead of structured `references[]`.
- Web trusts browser-submitted role or permissions.

## Minimum UI States

- Idle.
- Xiaoban is processing.
- Reading file.
- Checking evidence.
- Calling tool.
- Waiting for confirmation.
- Retrying.
- Interrupted.
- Failed with retry.
- Completed.

The short default processing text can be `小伴处理中...`.
