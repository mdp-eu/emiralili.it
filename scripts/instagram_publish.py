#!/usr/bin/env python3
"""Minimal Instagram publisher for GitHub Actions.

Modes:
- verify: validates the token and reports the connected Instagram identity.
- publish: publishes one public HTTPS image after an explicit PUBLISH confirmation.

The access token is read only from INSTAGRAM_ACCESS_TOKEN and is never printed.
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "https://graph.instagram.com"


class ApiError(RuntimeError):
    pass


def api_request(method: str, path: str, params: dict[str, str]) -> dict:
    url = f"{BASE_URL}{path}"
    encoded = urllib.parse.urlencode(params).encode()
    if method == "GET":
        url = f"{url}?{encoded.decode()}"
        data = None
    else:
        data = encoded

    request = urllib.request.Request(url, data=data, method=method)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            message = json.loads(body).get("error", {}).get("message", body)
        except json.JSONDecodeError:
            message = body
        raise ApiError(f"Instagram API returned HTTP {exc.code}: {message}") from exc
    except urllib.error.URLError as exc:
        raise ApiError(f"Instagram API connection failed: {exc.reason}") from exc

    try:
        return json.loads(payload)
    except json.JSONDecodeError as exc:
        raise ApiError("Instagram API returned a non-JSON response") from exc


def require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def get_identity(token: str) -> tuple[str, str]:
    profile = api_request(
        "GET",
        "/me",
        {
            "fields": "id,user_id,username",
            "access_token": token,
        },
    )
    user_id = str(profile.get("user_id") or profile.get("id") or "")
    username = str(profile.get("username") or "")
    if not user_id:
        raise ApiError("Connected Instagram identity did not return a user ID")
    return user_id, username


def wait_until_ready(container_id: str, token: str) -> None:
    for _ in range(12):
        status = api_request(
            "GET",
            f"/{container_id}",
            {
                "fields": "status_code,status",
                "access_token": token,
            },
        )
        code = str(status.get("status_code") or "")
        if code == "FINISHED":
            return
        if code in {"ERROR", "EXPIRED"}:
            detail = status.get("status") or code
            raise ApiError(f"Media container failed: {detail}")
        time.sleep(5)
    raise ApiError("Media container was not ready within 60 seconds")


def load_post_config(path: str) -> dict[str, object]:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            config = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Unable to read social post configuration: {exc}") from exc

    required = ("publish_id", "article_url", "image_url", "caption")
    missing = [name for name in required if not str(config.get(name, "")).strip()]
    if missing:
        raise RuntimeError(f"Social post configuration is missing: {', '.join(missing)}")
    normalized: dict[str, object] = {name: str(config[name]).strip() for name in required}
    delete_ids = config.get("delete_media_ids", [])
    if not isinstance(delete_ids, list):
        raise RuntimeError("delete_media_ids must be a list")
    normalized["delete_media_ids"] = [str(value).strip() for value in delete_ids if str(value).strip()]
    return normalized


def main() -> int:
    token = require_env("INSTAGRAM_ACCESS_TOKEN")
    mode = os.environ.get("PUBLISH_MODE", "verify").strip().lower()
    config_path = os.environ.get("SOCIAL_POST_FILE", "").strip()
    config = load_post_config(config_path) if config_path else None
    user_id, username = get_identity(token)
    print(f"Instagram identity verified: @{username or 'unknown'} (user ID {user_id})")

    if mode == "verify":
        print("Verification completed. No content was published.")
        return 0

    if mode != "publish":
        raise RuntimeError("PUBLISH_MODE must be verify or publish")

    auto_publish = os.environ.get("AUTO_PUBLISH", "").strip().lower() == "true"
    confirmation = os.environ.get("PUBLISH_CONFIRMATION", "").strip().upper()
    if not auto_publish and confirmation != "PUBLISH":
        state = "empty" if not confirmation else "invalid"
        raise RuntimeError(
            f"Publishing blocked: confirmation was {state}; enter PUBLISH in the final field"
        )

    if auto_publish:
        if not config:
            raise RuntimeError("Automatic publishing requires SOCIAL_POST_FILE")
        image_url = config["image_url"]
        caption = config["caption"]
        print(f"Automatic post authorized by manifest: {config['publish_id']}")
    else:
        image_url = require_env("IMAGE_URL")
        caption = require_env("CAPTION")
    for media_id in config.get("delete_media_ids", []) if config else []:
        api_request("DELETE", f"/{media_id}", {"access_token": token})
        print(f"Instagram post deleted successfully (media ID {media_id})")

    parsed = urllib.parse.urlparse(image_url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise RuntimeError("IMAGE_URL must be a public HTTPS URL")

    container = api_request(
        "POST",
        f"/{user_id}/media",
        {
            "image_url": image_url,
            "caption": caption,
            "access_token": token,
        },
    )
    container_id = str(container.get("id") or "")
    if not container_id:
        raise ApiError("Instagram did not return a media container ID")

    wait_until_ready(container_id, token)
    published = api_request(
        "POST",
        f"/{user_id}/media_publish",
        {
            "creation_id": container_id,
            "access_token": token,
        },
    )
    media_id = str(published.get("id") or "")
    if not media_id:
        raise ApiError("Instagram did not return a published media ID")

    print(f"Instagram post published successfully (media ID {media_id})")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ApiError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
