import json
import time
from collections import Counter
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Sequence, Tuple
from urllib.parse import urlparse

from .github_client import execute_graphql, fetch_repo_path

GITHUB_REPOS_QUERY = """
query GetUserRepos($login: String!, $after: String, $isFork: Boolean) {
  user(login: $login) {
    repositories(
      first: 100,
      after: $after,
      ownerAffiliations: OWNER,
      orderBy: {field: PUSHED_AT, direction: DESC},
      isFork: $isFork
    ) {
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        nameWithOwner
        pushedAt
        updatedAt
        stargazerCount
        forkCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges {
            size
            node {
              name
            }
          }
        }
      }
    }
  }
}
"""


def extract_github_username_from_url(url: str) -> Optional[str]:
    """
    Extract the GitHub username from a profile URL.

    Examples:
        https://github.com/username -> username
        https://github.com/username/ -> username
    """
    if not url:
        return None

    try:
        parsed = urlparse(url.strip())
        if "github.com" not in (parsed.netloc or ""):
            return None
        parts = (parsed.path or "").strip("/").split("/")
        return parts[0] if parts else None
    except Exception:
        return None


def _parse_iso(date_str: str) -> datetime:
    if date_str.endswith("Z"):
        date_str = date_str[:-1] + "+00:00"
    return datetime.fromisoformat(date_str)


def _language_percentages(edges: Sequence[Dict[str, Any]]) -> List[Tuple[str, int]]:
    languages: List[Tuple[str, int]] = []
    total = 0
    for edge in edges:
        size = edge.get("size") or 0
        name = edge.get("node", {}).get("name")
        if name and size:
            languages.append((name, size))
            total += size
    if total == 0:
        return []
    result: List[Tuple[str, int]] = []
    remaining = 100
    for idx, (name, size) in enumerate(languages):
        pct = round((size / total) * 100)
        if idx == len(languages) - 1:
            pct = max(0, min(100, remaining))
        remaining -= pct
        result.append((name, pct))
    return result


def _add_python_labels(content: str, labels: set[str]) -> None:
    lowered = content.lower()
    mapping = {
        "django": "Django",
        "djangorestframework": "Django REST Framework",
        "fastapi": "FastAPI",
        "flask": "Flask",
        "celery": "Celery",
    }
    for key, label in mapping.items():
        if key in lowered:
            labels.add(label)


def _add_package_json_labels(content: str, labels: set[str]) -> None:
    try:
        data = json.loads(content)
    except Exception:
        return

    deps = data.get("dependencies", {}) or {}
    dev_deps = data.get("devDependencies", {}) or {}
    all_keys = list(deps.keys()) + list(dev_deps.keys())
    mapping = {
        "react": "React",
        "next": "Next.js",
        "vue": "Vue",
        "@angular/core": "Angular",
        "express": "Express",
        "nestjs": "NestJS",
        "@nestjs/": "NestJS",
    }
    for key, label in mapping.items():
        for dep in all_keys:
            if dep == key or dep.startswith(key):
                labels.add(label)


def _infer_stack(owner: str, repo: str) -> List[str]:
    labels: set[str] = set()

    for path in ["requirements.txt", "pyproject.toml", "Pipfile"]:
        item_type, content = fetch_repo_path(owner, repo, path)
        if item_type == "file" and content:
            _add_python_labels(content, labels)

    item_type, content = fetch_repo_path(owner, repo, "package.json")
    if item_type == "file" and content:
        _add_package_json_labels(content, labels)

    item_type, _ = fetch_repo_path(owner, repo, "Dockerfile")
    if item_type:
        labels.add("Docker")

    item_type, _ = fetch_repo_path(owner, repo, "docker-compose.yml")
    if item_type:
        labels.add("Docker Compose")

    item_type, _ = fetch_repo_path(owner, repo, ".github/workflows")
    if item_type:
        labels.add("GitHub Actions")

    return sorted(labels)


