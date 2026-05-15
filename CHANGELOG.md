# 变更日志 (CHANGELOG)

本项目遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 风格,版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/) (`主版本号.次版本号.修订号`)。

> **当前阶段**: 项目处于 0.x 公测期,API / skill 命名仍可能调整;到达 v1.0.0 即视为稳定版本,后续仅在主版本升级时引入破坏性变更。

> **版本号映射说明**: 本项目早期内部迭代使用 `v1`/`v1.1`/`v1.2`/`v1.3`/`v1.4` 编号,首次对外公开发版时统一重映射为 `v0.1`/`v0.2`/`v0.3`/`v0.4`/`v0.5`,以反映"尚未到正式版"的真实成熟度。下方历史记录已按映射后版本号重写。

---

## [Unreleased]

> 待 v1.0.0 正式版前可能引入的方向: 增加退场 (Exit) 动效 / 增加更多场景 (C6 ~ C12) / 引入"过冲幅度"参数化调节 / 物理参数 spring → cubic-bezier 在线拟合工具。

---

## [0.5.0] - 2026-05

### Changed

- elegant 范式时长 `320ms → 520ms`,以加强"含蓄、舒展"的体感。
- 协议红线 (`.cursor/rules/motion.mdc`) 功能性交互动效时长上限 `> 400ms → > 600ms`,确保协议与代码一致。
- 同步更新: `miniprogram-preview/utils/catalog.js` / `miniprogram-preview/components/motion-card/motion-card.wxss` / 7 个 `docs/skills/*.md` / `scripts/gen_skills.py` / `scripts/gen_keyframes.py`。

### Added

- 项目首次对外发版,准备公开到 GitHub: `Janey-deng/wxpd-motion-mini-skills`。
- 新增 `LICENSE` (MIT) / `README.md` / `CHANGELOG.md` / `.gitignore` / `VERSION`。
- 新增 `install.sh` 一键安装脚本 (智能检测 Cursor / Claude Code / CodeBuddy)。
- 新增 `scripts/release.sh` 单人维护发版脚本。
- 在 `.cursor/rules/motion.mdc` 头部新增 "当前版本" 标注,由 release 脚本自动同步。

---

## [0.4.0] - 2026-05

### Removed

- 精简场景库,删除 5 个使用频次较低 / 缺乏强动效定义的场景:
  - C6 侧边抽屉
  - C8 Tab 内容切换
  - C9 图片懒加载
  - C11 上拉加载更多
  - C12 全屏遮罩
- 同步删除上述场景对应的 5 个 skill 文件、wxml/wxss 演示元素、keyframes。

### Result

- 保留 7 个核心场景 (C1 居中弹窗 / C2 底部抽屉 / C3 顶部 Toast / C4 列表项卡片 / C5 浮层 / C7 骨架屏 / C10 下拉刷新),共 7 个 skill。

---

## [0.3.0] - 2026-05

### Removed

- 移除"欢快 (Lively)"和"克制 (Restrained)"两种情绪范式。
- 数据层删除 `emotion` 字段。
- 首页移除"按场景 / 按情绪"切换 tab,直接按场景平铺展示。

### Changed

- 统一为 **优雅 (Elegant)** 单一范式,每场景仅保留 1 个 skill。
- 12 场景 × 1 elegant = 12 个 skill。

### Migration Note

- 如需在其他项目恢复多情绪分级,可在 `motion.mdc` 协议的 SKILL_SCHEMA 扩展字段中追加 `情绪标签: "[Lively (欢快) / Elegant (优雅) / Restrained (克制)]"`。

---

## [0.2.0] - 2026-05

### Removed

- 移除"利落 (Decisive)"情绪及对应 7 个**退场** skill (200ms 速度过快,用户难感知,体验价值低)。

### Result

- 组件库从 12 场景 + 4 情绪 + 24 skill (12 入场 + 12 退场) → 12 场景 + 3 情绪 + 19 skill (全部为入场)。

### Added

- skill 中文命名规范同步落地: `场景名 · 动作名` (例: 居中弹窗 · 缩放浮入)。

---

## [0.1.0] - 2026-05

### Added

- 项目首次发布 (内部迭代版本)。
- 12 场景 (C1 ~ C12) × 4 情绪 (利落 / 欢快 / 优雅 / 克制) = 24 skill (12 入场 + 12 退场)。
- 建立动效协议 `.cursor/rules/motion.mdc` (从 `.cursorrules` 迁移而来)。
- 建立小程序预览工程 `miniprogram-preview/` (微信原生 WebView 渲染,纯 CSS keyframes 动画)。
- 建立 spring 物理参数 → cubic-bezier 拟合算法参考 `miniprogram-preview/utils/spring2bezier.js` (RK4 数值积分)。
- 建立批量生成脚本 `scripts/gen_skills.py` / `scripts/gen_keyframes.py`。

---

## 版本号说明 (Versioning)

- **主版本号** (Major, 第 1 位): 不兼容的协议变更 / skill schema 破坏性调整。
  - 例: `motion.mdc` 的 `SKILL_SCHEMA` 必填字段从 4 个改为 5 个,或某个 skill 的命名规则发生破坏性改变。
- **次版本号** (Minor, 第 2 位): 新增 skill / 新增场景 / 新增协议条款 (向下兼容)。
  - 例: 新增"退场 (Exit) 动效"分类,旧 skill 不受影响。
- **修订号** (Patch, 第 3 位): bug 修复 / 文档完善 / 物理参数微调 (向下兼容,**不改变 skill 公开的命名与调用方式**)。
  - 例: 把某个 skill 的 overshoot 从 7% 调成 5%,但 skill ID 和调用方式不变。

> ⚠️ 在 0.x 期间,次版本号升级允许包含不兼容变更 (符合 SemVer 0.y.z 期约定); 1.0.0 之后将严格遵循语义化版本。
