# 🧩 Cursimple Extension Component Registry

[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

**English** | **[中文](README.md)**

> **The official extension component registry for Cursimple.**  
> Only components listed in this repository will appear in Cursimple's component list.

---

## 🎯 What is this?

This is the **extension component registry** for Cursimple. Every extension component shown in Cursimple must be registered in the [`components.json`](components.json) file of this repository.

### Components vs. plugins

| | Import plugins ([cursimple-plugins](https://github.com/cursimple/cursimple-plugins)) | Extension components (this repo) |
|---|---|---|
| Purpose | Import a timetable from the school's academic system | Keep homework, exams, announcements, etc. synced into Cursimple |
| Lifecycle | Runs once per import and exits after handing over the timetable | Stays installed: sign in once, then Cursimple syncs it periodically in the background |
| Output | Timetable | New-item notifications, due-date reminders, sidebar calendar, timetable tasks |
| Where to find | "Import from academic system", searched by school name | Component list, searched by component name or alias |

A component package has the same layout as an import plugin (`manifest.json` + entry script + `checksums.json`); the difference is `"kind": "extension"` in its manifest.

---

## 📋 Currently Listed Components

| Component Repository | Search Aliases |
|---------------------|----------------|
| [cursimple/YuKeTang_notice_plugin](https://github.com/cursimple/YuKeTang_notice_plugin) | 雨课堂通知 / 雨课堂 / 长江雨课堂 / 黄河雨课堂 / 荷塘雨课堂 / yuketang / ykt |

> 💡 The table above is generated from [`components.json`](components.json) — do not edit it by hand. Metadata such as stars is refreshed automatically.

---

## 🤝 How to Submit a Component?

### Method 1: Direct Edit (Requires Collaborator Access)

1. Click [Edit components.json on GitHub](https://github.com/cursimple/cursimple-components/edit/main/components.json)
2. Add your component to the JSON array (see "Entry format" below)
3. Commit the change

### Method 2: Submit a Pull Request (Recommended)

1. Fork this repository
2. Add your component to `components.json`
3. Open a Pull Request
4. Wait for review and merge

### Entry format

Prefer the object form, and use `aliases` to declare the words users may search for:

```json
[
  {
    "repo": "cursimple/YuKeTang_notice_plugin",
    "aliases": ["雨课堂通知", "雨课堂", "长江雨课堂", "yuketang"]
  }
]
```

Repository names are usually English (`YuKeTang_notice_plugin`) while users search in Chinese (「雨课堂」), so list in `aliases`:

- The component's Chinese name: `雨课堂通知`
- Common names of the platform it connects to: `雨课堂`, `长江雨课堂`
- Pinyin or English spellings: `yuketang`

Matching is a **case-insensitive substring match; prefixes count**. The app does no pinyin conversion — add pinyin as its own alias.

To stay compatible with the plugin registry, the `schools` key works too (merged with `aliases`, duplicates removed). An entry may also declare `"kind": "extension"`; any other value is rejected. The bare-string form still works:

```json
["cursimple/YuKeTang_notice_plugin"]
```

### Component repository requirements

- Hosted on GitHub as a public repository
- The package's `manifest.json` declares `"kind": "extension"` and is compatible with Cursimple's plugin API
- **Releases are published as GitHub Releases**; the latest release must carry these assets:
  - the component zip, e.g. `yuketang-notice-v1.0.0.zip`
  - a `manifest.json` naming the zip and its version:

    ```json
    {
      "filename": "yuketang-notice-v1.0.0.zip",
      "version": "v1.0.0"
    }
    ```

Cursimple finds the latest version via `https://github.com/<owner>/<repo>/releases/latest/download/manifest.json` and builds the download URL from its `filename`. This release `manifest.json` is a different file from the `manifest.json` inside the package. Do not mark the release as a pre-release, or `latest` will not point at it.

---

## 🛠️ Technical Details

### File structure

```
cursimple-components/
├── .github/
│   └── workflows/
│       └── update-component-stars.yml  # GitHub Actions: builds the component list and syncs the table
├── components.json                     # Component registry (core file, hand-written)
├── fetch_component_stars.py            # Fetches component repository metadata
├── render_readme_table.py              # Generates the README table from components.json
└── LICENSE                             # MIT License
```

### How it works

1. **Registration**: components are listed in `components.json`, each as `{"repo": "owner/repo", "aliases": [...]}` (the bare `"owner/repo"` string is also accepted)
2. **Data refresh**: on every push to `main`, every 6 hours, and on manual dispatch, GitHub Actions fetches stars, description, avatar, etc. for every component and writes `components-stars.json`
3. **Publishing**: `components-stars.json` is published to the orphan branch [`component-stars-data`](https://github.com/cursimple/cursimple-components/tree/component-stars-data) (the only file on that branch), followed by a jsDelivr cache purge
4. **App consumption**: Cursimple reads `https://raw.githubusercontent.com/cursimple/cursimple-components/component-stars-data/components-stars.json`; every entry carries `"kind": "extension"` and otherwise uses the same fields as the plugin registry's `plugins-stars.json`

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🔗 Related Links

- [Cursimple](https://github.com/cursimple) - Main Cursimple project
- [Import plugin registry](https://github.com/cursimple/cursimple-plugins) - Plugins that import timetables
- [Submit a component](https://github.com/cursimple/cursimple-components/edit/main/components.json) - Add your component

---

<p align="center">
  <sub>Maintained by the Cursimple team ❤️</sub>
</p>
