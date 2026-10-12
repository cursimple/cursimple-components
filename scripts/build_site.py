"""Package the registry and optional published metadata for the static catalog."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
STARS_URL = "https://raw.githubusercontent.com/cursimple/cursimple-components/component-stars-data/components-stars.json"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true", help="Refresh the bundled public metadata snapshot")
    args = parser.parse_args()
    entries = json.loads((ROOT / "components.json").read_text())
    if not isinstance(entries, list):
        raise ValueError("components.json must be an array")
    target = ROOT / "docs/data"
    target.mkdir(parents=True, exist_ok=True)
    (target / "components.json").write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n")
    if args.refresh:
        try:
            request = Request(STARS_URL, headers={"User-Agent": "CurSimple-component-catalog"})
            with urlopen(request, timeout=20) as response:
                data = json.load(response)
            if not isinstance(data.get("repositories"), list):
                raise ValueError("invalid metadata")
            (target / "components-stars.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
            print("Refreshed published component metadata")
        except Exception as error:
            print(f"Metadata unavailable; keeping bundled snapshot ({type(error).__name__})")
    if not (target / "components-stars.json").is_file():
        (target / "components-stars.json").write_text('{"repositories":[]}\n')
    output = ROOT / "build/site"
    output.mkdir(parents=True, exist_ok=True)
    for name in ("index.html", "style.css", "app.js", "catalog.js", "i18n.js"):
        shutil.copy2(ROOT / "docs" / name, output / name)
    for name in ("assets", "data"):
        shutil.copytree(ROOT / "docs" / name, output / name, dirs_exist_ok=True)
    print(f"Catalog built from {len(entries)} registry entries")


if __name__ == "__main__":
    main()
