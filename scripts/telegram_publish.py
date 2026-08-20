#!/usr/bin/env python3
"""Publish verified dossier notifications to a Telegram channel.

Modes:
- verify: validates the bot token and channel publishing rights.
- publish: sends one photo post from a JSON manifest.

The bot token is read only from TELEGRAM_BOT_TOKEN and is never printed.
"""

from __future__ import annotations

import html
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API_ROOT = "https://api.telegram.org"


class TelegramError(RuntimeError):
    pass


def require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def api_request(token: str, method: str, params: dict[str, str]) -> dict:
    url = f"{API_ROOT}/bot{token}/{method}"
    data = urllib.parse.urlencode(params).encode("utf-8")
    request = urllib.request.Request(url, data=data, method="POST")

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            description = json.loads(body).get("description", "Telegram API request failed")
        except json.JSONDecodeError:
            description = "Telegram API returned an invalid error response"
        raise TelegramError(f"Telegram API returned HTTP {exc.code}: {description}") from exc
    except urllib.error.URLError as exc:
        raise TelegramError(f"Telegram API connection failed: {exc.reason}") from exc

    try:
        result = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise TelegramError("Telegram API returned a non-JSON response") from exc

    if not result.get("ok"):
        raise TelegramError(str(result.get("description") or "Telegram API request failed"))
    return dict(result.get("result") or {})


def load_post_config(path: str) -> dict[str, str]:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            config = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Unable to read Telegram post configuration: {exc}") from exc

    required = ("publish_id", "title", "summary", "article_url", "image_url", "author")
    missing = [name for name in required if not str(config.get(name, "")).strip()]
    if missing:
        raise RuntimeError(f"Telegram post configuration is missing: {', '.join(missing)}")

    normalized = {name: str(config[name]).strip() for name in required}
    for field in ("article_url", "image_url"):
        parsed = urllib.parse.urlparse(normalized[field])
        if parsed.scheme != "https" or not parsed.netloc:
            raise RuntimeError(f"{field} must be a public HTTPS URL")

    if len(normalized["title"]) > 220:
        raise RuntimeError("Telegram title must not exceed 220 characters")
    if len(normalized["summary"]) > 650:
        raise RuntimeError("Telegram summary must not exceed 650 characters")
    return normalized


def verify_access(token: str, chat_id: str) -> tuple[str, int]:
    bot = api_request(token, "getMe", {})
    bot_id = int(bot.get("id") or 0)
    username = str(bot.get("username") or "")
    if not bot_id:
        raise TelegramError("Telegram did not return the bot identity")

    chat = api_request(token, "getChat", {"chat_id": chat_id})
    if str(chat.get("type") or "") != "channel":
        raise TelegramError("TELEGRAM_CHAT_ID does not identify a channel")

    membership = api_request(
        token,
        "getChatMember",
        {"chat_id": chat_id, "user_id": str(bot_id)},
    )
    if str(membership.get("status") or "") not in {"administrator", "creator"}:
        raise TelegramError("The bot is not an administrator of the Telegram channel")
    if membership.get("can_post_messages") is False:
        raise TelegramError("The bot does not have permission to publish messages")

    return username, bot_id


def build_caption(config: dict[str, str]) -> str:
    caption = (
        f"<b>{html.escape(config['title'])}</b>\n\n"
        f"{html.escape(config['summary'])}\n\n"
        f"<a href=\"{html.escape(config['article_url'], quote=True)}\">"
        "Leggi il dossier completo</a>\n\n"
        f"<i>{html.escape(config['author'])}</i>"
    )
    if len(caption) > 1024:
        raise RuntimeError("Rendered Telegram caption exceeds the 1024-character limit")
    return caption


def main() -> int:
    token = require_env("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "@emiralili").strip()
    mode = os.environ.get("PUBLISH_MODE", "verify").strip().lower()
    username, bot_id = verify_access(token, chat_id)
    print(f"Telegram bot verified: @{username or 'unknown'} (bot ID {bot_id})")
    print(f"Telegram channel verified: {chat_id}")

    if mode == "verify":
        print("Verification completed. No content was published.")
        return 0

    if mode != "publish":
        raise RuntimeError("PUBLISH_MODE must be verify or publish")

    config_path = require_env("SOCIAL_POST_FILE")
    config = load_post_config(config_path)
    reply_markup = json.dumps(
        {
            "inline_keyboard": [
                [{"text": "Leggi su emiralili.it", "url": config["article_url"]}]
            ]
        },
        ensure_ascii=False,
    )
    sent = api_request(
        token,
        "sendPhoto",
        {
            "chat_id": chat_id,
            "photo": config["image_url"],
            "caption": build_caption(config),
            "parse_mode": "HTML",
            "reply_markup": reply_markup,
        },
    )
    message_id = int(sent.get("message_id") or 0)
    if not message_id:
        raise TelegramError("Telegram did not return a published message ID")

    print(
        "Telegram dossier notification published successfully "
        f"(message ID {message_id}, publish ID {config['publish_id']})"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (TelegramError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
