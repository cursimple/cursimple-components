(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.ComponentI18n = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  const messages = {
    'zh-CN': {
      title: '课简 · 组件收录', brand: '课简组件', app: '课简官网', plugins: '导课插件', source: '组件仓库',
      browse: '浏览组件', submit: '提交收录', eyebrow: 'CURSIMPLE COMPONENTS',
      heading: '让课简接上你的学习平台', intro: '按需安装独立组件，同步学习任务、接收课程公告，把课简提醒发送到常用平台。',
      search: '搜索名称、用途或别名', refresh: '刷新组件', loading: '正在加载组件…',
      count: '已收录 {total} 个组件', results: '找到 {count} 个组件，共收录 {total} 个',
      empty: '没有匹配的组件，试试“雨课堂”“微信”或其他关键词。', noEntries: '当前还没有收录组件。',
      failed: '暂时无法加载组件，请重试或前往组件仓库查看。', cached: '在线资料暂时不可用，正在展示已保存的收录资料。',
      repo: '查看仓库', releases: '版本与下载', stars: 'GitHub 星标', alias: '搜索别名',
      fallback: '打开仓库了解功能、安装方式与兼容版本。',
      installationTitle: '在课简中安装', installation: '打开课简的「组件」市场，搜索名称并安装。也可以从组件仓库的 Release 下载组件 ZIP，再用「导入 ZIP」安装。',
      compatibility: '安装后按组件页面完成登录或通知绑定。兼容版本以组件详情为准；后台同步和消息送达受系统、网络与平台授权影响。',
      submitTitle: '把你的组件加入收录', submitIntro: '注册表和应用市场共用 components.json。提交仓库地址与搜索别名，合并后由工作流更新收录资料。',
      edit: '在 GitHub 编辑', pullRequest: '查看贡献说明', requirements: '准备组件包',
      requirementsText: '组件包声明 kind: extension，并提供兼容的 manifest.json、入口脚本和 checksums.json。Release 附件需要同时上传组件 ZIP 与下载清单 manifest.json。',
      format: '注册条目示例', developer: '组件开发指南', privacy: '本网页用于浏览收录资料；账号登录、通知绑定和安装操作在课简或 GitHub 中完成。',
      rainName: '雨课堂通知', rainDesc: '在课简查看雨课堂作业、考试与课程公告，设置新内容和截止提醒；组件支持的任务可显示在日历、课表事务和桌面卡片中。',
      notifyName: '多平台通知', notifyDesc: '把课简的上课提醒、笔记到期和组件消息发送到微信、QQ、飞书、企业微信、钉钉、邮箱等渠道，在组件内管理目标与发送回执。',
    },
    'zh-TW': {
      title: '課簡 · 元件收錄', brand: '課簡元件', app: '課簡官網', plugins: '匯入課表外掛', source: '元件儲存庫',
      browse: '瀏覽元件', submit: '提交收錄', eyebrow: 'CURSIMPLE COMPONENTS',
      heading: '讓課簡接上你的學習平台', intro: '按需安裝獨立元件，同步學習任務、接收課程公告，把課簡提醒傳送到常用平台。',
      search: '搜尋名稱、用途或別名', refresh: '重新整理元件', loading: '正在載入元件…',
      count: '已收錄 {total} 個元件', results: '找到 {count} 個元件，共收錄 {total} 個',
      empty: '沒有符合的元件，試試「雨課堂」「微信」或其他關鍵字。', noEntries: '目前尚未收錄元件。',
      failed: '暫時無法載入元件，請重試或前往元件儲存庫查看。', cached: '線上資料暫時無法取得，正在顯示已儲存的收錄資料。',
      repo: '查看儲存庫', releases: '版本與下載', stars: 'GitHub 星標', alias: '搜尋別名',
      fallback: '開啟儲存庫了解功能、安裝方式與相容版本。',
      installationTitle: '在課簡中安裝', installation: '開啟課簡的「元件」市場，搜尋名稱並安裝。也可從元件儲存庫的 Release 下載元件 ZIP，再用「匯入 ZIP」安裝。',
      compatibility: '安裝後依元件頁面完成登入或通知綁定。相容版本以元件詳情為準；背景同步與訊息送達受系統、網路與平台授權影響。',
      submitTitle: '把你的元件加入收錄', submitIntro: '註冊表與應用程式市場共用 components.json。提交儲存庫網址與搜尋別名，合併後由工作流程更新收錄資料。',
      edit: '在 GitHub 編輯', pullRequest: '查看貢獻說明', requirements: '準備元件套件',
      requirementsText: '元件套件宣告 kind: extension，並提供相容的 manifest.json、進入點腳本與 checksums.json。Release 附件需同時上傳元件 ZIP 與下載清單 manifest.json。',
      format: '註冊項目範例', developer: '元件開發指南', privacy: '本網頁用於瀏覽收錄資料；帳號登入、通知綁定與安裝操作在課簡或 GitHub 中完成。',
      rainName: '雨課堂通知', rainDesc: '在課簡查看雨課堂作業、考試與課程公告，設定新內容與截止提醒；元件支援的任務可顯示於日曆、課表事務及桌面卡片。',
      notifyName: '多平台通知', notifyDesc: '把課簡的上課提醒、筆記到期與元件訊息傳送到微信、QQ、飛書、企業微信、釘釘、電子郵件等管道，在元件內管理目標與傳送回執。',
    },
    en: {
      title: 'CurSimple · Component catalog', brand: 'CurSimple', app: 'App website', plugins: 'Plugins', source: 'Registry',
      browse: 'Browse', submit: 'Contribute', eyebrow: 'CURSIMPLE COMPONENTS',
      heading: 'Connect your learning platforms', intro: 'Install independent components to sync learning tasks, follow course announcements and send CurSimple reminders to your preferred services.',
      search: 'Search names, features or aliases', refresh: 'Refresh components', loading: 'Loading components…',
      count: '{total} listed components', results: '{count} matches out of {total} components',
      empty: 'No matches. Try “yuketang”, “WeChat” or another keyword.', noEntries: 'No components are listed yet.',
      failed: 'Cannot load the catalog. Retry or open the component registry.', cached: 'Online metadata is unavailable. Showing the bundled catalog snapshot.',
      repo: 'Repository', releases: 'Releases', stars: 'GitHub stars', alias: 'Search aliases',
      fallback: 'Open the repository for features, installation and compatible versions.',
      installationTitle: 'Install in CurSimple', installation: 'Open the Components market in CurSimple, search by name and install. You can also download a component ZIP from its GitHub Release and use Import ZIP.',
      compatibility: 'Sign in or bind notification targets inside the component. Check its details for compatibility; background sync and delivery depend on the system, network and platform authorization.',
      submitTitle: 'List your component', submitIntro: 'The website and app market share components.json. Add your repository and search aliases; workflows update the catalog after the change is merged.',
      edit: 'Edit on GitHub', pullRequest: 'Contribution guide', requirements: 'Prepare the package',
      requirementsText: 'Declare kind: extension and include a compatible manifest.json, entry script and checksums.json. Upload both the component ZIP and download manifest.json as GitHub Release assets.',
      format: 'Registry entry example', developer: 'Component development guide', privacy: 'This page browses catalog information. Account sign-in, notification binding and installation take place in CurSimple or GitHub.',
      rainName: 'YuKeTang notices', rainDesc: 'Follow YuKeTang assignments, exams and course announcements in CurSimple. Configure new-item and deadline reminders; supported tasks can appear in calendars, timetable events and home screen widgets.',
      notifyName: 'Multi-platform notifications', notifyDesc: 'Send class reminders, note deadlines and component messages to WeChat, QQ, Feishu, WeCom, DingTalk, email and other services. Manage recipients and delivery receipts inside the component.',
    },
  };
  function normalize(value) {
    if (typeof value !== 'string') return 'zh-CN';
    value = value.replace(/_/g, '-');
    if (/^en(?:-|$)/i.test(value)) return 'en';
    if (/^zh-(?:TW|HK|MO|Hant)/i.test(value)) return 'zh-TW';
    return 'zh-CN';
  }
  function t(key, language = 'zh-CN', values = {}) {
    const text = messages[normalize(language)][key];
    if (text == null) throw new Error(`Missing translation: ${key}`);
    return text.replace(/\{(\w+)\}/g, (_, name) => String(values[name] ?? `{${name}}`));
  }
  function labels(language) {
    return {
      'cursimple/YuKeTang_notice_plugin': { name: t('rainName', language), description: t('rainDesc', language) },
      'cursimple/cursimple-notify-component': { name: t('notifyName', language), description: t('notifyDesc', language) },
    };
  }
  return { messages, normalize, t, labels };
});
