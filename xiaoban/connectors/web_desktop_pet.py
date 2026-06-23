"""Web desktop pet connector normalization.

The browser envelope is not a permission boundary. My Stand backend should pass
trusted session identity into this normalizer; browser-submitted user/workspace
fields are kept only as untrusted metadata for debugging and audit.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from xiaoban.identity import ChannelIdentity, MyStandUserIdentity

from .events import NormalizedInboundEvent
from .response import build_connector_response

WebDesktopPetAction = Literal["send", "retry", "interrupt", "new_conversation", "continue_conversation"]
WebDesktopPetStatus = Literal[
    "accepted",
    "duplicate",
    "running",
    "waiting_confirmation",
    "failed",
    "completed",
]


@dataclass(frozen=True)
class WebDesktopPetEnvelope:
    channel: str
    conversation_id: str
    message_id: str
    client_ts: str
    text: str
    action: WebDesktopPetAction = "send"
    site_id: str = ""
    workspace_id: str = ""
    browser_user_id: str = ""
    page_context: dict[str, Any] | None = None
    module_context: dict[str, Any] | None = None
    references: tuple[dict[str, Any], ...] = ()
    attachments: tuple[dict[str, Any], ...] = ()


def parse_web_desktop_pet_envelope(raw: dict[str, Any]) -> WebDesktopPetEnvelope:
    channel = str(raw.get("channel") or "web-desktop-pet")
    if channel != "web-desktop-pet":
        raise ValueError("web desktop pet envelope must use channel=web-desktop-pet")

    conversation_id = str(raw.get("conversationId") or raw.get("conversation_id") or "").strip()
    message_id = str(raw.get("messageId") or raw.get("message_id") or "").strip()
    client_ts = str(raw.get("clientTs") or raw.get("client_ts") or "").strip()
    if not conversation_id:
        raise ValueError("conversationId is required")
    if not message_id:
        raise ValueError("messageId is required")
    if not client_ts:
        raise ValueError("clientTs is required")

    action = str(raw.get("action") or "send")
    if action not in {"send", "retry", "interrupt", "new_conversation", "continue_conversation"}:
        raise ValueError(f"unsupported web desktop pet action: {action}")

    references = raw.get("references") or ()
    attachments = raw.get("attachments") or ()
    if not isinstance(references, (list, tuple)):
        raise ValueError("references must be an array")
    if not isinstance(attachments, (list, tuple)):
        raise ValueError("attachments must be an array")

    return WebDesktopPetEnvelope(
        channel=channel,
        conversation_id=conversation_id,
        message_id=message_id,
        client_ts=client_ts,
        text=str(raw.get("text") or ""),
        action=action,  # type: ignore[arg-type]
        site_id=str(raw.get("siteId") or raw.get("site_id") or ""),
        workspace_id=str(raw.get("workspaceId") or raw.get("workspace_id") or ""),
        browser_user_id=str(raw.get("userId") or raw.get("user_id") or ""),
        page_context=dict(raw.get("pageContext") or raw.get("page_context") or {}),
        module_context=dict(raw.get("moduleContext") or raw.get("module_context") or {}),
        references=tuple(dict(item) for item in references),
        attachments=tuple(dict(item) for item in attachments),
    )


def normalize_web_desktop_pet_event(
    raw: dict[str, Any],
    *,
    trusted_user: MyStandUserIdentity | None = None,
) -> NormalizedInboundEvent:
    envelope = parse_web_desktop_pet_envelope(raw)
    site_id = trusted_user.site_id if trusted_user else envelope.site_id
    user_id = trusted_user.user_id if trusted_user else envelope.browser_user_id
    if not site_id:
        site_id = "unknown-site"
    if not user_id:
        user_id = "unknown-user"

    channel_identity = ChannelIdentity(
        channel="web-desktop-pet",
        channel_account_id=site_id,
        external_chat_id=envelope.conversation_id,
        external_user_id=user_id,
    )
    kind = "file" if envelope.attachments else "text"
    return NormalizedInboundEvent(
        connector="web-desktop-pet",
        channel_identity=channel_identity,
        message_id=envelope.message_id,
        conversation_id=envelope.conversation_id,
        client_ts=envelope.client_ts,
        kind=kind,
        text=envelope.text,
        attachments=envelope.attachments,
        metadata={
            "action": envelope.action,
            "trustedUserId": trusted_user.user_id if trusted_user else "",
            "browserUserId": envelope.browser_user_id,
            "workspaceId": envelope.workspace_id,
            "pageContext": envelope.page_context or {},
            "moduleContext": envelope.module_context or {},
            "references": envelope.references,
            "identitySource": "mystand-session" if trusted_user else "untrusted-browser-envelope",
        },
    )


def build_web_desktop_pet_response(
    receive_result,
    *,
    conversation_id: str,
    message_id: str,
    status: WebDesktopPetStatus | None = None,
    text: str = "",
    assistant_message_id: str = "",
    tool_events: tuple[dict[str, Any], ...] = (),
    error: dict[str, str] | None = None,
) -> dict[str, Any]:
    base = build_connector_response(receive_result, error=error["code"] if error else None)
    base.update(
        {
            "conversationId": conversation_id,
            "messageId": message_id,
            "status": status or base["status"],
            "text": text,
            "assistantMessageId": assistant_message_id,
            "toolEvents": list(tool_events),
        }
    )
    if error:
        base["error"] = error
    return base


__all__ = [
    "WebDesktopPetEnvelope",
    "build_web_desktop_pet_response",
    "normalize_web_desktop_pet_event",
    "parse_web_desktop_pet_envelope",
]
