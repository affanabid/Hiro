import base64
import os
from typing import Any, Dict, Optional, Tuple

import requests

GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"
GITHUB_REST_URL = "https://api.github.com"


def _get_token() -> str:
    """Return the GitHub token from env or raise if missing."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable is not set.")
    return token


def _headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {_get_token()}",
        "Accept": "application/vnd.github+json",
    }


def execute_graphql(query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Execute a GraphQL query and return the `data` payload."""
    response = requests.post(
        GITHUB_GRAPHQL_URL,
        json={"query": query, "variables": variables or {}},
        headers=_headers(),
        timeout=20,
    )
    response.raise_for_status()
    payload = response.json()
    if "errors" in payload:
        messages = "; ".join(err.get("message", "Unknown error") for err in payload["errors"])
        raise RuntimeError(f"GitHub GraphQL Errors: {messages}")
    return payload.get("data", {})


def fetch_repo_path(owner: str, repo: str, path: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Fetch a file/directory at the given path.

    Returns:
        (type, content) where type is "file" or "dir". If 404, returns (None, None).
        Content is decoded text for files when available.
    """
    url = f"{GITHUB_REST_URL}/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(url, headers=_headers(), timeout=20)
    if response.status_code == 404:
        return None, None
    response.raise_for_status()
    data: Any = response.json()

    item_type = data.get("type")
    if item_type == "file":
        content = data.get("content") or ""
        encoding = data.get("encoding")
        if encoding == "base64":
            try:
                decoded = base64.b64decode(content).decode("utf-8", errors="ignore")
            except Exception:
                decoded = ""
            return item_type, decoded
        return item_type, None

    if item_type == "dir":
        return item_type, None

    # Some endpoints return a list when path is a directory; treat as directory presence.
    if isinstance(data, list):
        return "dir", None

    return None, None
