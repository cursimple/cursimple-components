# 🧩 Cursimple 扩展组件注册表

[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

**[English](README_EN.md)** | **中文**

> **课简（Cursimple）的官方扩展组件总仓库。**  
> 只有收录在此仓库中的组件，才会在课简的组件列表中显示。

---

## 🎯 这是什么？

这是课简的**扩展组件注册表**。所有在课简中展示的扩展组件，都需要被收录到本仓库的 [`components.json`](components.json) 文件中。

### 组件和插件有什么不同？

| | 导课插件（[cursimple-plugins](https://github.com/cursimple/cursimple-plugins)） | 扩展组件（本仓库） |
|---|---|---|
| 做什么 | 从教务系统导入课表 | 把作业、考试、公告等内容持续同步进课简 |
| 怎么跑 | 导课时跑一次，交出课表就结束 | 装好后常驻：登录一次，之后由课简在后台定时同步 |
| 产出 | 课表 | 新内容通知、截止前提醒、侧边栏日历、课表事务 |
| 在哪找 | 「从教务系统导课」按学校名搜索 | 组件列表，按组件名或别名搜索 |

组件包的结构与导课插件相同（`manifest.json` + 入口脚本 + `checksums.json`），区别在 manifest 里写的是 `"kind": "extension"`。

---

## 📋 当前收录的组件

| 组件仓库 | 搜索别名 |
|---------|---------|
| [cursimple/YuKeTang_notice_plugin](https://github.com/cursimple/YuKeTang_notice_plugin) | 雨课堂通知 / 雨课堂 / 长江雨课堂 / 黄河雨课堂 / 荷塘雨课堂 / yuketang / ykt |
| [cursimple/cursimple-notify-component](https://github.com/cursimple/cursimple-notify-component) | 多平台通知 / 通知推送 / 消息推送 / 微信通知 / QQ通知 / 飞书 / 企业微信 / 钉钉 / 邮箱通知 / Server酱 / PushPlus / WxPusher / PushDeer / Bark / notify |

> 💡 上表由 [`components.json`](components.json) 自动生成，请勿手改；星标等元数据会定期自动更新。

---

## 🤝 如何提交组件？

### 方法一：直接编辑（需协作者权限）

1. 点击 [在 GitHub 编辑 components.json](https://github.com/cursimple/cursimple-components/edit/main/components.json)
2. 在 JSON 数组中添加你的组件（格式见下方「条目格式」）
3. 提交更改

### 方法二：提交 Pull Request（推荐）

1. Fork 本仓库
2. 在 `components.json` 中添加你的组件
3. 提交 Pull Request
4. 等待审核合并

### 条目格式

推荐写成对象，并用 `aliases` 声明用户可能用来搜这个组件的词：

```json
[
  {
    "repo": "cursimple/YuKeTang_notice_plugin",
    "aliases": ["雨课堂通知", "雨课堂", "长江雨课堂", "yuketang"]
  }
]
```

仓库名多半是英文（`YuKeTang_notice_plugin`），用户搜的却是「雨课堂」，两者对不上就找不到你的组件，所以请把这些都列进 `aliases`：

- 组件的中文名：`雨课堂通知`
- 对接平台的常用叫法：`雨课堂`、`长江雨课堂`
- 拼音或英文写法：`yuketang`

匹配规则是**忽略大小写的子串匹配，前缀也算命中**。App 不做拼音转换，要支持拼音就直接把拼音写成一条别名。

为了和插件注册表通用，`schools` 键同样有效（与 `aliases` 合并去重）；条目也可以写 `"kind": "extension"`，写别的值会被拒绝。只写仓库名的格式也仍然有效：

```json
["cursimple/YuKeTang_notice_plugin"]
```

### 组件仓库要求

- 托管在 GitHub 上，且仓库公开
- 组件包的 `manifest.json` 声明 `"kind": "extension"`，与课简的插件接口兼容
- **通过 GitHub Release 发版**，最新 Release 的附件里必须有：
  - 组件包 zip，例如 `yuketang-notice-v1.0.0.zip`
  - 一个 `manifest.json`，写明 zip 的文件名和版本号：

    ```json
    {
      "filename": "yuketang-notice-v1.0.0.zip",
      "version": "v1.0.0"
    }
    ```

课简通过 `https://github.com/<owner>/<repo>/releases/latest/download/manifest.json` 找到最新版，再用其中的 `filename` 拼出下载地址。所以这个 `manifest.json`（发版用的清单）和组件包里那份 `manifest.json`（组件自身的声明）是两个文件，不要混淆；Release 也不能标成 pre-release，否则 `latest` 指不到它。

---

## 🛠️ 技术细节

### 文件结构

```
cursimple-components/
├── .github/
│   └── workflows/
│       └── update-component-stars.yml  # 生成组件清单、同步收录表的 GitHub Actions
├── components.json                     # 组件注册表（核心文件，手写）
├── fetch_component_stars.py            # 抓取组件仓库元数据的脚本
├── render_readme_table.py              # 按 components.json 生成收录表
└── LICENSE                             # MIT 许可证
```

### 工作原理

1. **组件注册**：组件信息存储在 `components.json` 中，每条为 `{"repo": "owner/repo", "aliases": [...]}` 对象（也兼容 `"owner/repo"` 纯字符串）
2. **数据更新**：`main` 有推送时、每 6 小时一次，以及手动触发时，GitHub Actions 会抓取所有组件仓库的星标、简介、头像等元数据，生成 `components-stars.json`
3. **数据发布**：`components-stars.json` 发布到孤儿分支 [`component-stars-data`](https://github.com/cursimple/cursimple-components/tree/component-stars-data)（分支里只有这一个文件），随后清一次 jsDelivr 缓存
4. **App 读取**：课简读取 `https://raw.githubusercontent.com/cursimple/cursimple-components/component-stars-data/components-stars.json`，每条都带 `"kind": "extension"`，字段与插件注册表的 `plugins-stars.json` 相同

---

## 📄 许可证

本项目基于 [MIT 许可证](LICENSE) 开源。

---

## 🔗 相关链接

- [课简（Cursimple）](https://github.com/cursimple) - 课简主项目
- [导课插件注册表](https://github.com/cursimple/cursimple-plugins) - 从教务系统导课的插件
- [提交组件](https://github.com/cursimple/cursimple-components/edit/main/components.json) - 添加你的组件

---

<p align="center">
  <sub>由课简团队维护 ❤️</sub>
</p>
