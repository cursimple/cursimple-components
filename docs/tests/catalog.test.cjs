const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const catalog = require('../catalog.js');
const i18n = require('../i18n.js');

test('registry keeps aliases and schools, supports legacy strings and deduplicates repositories', () => {
  const values = catalog.parseRegistry([{ repo: 'cursimple/Example', aliases: ['课程', '课程'], schools: ['长大'] }, 'cursimple/example']);
  assert.equal(values.length, 1);
  assert.deepEqual(values[0].aliases, ['课程', '长大']);
});

test('unsafe repository paths and the wrong component kind are refused', () => {
  for (const repo of ['https://example.com', 'owner/../private', 'owner/..', 'owner/<script>']) assert.throws(() => catalog.parseRegistry([repo]));
  assert.throws(() => catalog.parseRegistry([{ repo: 'owner/repo', kind: 'plugin' }]));
});

test('search matches aliases, descriptions and localized labels without requiring online metadata', () => {
  const entries = catalog.parseRegistry([{ repo: 'cursimple/YuKeTang_notice_plugin', aliases: ['雨课堂', 'ykt'] }, { repo: 'cursimple/cursimple-notify-component', aliases: ['微信通知', 'notify'] }]);
  assert.equal(catalog.search(entries, 'YKT').length, 1);
  assert.equal(catalog.search(entries, '微信').length, 1);
  assert.equal(catalog.search(entries, 'WeChat', new Map(), i18n.labels('en'))[0].repo, entries[1].repo);
  assert.equal(catalog.search(entries, 'missing').length, 0);
});

test('metadata preserves a real zero star count and rejects unsafe avatar URLs', () => {
  const data = catalog.parseMetadata({ repositories: [{ name: 'cursimple/example', star: 0, avatar: 'javascript:alert(1)' }] });
  assert.equal(data.get('cursimple/example').stars, 0);
  assert.equal(data.get('cursimple/example').avatar, null);
  assert.equal(catalog.safeAvatar('https://untrusted.example/photo'), null);
  assert.ok(catalog.safeAvatar('https://avatars.githubusercontent.com/u/1'));
});

test('all language keys and interpolation parameters agree and HTML references are translated', () => {
  const keys = Object.keys(i18n.messages['zh-CN']).sort();
  for (const language of ['zh-CN', 'zh-TW', 'en']) {
    assert.deepEqual(Object.keys(i18n.messages[language]).sort(), keys);
    for (const key of keys) {
      assert.ok(i18n.messages[language][key]);
      assert.deepEqual(i18n.messages[language][key].match(/\{\w+\}/g), i18n.messages['zh-CN'][key].match(/\{\w+\}/g));
    }
  }
  const html = fs.readFileSync(path.join(__dirname, '../index.html'), 'utf8');
  for (const match of html.matchAll(/data-i18n="([^"]+)"/g)) assert.ok(keys.includes(match[1]));
});

test('packaged registry matches the app registry and optional metadata can omit new entries', () => {
  const original = JSON.parse(fs.readFileSync(path.join(__dirname, '../../components.json'), 'utf8'));
  const bundled = JSON.parse(fs.readFileSync(path.join(__dirname, '../data/components.json'), 'utf8'));
  assert.deepEqual(bundled, original);
  assert.ok(catalog.parseRegistry(bundled).length > 0);
  const emptyMetadata = catalog.parseMetadata({ repositories: [] });
  assert.equal(catalog.search(catalog.parseRegistry(bundled), '', emptyMetadata).length, bundled.length);
});
