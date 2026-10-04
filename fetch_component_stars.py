"""
抓取课简扩展组件仓库的 GitHub 元数据，写成 components-stars.json。

components.json 是一个 JSON 数组，每一项可以是：

* "owner/repo" —— 只给仓库名，不带额外信息；
* {"repo": "owner/repo", "aliases": ["雨课堂", "yuketang"]} —— 仓库加搜索别名。

"aliases" 是用户在课简里搜组件时比对的词。仓库名多半是英文
（"YuKeTang_notice_plugin"），用户搜的却是「雨课堂」，所以把组件的中文名、
常用叫法和拼音都写进来；App 按忽略大小写的子串匹配，不做拼音转换。
加别名只改注册表，不必给 App 发版。

为了和插件注册表（cursimple-plugins）的 plugins-stars.json 用同一套解析，
"schools" 键照样认，原样写进输出；条目也可以写 "kind"，但只能是 "extension"。
输出里每一项都带 "kind": "extension"，App 靠它把组件和导课插件分开。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_SOURCE = (
    "https://raw.githubusercontent.com/"
    "cursimple/cursimple-components/refs/heads/main/components.json"
)
DEFAULT_OUTPUT = "components-stars.json"
GRAPHQL_URL = "https://api.github.com/graphql"
COMPONENT_KIND = "extension"
REGISTRY_NAME = "components.json"


def request_json(url: str, *, token: str | None = None, payload: dict[str, Any] | None = None) -> Any:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {
        "Accept": "application/json",
        "User-Agent": "github-star-fetch",
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"
        headers["Content-Type"] = "application/json"

    request = Request(url, data=data, headers=headers, method="POST" if payload else "GET")

    try:
        with urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} from {url}: {body}") from exc
    except URLError as exc:
        raise RuntimeError(f"Failed to request {url}: {exc.reason}") from exc


def load_source(source: str) -> Any:
    # 工作流里直接读检出的文件：raw.githubusercontent.com 有几分钟的缓存，
    # 刚合并的条目去读线上地址可能还是旧的
    if source.startswith(("http://", "https://")):
        return request_json(source)
    return json.loads(Path(source).read_text(encoding="utf-8"))


def clean_names(raw: Any, index: int, key: str) -> list[str]:
    if not isinstance(raw, list):
        raise ValueError(f"{REGISTRY_NAME} item #{index} must carry a list \"{key}\"")
    names: list[str] = []
    for value in raw:
        if not isinstance(value, str):
            raise ValueError(f"{REGISTRY_NAME} item #{index} has a non-string entry in \"{key}\"")
        name = value.strip()
        if name and name not in names:
            names.append(name)
    return names


def load_repo_entries(source: str) -> tuple[list[str], dict[str, dict[str, list[str]]]]:
    """返回仓库名列表，以及每个仓库声明的 schools / aliases。"""
    data = load_source(source)

    if not isinstance(data, list):
        raise ValueError(f"{REGISTRY_NAME} must be a JSON array")

    repo_names: list[str] = []
    names_by_repo: dict[str, dict[str, list[str]]] = {}

    for index, item in enumerate(data, start=1):
        declared: dict[str, list[str]] = {}
        if isinstance(item, str):
            repo_name = item.strip()
        elif isinstance(item, dict):
            raw_repo = item.get("repo")
            if not isinstance(raw_repo, str):
                raise ValueError(f"{REGISTRY_NAME} item #{index} must carry a string \"repo\"")
            repo_name = raw_repo.strip()
            kind = item.get("kind", COMPONENT_KIND)
            if kind != COMPONENT_KIND:
                raise ValueError(
                    f"{REGISTRY_NAME} item #{index} declares kind {kind!r}; "
                    f"only {COMPONENT_KIND!r} belongs in the component registry"
                )
            for key in ("schools", "aliases"):
                if key in item:
                    declared[key] = clean_names(item[key], index, key)
        else:
            raise ValueError(f"{REGISTRY_NAME} item #{index} must be a string or an object")

        parts = repo_name.split("/")
        if len(parts) != 2 or not all(parts):
            raise ValueError(f"{REGISTRY_NAME} item #{index} must use owner/repo format: {item!r}")
        if repo_name in names_by_repo:
            raise ValueError(f"{REGISTRY_NAME} item #{index} repeats {repo_name}")

        repo_names.append(repo_name)
        names_by_repo[repo_name] = declared

    return repo_names, names_by_repo


def build_query(repo_names: list[str]) -> str:
    fields: list[str] = []

    for index, repo_name in enumerate(repo_names, start=1):
        owner, name = repo_name.split("/", 1)
        fields.append(
            f"""
    repo{index:03d}: repository(owner: {json.dumps(owner)}, name: {json.dumps(name)}) {{
      nameWithOwner
      name
      owner {{
        login
        avatarUrl(size: 80)
      }}
      description
      stargazerCount
      primaryLanguage {{
        name
      }}
      url
    }}"""
        )

    return (
        "query GetComponentRepositoryStars {"
        + "".join(fields)
        + """
    rateLimit {
      limit
      remaining
      used
      resetAt
      cost
    }
  }"""
    )


def repository_from_graphql(
    value: dict[str, Any],
    names_by_repo: dict[str, dict[str, list[str]]] | None = None,
) -> dict[str, Any]:
    owner = value["owner"]
    primary_language = value["primaryLanguage"]
    name_with_owner = value["nameWithOwner"]

    repository: dict[str, Any] = {
        "name": name_with_owner,
        "repo": value["name"],
        "owner": owner["login"],
        "avatar": owner["avatarUrl"],
        "description": value["description"] or "",
        "star": value["stargazerCount"],
        "language": primary_language["name"] if primary_language else "",
        "url": value["url"],
    }

    # 没声明的键整个省掉，和 plugins-stars.json 的写法一致
    declared = (names_by_repo or {}).get(name_with_owner) or {}
    for key in ("schools", "aliases"):
        if declared.get(key):
            repository[key] = declared[key]

    repository["kind"] = COMPONENT_KIND
    return repository


def fetch_repo_batch(
    repo_names: list[str],
    token: str,
    names_by_repo: dict[str, dict[str, list[str]]] | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    response = request_json(GRAPHQL_URL, token=token, payload={"query": build_query(repo_names)})

    if not isinstance(response, dict):
        raise RuntimeError("GitHub GraphQL response must be a JSON object")

    if response.get("errors"):
        raise RuntimeError(f"GitHub GraphQL returned errors: {json.dumps(response['errors'])}")

    data = response.get("data")
    if not isinstance(data, dict):
        raise RuntimeError("GitHub GraphQL response is missing data")

    repositories: list[dict[str, Any]] = []
    for index in range(1, len(repo_names) + 1):
        key = f"repo{index:03d}"
        value = data.get(key)
        if value is None:
            raise RuntimeError(f"GitHub GraphQL returned no data for {repo_names[index - 1]}")
        repositories.append(repository_from_graphql(value, names_by_repo))

    rate_limit = data.get("rateLimit")
    if not isinstance(rate_limit, dict):
        raise RuntimeError("GitHub GraphQL response is missing rateLimit")

    return repositories, rate_limit


def fetch_all_repos(
    repo_names: list[str],
    token: str,
    batch_size: int,
    names_by_repo: dict[str, dict[str, list[str]]] | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    repositories: list[dict[str, Any]] = []
    rate_limits: list[dict[str, Any]] = []

    for start in range(0, len(repo_names), batch_size):
        batch = repo_names[start : start + batch_size]
        batch_number = start // batch_size + 1
        print(f"Fetching batch {batch_number}: {len(batch)} repositories")

        batch_repositories, rate_limit = fetch_repo_batch(batch, token, names_by_repo)
        repositories.extend(batch_repositories)
        rate_limits.append(rate_limit)

        print(
            "Fetched batch "
            f"{batch_number}: cost={rate_limit.get('cost')}, "
            f"remaining={rate_limit.get('remaining')}"
        )

    return repositories, rate_limits


def write_json_file(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        delete=False,
        dir=str(path.parent),
        prefix=f".{path.name}.",
        suffix=".tmp",
    ) as temp_file:
        json.dump(data, temp_file, ensure_ascii=False, separators=(",", ":"))
        temp_name = temp_file.name

    Path(temp_name).replace(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch repository metrics for cursimple extension components and write JSON data."
    )
    parser.add_argument(
        "--source",
        default=DEFAULT_SOURCE,
        help="components.json 的本地路径或 URL",
    )
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--batch-size", type=int, default=100)
    parser.add_argument("--token-env", default="GITHUB_TOKEN")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    token = os.environ.get(args.token_env)
    if not token:
        print(f"Environment variable {args.token_env} is required", file=sys.stderr)
        return 1

    if args.batch_size < 1 or args.batch_size > 100:
        print("--batch-size must be between 1 and 100", file=sys.stderr)
        return 1

    repo_names, names_by_repo = load_repo_entries(args.source)
    tagged = sum(1 for declared in names_by_repo.values() if any(declared.values()))
    print(
        f"Loaded {len(repo_names)} repositories from {args.source} "
        f"({tagged} with declared aliases)"
    )

    repositories, _rate_limits = fetch_all_repos(
        repo_names, token, args.batch_size, names_by_repo
    )
    repositories_by_stars = sorted(repositories, key=lambda item: item["star"], reverse=True)

    output = {
        "repositories": repositories_by_stars,
    }

    write_json_file(Path(args.output), output)
    print(f"Wrote {len(repositories)} repositories to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