def fetch_repositories(
    username: str,
    max_repos: int,
    years: Optional[int],
    include_forks: bool,
) -> List[Dict[str, Any]]:
    repos: List[Dict[str, Any]] = []
    has_next = True
    cursor: Optional[str] = None
    cutoff = None
    if years is not None:
        cutoff = datetime.now(timezone.utc) - timedelta(days=365 * years)

    is_fork_arg: Optional[bool] = None if include_forks else False

    while has_next and len(repos) < max_repos:
        try:
            data = execute_graphql(
                GITHUB_REPOS_QUERY,
                {"login": username, "after": cursor, "isFork": is_fork_arg},
            )
        except RuntimeError as exc:
            if "Could not resolve to a User" in str(exc) or "NOT_FOUND" in str(exc):
                return []
            raise
        user = data.get("user")
        if user is None:
            return []

        repo_conn = user.get("repositories") or {}
        nodes = repo_conn.get("nodes") or []
        page_info = repo_conn.get("pageInfo") or {}

        for node in nodes:
            if len(repos) >= max_repos:
                break

            pushed_at = node.get("pushedAt")
            if cutoff and pushed_at:
                pushed_date = _parse_iso(pushed_at)
                if pushed_date < cutoff:
                    has_next = False
                    break

            repos.append(node)

        has_next = bool(page_info.get("hasNextPage")) and len(repos) < max_repos and has_next
        cursor = page_info.get("endCursor")
        if has_next:
            time.sleep(0.2)

    return repos


def scrape_github_user(
    username: str,
    max_repos: int = 50,
    repo_limit: int = 30,
    years: Optional[int] = None,
    include_forks: bool = False,
) -> List[str]:
    repos = fetch_repositories(username, max_repos=max_repos, years=years, include_forks=include_forks)

    output: List[str] = []
    for idx, repo in enumerate(repos):
        name_with_owner = repo.get("nameWithOwner", "")
        languages_edges = repo.get("languages", {}).get("edges", []) or []
        language_parts = _language_percentages(languages_edges)
        languages_str = ", ".join(f"{name} ({pct}%)" for name, pct in language_parts) if language_parts else "(none)"

        stack_labels: List[str] = []
        if idx < repo_limit and name_with_owner and "/" in name_with_owner:
            owner, repo_name = name_with_owner.split("/", 1)
            stack_labels = _infer_stack(owner, repo_name)
        stack_str = ", ".join(stack_labels) if stack_labels else "(none)"

        output.append(f"{name_with_owner} -> {languages_str} | {stack_str}")

    return output


def get_github_insights(
    username: str,
    max_repos: int = 50,
    repo_limit: int = 30,
    years: Optional[int] = None,
    include_forks: bool = False,
) -> Dict[str, Any]:
    """
    Return structured insights for a GitHub user, suitable for frontend visualization.
    """
    repos = fetch_repositories(username, max_repos=max_repos, years=years, include_forks=include_forks)
    if not repos:
        return {
            "username": username,
            "repo_count": 0,
            "top_languages": [],
            "repos": [],
        }

    aggregated_langs: Counter[str] = Counter()
    repos_output: List[Dict[str, Any]] = []

    for idx, repo in enumerate(repos):
        name_with_owner = repo.get("nameWithOwner", "")
        pushed_at = repo.get("pushedAt")
        updated_at = repo.get("updatedAt")
        stars = repo.get("stargazerCount", 0)
        forks = repo.get("forkCount", 0)

        languages_edges = repo.get("languages", {}).get("edges", []) or []
        language_parts = _language_percentages(languages_edges)

        for lang_name, pct in language_parts:
            aggregated_langs[lang_name] += pct

        stack_labels: List[str] = []
        if idx < repo_limit and name_with_owner and "/" in name_with_owner:
            owner, repo_name = name_with_owner.split("/", 1)
            stack_labels = _infer_stack(owner, repo_name)

        repos_output.append(
            {
                "name_with_owner": name_with_owner,
                "pushed_at": pushed_at,
                "updated_at": updated_at,
                "stars": stars,
                "forks": forks,
                "languages": [
                    {"name": lang_name, "percent": pct} for lang_name, pct in language_parts
                ],
                "stack_labels": stack_labels,
            }
        )

    # Normalize aggregated language scores to approximate percentages
    total_lang_score = sum(aggregated_langs.values())
    if total_lang_score > 0:
        top_languages = [
            {
                "name": name,
                "percent": round((score / total_lang_score) * 100),
            }
            for name, score in aggregated_langs.most_common(10)
        ]
    else:
        top_languages = []

    return {
        "username": username,
        "repo_count": len(repos_output),
        "top_languages": top_languages,
        "repos": repos_output,
    }
