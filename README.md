# motion-mini-skills

> 一套面向**微信小程序**的动效协议与 skill 库,通过 AI 提示词调用,生成具备物理质感的动画代码。

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v0.5.1-orange.svg)](CHANGELOG.md)
[![Skills](https://img.shields.io/badge/skills-6-green.svg)](docs/motion-catalog.md)
[![Stage](https://img.shields.io/badge/stage-公测中-yellow.svg)](#项目阶段)

---

## 这是什么

一份给 AI (Cursor / Claude Code / CodeBuddy / 通用 LLM) 的"动效说明书":

- **动效协议** (`.cursor/rules/motion.mdc`): 限定 AI 生成动效时必须遵守的规则 (时长红线、性能要求、合规检查)。
- **6 个 skill** (`docs/skills/*.md`): 每个 skill 一个动效场景 (居中弹窗 / 底部抽屉 / Toast / ...),包含完整 wxml + wxss 实现代码、物理参数、AI 唤醒词。
- **预览工程** (`miniprogram-preview/`): 微信开发者工具打开即可预览 6 个动效在真机上的视觉效果。

调用时不需要 npm install 或任何运行时依赖,你只需让 AI **读到这些 md 文件**,它就会按规则生成动效代码。

---

## 5 分钟接入 (按你的 IDE 选一种)

### 用法 ① · AI Prompt 直接调用 (任何 IDE / Web LLM 通用)

最通用的方式,**不需要安装任何东西**。在 Cursor / Claude Code / CodeBuddy / ChatGPT 网页版 / Gemini 等任何能拉 URL 的 AI 中,贴下面这段:

```
请遵循以下动效协议生成代码:

协议: https://raw.githubusercontent.com/Janey-deng/wxpd-motion-mini-skills/v0.5.1/.cursor/rules/motion.mdc
Skill: https://raw.githubusercontent.com/Janey-deng/wxpd-motion-mini-skills/v0.5.1/docs/skills/modal-slide-up-in-elegant.md

需求: <在这里写你的具体场景, 比如 "在 pages/order/order 页给底部确认弹窗加这个动效">
```

→ 把 `modal-slide-up-in-elegant.md` 替换成你想用的 skill 文件名 (见下方 [Skill 索引](#skill-索引))。

### 用法 ② · 一键安装到项目 (Cursor / Claude Code / CodeBuddy)

在你自己的项目根目录执行:

```bash
curl -sSL https://raw.githubusercontent.com/Janey-deng/wxpd-motion-mini-skills/v0.5.1/install.sh | bash -s v0.5.1
```

脚本会自动:

1. 把动效协议 + 6 个 skill md 复制到你项目的 `docs/motion-skills/` 目录。
2. 智能检测你的 IDE,在对应位置写一个**入口指针**:
   - 检测到 `.cursor/` → 写 `.cursor/rules/motion.mdc`
   - 检测到 `CLAUDE.md` 或 `.claude/` → 在 `CLAUDE.md` 追加引用块
   - 检测到 `.codebuddy/` → 写 `.codebuddy/rules/motion/RULE.mdc`
3. 三个 IDE 共存也兼容 (同时安装到所有检测到的位置)。

安装后在你的 AI IDE 中直接说人话即可:

```
给 pages/order 页的底部确认弹窗加一个优雅入场动效
```

AI 会自动从 `docs/motion-skills/` 找到匹配的 skill 并生成代码。

### 用法 ③ · 手动复制 (兜底)

如果你不想跑脚本,也不想拉 URL:

1. 打开本仓库 [docs/skills/](docs/skills/) 找到你要的 skill md 文件。
2. 复制整篇 md 内容 + 你的具体需求,贴到任何 AI 里。

---

## Skill 索引 (当前 main 共 6 个)

> ⚠️ **版本对齐说明**: 当前 main 分支已删除 C7 骨架屏 skill, 共 6 个; 已发布的 [v0.5.1](https://github.com/Janey-deng/wxpd-motion-mini-skills/releases/tag/v0.5.1) tag 仍包含 C7 共 7 个。下次发版时会同步删除, 届时 install.sh 拿到的也是 6 个。当前若用 v0.5.1 安装, 仍会得到 7 个 skill (含 C7)。

所有 skill 都是 **优雅 (Elegant) 入场范式**: 默认时长 520ms · 缓动曲线 `cubic-bezier(0.32, 1.18, 0.5, 1)` · 末端 ~7% 微量超越 (C1 modal / C2 actionsheet / C4 card 各有 per-skill override, 见 [docs/motion-catalog.md](docs/motion-catalog.md) §3 速查表 footnote)。

| 场景编号 | Skill ID | 场景 · 动作 | 文档 |
|---|---|---|---|
| C1  | `modal-slide-up-in-elegant`      | 居中弹窗 · 上滑浮入   | [md](docs/skills/modal-slide-up-in-elegant.md) |
| C2  | `actionsheet-slide-up-elegant`   | 底部抽屉 · 上滑展开   | [md](docs/skills/actionsheet-slide-up-elegant.md) |
| C3  | `toast-drop-in-elegant`          | 顶部 Toast · 下落出现 | [md](docs/skills/toast-drop-in-elegant.md) |
| C4  | `card-stagger-in-elegant`        | 列表项卡片 · 错位浮入 | [md](docs/skills/card-stagger-in-elegant.md) |
| C5  | `popover-anchor-in-elegant`      | 浮层 · 锚点放大       | [md](docs/skills/popover-anchor-in-elegant.md) |
| C10 | `refresh-pull-in-elegant`        | 下拉刷新 · 弹性下拉   | [md](docs/skills/refresh-pull-in-elegant.md) |

> 完整目录与场景说明见 [docs/motion-catalog.md](docs/motion-catalog.md)。

---

## 在真机上预览动效

如果你想直观看到 6 个动效在真机的效果(而不是仅看 md):

1. 安装 [微信开发者工具](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)。
2. 打开本仓库的 `miniprogram-preview/` 目录作为小程序项目。
3. 在 AppID 处选 "测试号" 即可,无需配置真实 AppID。
4. 编译运行,首页瀑布流卡片即 6 个动效,点击任意卡片进入详情页可看完整动画 + 倍速回放。

---

## 版本管理

- **当前版本**: `v0.5.1`
- **版本策略**: [语义化版本](https://semver.org/lang/zh-CN/) (0.x 公测期允许小幅调整,v1.0.0 后严格遵循)。
- **变更日志**: [CHANGELOG.md](CHANGELOG.md)
- **锁版本调用**: 所有 `install.sh` 与 raw URL 都建议带具体 tag (如 `v0.5.1`),不要用 `main` 分支,避免你的项目里的 AI 输出在我升级 skill 时突然变化。
- **升级**: 重新跑一次 `install.sh` 带新版本号即可,会覆盖旧入口指针 + 同步最新 skill 内容。
- **回滚**: 同上,带旧版本号即可。

---

## 项目阶段

⚠️ **当前 v0.5.1 是公测版本**,正式版 v1.0.0 还差几步:

- [ ] 增加退场 (Exit) 动效分类 (当前只有 6 个入场)
- [ ] 增加更多场景 (C6 / C7 / C8 / C9 / C11 / C12 等)
- [ ] 物理参数 spring → cubic-bezier 提供在线拟合工具
- [ ] 在多种真机环境下验证 60fps 稳定性

到达正式版时会在 README 与 CHANGELOG 同时标注。

---

## 反馈与建议

- 单人维护项目,迭代节奏不固定。
- 用法疑问 / 新动效需求 / Bug 反馈: 请在公司内沟通工具直接联系维护者 wxpd。
- 公开仓库不接收 PR(单人维护项目,避免 review 负担),但欢迎在 issue 里提想法。

---

## License

[MIT](LICENSE) © 2026 wxpd
