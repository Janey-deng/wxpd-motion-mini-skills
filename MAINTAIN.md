# 维护备忘录 (MAINTAIN.md)

> 这份文档是给我自己看的。不是给同事的 README,是给"半年后忘了一切的我"的求生指南。
>
> 看不懂任何东西时,**复制对应命令到终端跑就对了**。出问题先看 [📞 应急](#-应急-出问题先做什么) 一节,**别慌、别 force push**。

---

## 🎯 一句话原则

**改完东西就跑这两行存档:**

```bash
git add -A && git commit -m "改了什么"
git push
```

**满意了想发版给同事用就跑这一行:**

```bash
bash scripts/release.sh X.Y.Z   # 例如 0.6.0 / 1.0.0
```

其余命令不懂就问 AI,**千万别照搬网上的 git 教程**。

---

## 🧠 三层关系图 (理解这个就够用)

```
┌─────────────────┐
│  你的电脑        │  ← 在 Cursor 里改文件 (没人看到)
│  (Cursor 打开)  │
└────────┬────────┘
         │ git commit (打个时间戳)
         │ git push   (上传到云端)
         ▼
┌─────────────────┐
│  GitHub main    │  ← 公开可见, 同事不会主动来看
│  (你的工作云盘)   │     用来"备份 + 跨设备"
└────────┬────────┘
         │ bash scripts/release.sh X.Y.Z
         │ 网页上点 Publish
         ▼
┌─────────────────┐
│  GitHub Release │  ← 同事用 install.sh 拉的就是这一层
│  (vX.Y.Z 定版)   │     必须正式公告才有人来用
└─────────────────┘
```

- 改了**不 push** → 你一个人玩(没有备份,别这么干)
- push 了**不发 Release** → 备份了,但同事看不到(**日常状态就该这样**)
- 发 Release → 同事可以升级使用(慎重,得写 CHANGELOG)

---

## 📋 日常 5 步走 (每次打开 Cursor 之后)

### 1. 拉一下远端最新 (跨设备 / 多日没操作时必做)

```bash
git pull
```

提示 `Already up to date.` 表示本地就是最新,跳过。

### 2. 改文件 (在 Cursor 里改,边改边用微信开发者工具看效果)

### 3. 实测效果满意 (不满意就继续改)

### 4. 存档到 GitHub (本日所有改动一次性存)

```bash
git add -A
git commit -m "本次改动的简单描述"
git push
```

`commit -m "..."` 引号里写一句中文人话,例如:

- `"调整 modal 弹窗 overshoot 7% → 5%"`
- `"新增 C8 Tab 切换 skill 草稿"`
- `"修首页卡片在 iPhone 12 上的对齐问题"`

### 5. 验证云端已收到 (可选)

打开 [GitHub 仓库网页](https://github.com/Janey-deng/wxpd-motion-mini-skills),看顶部 commit 时间是不是刚才那一刻。

---

## 🚀 想发版给同事用 (从 v0.5.1 升级到 v0.6.0 / v1.0.0)

### 第 1 步:决定版本号 (看你这次改了什么类型)


| 改动类型             | 版本号怎么升      | 例子                              |
| ---------------- | ----------- | ------------------------------- |
| 大改 / 完全重做 / 公测毕业 | **主版本号 +1** | 0.5.1 → **1.0.0**;1.0.0 → 2.0.0 |
| 新增 skill / 新增场景  | **次版本号 +1** | 0.5.1 → **0.6.0**               |
| 仅修小 bug / 微调参数   | **修订号 +1**  | 0.5.1 → **0.5.2**               |


> 拿不准时直接问 AI:`"我这次改了 X 加了 Y,版本号该升到几?"`

### 第 2 步:写 CHANGELOG

打开 `CHANGELOG.md`,在 `## [Unreleased]` 下面、`## [0.5.1]` 上面,**插入一段**:

```markdown
## [X.Y.Z] - 2026-XX-XX

### Changed (改动了什么)
- 描述本次的改动

### Added (新增了什么)
- 描述本次的新增

### Fixed (修复了什么)
- 描述本次修的 bug
```

只写适用的小节(没新增就不写 `### Added` 段)。

> 拿不准怎么写:复制本次的 `git log` 给 AI,让它帮你整理。

### 第 3 步:跑发版脚本

```bash
bash scripts/release.sh X.Y.Z
```

跟着脚本提示走,它会暂停让你确认 `git diff`,**看一眼无误后回车继续**。脚本会自动:

- 改 `VERSION` → 改 `motion.mdc` 头部 → 校验 CHANGELOG 写好 → commit → 打 tag → push

### 第 4 步:网页发布 Release

脚本最后会给你一个 GitHub 链接,点进去填:


| 字段                          | 填什么                             |
| --------------------------- | ------------------------------- |
| title                       | `vX.Y.Z · 这版的简短说明`              |
| description                 | 复制 CHANGELOG 里刚写的 `[X.Y.Z]` 段内容 |
| ☑ Set as a pre-release      | 1.0.0 之前**都要勾**                 |
| ☑ Set as the latest release | 默认勾着,保持                         |


最后点 **Publish release**。

### 第 5 步:通知同事 (飞书 / 钉钉)

发这条命令给同事,让他们在自己项目根跑(把 `X.Y.Z` 换成实际版本号):

```bash
curl -sSL https://raw.githubusercontent.com/Janey-deng/wxpd-motion-mini-skills/vX.Y.Z/install.sh | bash -s vX.Y.Z
```

---

## ⛔ 4 条红线 (再忙也不要做)


| 千万别做                             | 为什么                  | 替代做法              |
| -------------------------------- | -------------------- | ----------------- |
| `git reset --hard`               | **永久丢失**改动,无法恢复      | 出问题先找 AI          |
| `git push --force`               | 覆盖云端历史,同事会受影响        | 出问题先找 AI          |
| 在 GitHub 网页上直接改文件                | 跟本地不同步,下次 push 会冲突报错 | 永远在 Cursor 本地改    |
| 删除已发布的 tag (`git tag -d v0.5.1`) | 已经在用旧版的同事会突然 404     | tag 一旦发了就**永远保留** |


---

## 📞 应急: 出问题先做什么

### 情况 1:git 报错红字一片

**先什么都别做**,截图给 AI,问 `"这个错误是什么意思,我该怎么办?"`。

**通用临时止损命令** (不会丢东西,安全):

```bash
git stash         # 把当前所有改动暂存起来 (好比 Cmd+Z 一次性撤销)
git pull          # 拉最新
git stash pop     # 把改动还原回来
```

### 情况 2:不小心 commit 了不该 commit 的东西 (但还没 push)

```bash
git reset --soft HEAD~1     # 撤销最后一次 commit, 改动还在文件里
```

⚠️ 必须确认还没 push,已经 push 了就找 AI 帮忙。

### 情况 3:不知道当前是什么状态

```bash
git status                       # 看本地状态
git log --oneline | head -5      # 看最近 5 个 commit
```

把输出截图给 AI,它能帮你判断下一步。

### 情况 4:Cursor 里 push 一直要密码 / 失败

osxkeychain 里的 PAT 可能过期(默认 90 天)。重新去 GitHub 生成 PAT,然后下次 push 时输入新 PAT 即可,系统会自动覆盖钥匙串里的旧值。

PAT 生成路径:GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token (classic) → 勾 `repo` 权限 → 复制 token。

---

## 🗺️ 找文件去哪改


| 想改什么                  | 改这个文件                                                                                                                     |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| 某个 skill 的物理参数 / 实现代码 | `docs/skills/<skill-id>.md`                                                                                               |
| 添加新 skill             | 1) 在 `docs/skills/` 加新 md 2) 在 `miniprogram-preview/utils/catalog.js` 加一条 3) 跑 `python3 scripts/gen_keyframes.py` 同步 wxss |
| 协议规则 / 时长红线           | `.cursor/rules/motion.mdc`                                                                                                |
| 首页文案 / 卡片样式           | `miniprogram-preview/pages/index/`                                                                                        |
| 详情页样式                 | `miniprogram-preview/pages/detail/`                                                                                       |
| 演示动画的 keyframes 代码    | `miniprogram-preview/components/motion-card/motion-card.wxss` 末尾 (建议改 docs/skills 后跑生成脚本同步)                               |
| 给同事看的接入说明             | `README.md`                                                                                                               |
| 同事 install 后看到的入口指针文案 | `install.sh` 中的 `make_entry_body` 函数                                                                                      |


> 拿不准在哪个文件:让 AI 帮你找,`"我想改 X,该改哪个文件?"`

---

## 🤖 跟 AI 协作的几个万能问法

- `"我这一步是不是该 commit?"` → 让 AI 看你的 git status 帮你判断
- `"这个红字是什么意思,我现在该怎么办?"` → 复制报错全文
- `"看下我这版 CHANGELOG 有没有写漏什么"` → 复制你写的 changelog 段落
- `"我加了 X 改了 Y,版本号该升到几?"` → 描述本次改动
- `"帮我重新跑一遍发版流程"` → AI 会带你走 release.sh

---

## 🔚 最后:我现在的版本是多少?

直接跑:

```bash
cat VERSION
```

或者打开 GitHub 仓库的 [Releases 页](https://github.com/Janey-deng/wxpd-motion-mini-skills/releases) 看最新一条。

---

> 写于 v0.5.1 发版时 · 后续版本可以增补,但**核心三层关系图永远不变**。

