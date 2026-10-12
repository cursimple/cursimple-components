# CurSimple · Component catalog

[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

**English** | **[中文](README.md)**

CurSimple's default extension-component registry, listing independent packages such as YuKeTang notices and multi-platform notifications. The website and app market share [`components.json`](components.json); users can also add other component sources in CurSimple.

[Component catalog](https://cursimple.github.io/cursimple-components/) · [App website](https://cursimple.github.io/cursimple-app/) · [School plugin catalog](https://cursimple.github.io/cursimple-plugins/)

---

## 🎯 What is this?

This is CurSimple's default public component source. Maintain listings in [`components.json`](components.json); users can also add other registries or individual component Release repositories in the app's source settings.

### Components vs. plugins

| | Import plugins ([cursimple-plugins](https://github.com/cursimple/cursimple-plugins)) | Extension components (this repo) |
|---|---|---|
| Purpose | Import a timetable from the school's academic system | Keep homework, exams, announcements, etc. synced into Cursimple |
| Lifecycle | Runs once per import and exits after handing over the timetable | After installation/enabling, CurSimple schedules sync; background access and sign-in validity depend on the system and platform |
| Output | Timetable | New-item notifications, due-date reminders, sidebar calendar, timetable tasks |
| Where to find | "Import from academic system", searched by school name | Components market and this catalog website, searched by name or alias |

A component package has the same layout as an import plugin (`manifest.json` + entry script + `checksums.json`); the difference is `"kind": "extension"` in its manifest.

---

## 📋 Currently Listed Components

| Component Repository | Search Aliases |
|---------------------|----------------|
| [cursimple/YuKeTang_notice_plugin](https://github.com/cursimple/YuKeTang_notice_plugin) | 雨课堂通知 / 雨课堂 / 长江雨课堂 / 黄河雨课堂 / 荷塘雨课堂 / yuketang / ykt |
| [cursimple/cursimple-notify-component](https://github.com/cursimple/cursimple-notify-component) | 多平台通知 / 通知推送 / 消息推送 / 微信通知 / QQ通知 / 飞书 / 企业微信 / 钉钉 / 邮箱通知 / Server酱 / PushPlus / WxPusher / PushDeer / Bark / notify |

> 💡 The table above is generated from [`components.json`](components.json) — do not edit it by hand. Metadata such as stars is refreshed automatically.

---

<a id="contribute"></a>

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
├── docs/                              # Website source / 组件网页
├── scripts/build_site.py              # Website bundle / 站点打包
└── LICENSE                             # MIT License
```

### How it works

1. **Registration**: components are listed in `components.json`, each as `{"repo": "owner/repo", "aliases": [...]}` (the bare `"owner/repo"` string is also accepted)
2. **Data refresh**: on every push to `main`, every 6 hours, and on manual dispatch, GitHub Actions fetches stars, description, avatar, etc. for every component and writes `components-stars.json`
3. **Publishing**: `components-stars.json` is published to the orphan branch [`component-stars-data`](https://github.com/cursimple/cursimple-components/tree/component-stars-data) (the only file on that branch), followed by a jsDelivr cache purge
4. **App consumption**: Cursimple reads `https://raw.githubusercontent.com/cursimple/cursimple-components/component-stars-data/components-stars.json`; every entry carries `"kind": "extension"` and otherwise uses the same fields as the plugin registry's `plugins-stars.json`

---

## Catalog website and deployment

The website source is in `docs/`. It supports search, aliases, real GitHub stars, repositories/releases, installation guidance and contribution links in Simplified Chinese, Traditional Chinese and English, with light/dark themes. Bundled data renders before optional online metadata refresh; network failures retain browsable content.

```bash
python3 scripts/build_site.py
node --test docs/tests/*.test.cjs
python3 -m http.server 8895 --directory build/site
```

Open `http://localhost:8895/`. The root `components.json` is authoritative and copied into the site snapshot at build time. Add `--refresh` to update public metadata. The site never asks for a GitHub token; edits and PRs use GitHub itself.

For the first deployment, set **Settings → Pages → Source** to **GitHub Actions**. Merge the website changes or manually run `Component Catalog Pages`; it verifies the site and deploys the required runtime files to `https://cursimple.github.io/cursimple-components/`. The existing metadata workflow remains independent.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## Using components

- **YuKeTang notices:** sync learning tasks and course announcements, configure new-item/deadline reminders and use supported calendars, timetable events and widgets. [Features and versions](https://github.com/cursimple/YuKeTang_notice_plugin)
- **Multi-platform notifications:** send class notices, note deadlines and component messages to WeChat, QQ, Feishu, WeCom, DingTalk, email and other channels, with recipient controls and delivery receipts. [Features and versions](https://github.com/cursimple/cursimple-notify-component)

Search and install through CurSimple's Components market, or download a component Release ZIP and use Import ZIP. Complete sign-in or notification binding, then check compatibility, account state and actual sync/delivery results in the component.

## 🔗 Related Links

- [Cursimple](https://github.com/cursimple) - Main Cursimple project
- [Import plugin registry](https://github.com/cursimple/cursimple-plugins) - Plugins that import timetables
- [Submit a component](https://github.com/cursimple/cursimple-components/edit/main/components.json) - Add your component

---

<p align="center">
  <sub>Maintained by the Cursimple team ❤️</sub>
</p>
