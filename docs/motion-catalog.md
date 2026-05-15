# 微信小程序动效目录 (Motion Catalog)

> 一份给**设计师 + 前端开发**协同使用的动效查阅手册。
> 把"我想要那种从底部弹起来一点点回弹的感觉"翻译成可执行的物理参数 + 代码 + AI 唤醒词。

---

## 0. 文档定位

| 项 | 说明 |
| --- | --- |
| 适用平台 | 微信小程序 (原生 WebView 渲染) |
| 适用角色 | 设计师 / 前端 / AI 辅助开发用户 |
| 与 [.cursor/rules/motion.mdc](../.cursor/rules/motion.mdc) 关系 | 本目录是协议的**实例化产物**;motion.mdc 定义"该怎么做",本文件给"具体的 6 套答案" |
| 不是什么 | 不是组件库 API 文档;不是性能调优手册;不是 iOS/Android 系统动效完整对照表 |
| 版本 | v1.5 (2026-05) |

### 怎么读这份文档

- **赶时间** -> 直接跳到 [3. 场景速查表](#3-场景速查表),按场景找到对应 skill 链接
- **想理解为什么这样设计** -> 先看 [2. 优雅范式](#2-优雅范式)
- **想自己加一条新动效** -> 读 [4. 自定义动效的 4 步流程](#4-自定义动效的-4-步流程)

---

## 1. 微信小程序常见动效场景清单 (6 个核心场景)

本期只实现**入场动效**。退场关键词作为设计概念保留(见下表"退场关键词"列),后续版本补充实现。交互反馈类(按钮按压、长按、Tab indicator 滑动)不在本期范围。

| 编号 | 场景 | UI 锚点 (在哪里出现) | 典型用法 | 入场关键词 | 退场关键词 |
| --- | --- | --- | --- | --- | --- |
| C1 | 居中弹窗 (Modal) | 屏幕中心 | 二次确认、表单弹层 | 上滑浮入 | 缩放消散 |
| C2 | 底部抽屉 (ActionSheet) | 屏幕底边 | 操作菜单、分享面板 | 上滑展开 | 下滑收起 |
| C3 | 顶部 Toast | 屏幕顶边 | 操作反馈、轻提示 | 下落出现 | 上抬消失 |
| C4 | 列表项卡片 | 列表容器内 | 信息流、商品卡 | 错位浮入 (stagger) | 横滑移除 |
| C5 | 浮层 Popover/Tooltip | 锚定元素附近 | 引导、提示气泡 | 锚点放大 | 锚点缩回 |
| C10 | 下拉刷新指示器 | 列表顶部 | 刷新数据 | 弹性下拉 | 回缩消失 |

> 编号沿用 v1 的 C1-C12 系列;v1.3 保留 C1/C2/C3/C4/C5/C7/C10 共 7 个;v1.5 删除 C7 (应用场景不多), 当前共 6 个核心场景。

---

## 2. 优雅范式

参考 iOS HIG 的 motion 章节 + Material Motion 的 emphasis 分级,本期仅实现一种统一的入场体感 —— **优雅 (Elegant)**。

### 2.1 体感关键词

```
        缓入缓出 + 末端 ~7% 微量超越
        ────────────────────────────
            体感 "呼吸感"
        含蓄、有礼貌、不打扰
```

### 2.2 物理参数

| 体感关键词 | 物理逻辑 | 推荐曲线/参数 | 推荐时长 | 适用产品 / 场景 |
| --- | --- | --- | --- | --- |
| 缓入缓出、微量超越、含蓄 | 弹簧高张力中摩擦;末端 ~5-8% 超越 | `spring(1, 220, 18)` 拟合 = `cubic-bezier(0.32, 1.18, 0.5, 1)` | 520ms | 阅读、零售、内容平台、生活方式品牌、企业 SaaS、严肃通知 |

### 2.3 为什么只保留优雅

- **欢快 (Lively, 360ms + ~20% 超越)** 偏娱乐 / 营销,弹跳感强,**通用性弱**;若产品需要,从优雅范式手工改 spring 张力即可。
- **克制 (Restrained, 240ms 无超越)** 偏严肃 / 工具,体感"按部就班",**辨识度弱**;在小程序常见场景中,优雅范式同样能胜任绝大多数严肃通知。
- **保留单一范式** = 设计师不需要在 3 个候选中犹豫,前端不需要为同一组件维护 2-3 套 keyframes;**降低协作熵**比覆盖更多情绪更重要。

> 与 [.cursor/rules/motion.mdc](../.cursor/rules/motion.mdc) 第 3 节"入场强调生长感"完全一致。
> v1.2 移除了"欢快 (Lively)"和"克制 (Restrained)"两种情绪,组件库统一为优雅 (Elegant) 单一范式。

---

## 3. 场景速查表

每行的值是 `<场景缩写>-<动作>-elegant`,点击跳转到对应 skill 文档。

| 场景 | 入场 Skill |
| --- | --- |
| C1 居中弹窗 | [modal-slide-up-in-elegant](skills/modal-slide-up-in-elegant.md) ★ |
| C2 底部抽屉 | [actionsheet-slide-up-elegant](skills/actionsheet-slide-up-elegant.md) ★ |
| C3 顶部 Toast | [toast-drop-in-elegant](skills/toast-drop-in-elegant.md) |
| C4 列表项卡片 | [card-stagger-in-elegant](skills/card-stagger-in-elegant.md) ★ |
| C5 浮层 | [popover-anchor-in-elegant](skills/popover-anchor-in-elegant.md) |
| C10 下拉刷新 | [refresh-pull-in-elegant](skills/refresh-pull-in-elegant.md) |

入场小计: **6 个 skill**

> ★ 标记的 skill 有 per-skill duration override / curve override / 组合动画 orchestration:
>
> - `card-stagger-in-elegant`: 单卡 duration override 至 **600ms** (远低于 1000ms 红线);
>   因 6 卡 stagger 总入场需要更舒展的"呼吸感", 总入场 = 600 + 5×60 = 900ms。
> - `modal-slide-up-in-elegant`: modal 自身 **480ms** + 显式过冲 8rpx + curve override
>   `cubic-bezier(0.4, 0, 0.2, 1)` (ease-in-out, 不带隐式 overshoot, 让 keyframe 8rpx 过冲独立可控);
>   3 帧 keyframe (`+24rpx → 60% 过冲到 -8rpx → 100% 回正`); 配合 orchestration
>   { maskDuration: 200, mainDelay: 180 } 形成"遮罩 90% → modal 启动"组合动画;
>   总入场 = 0.9 × 200 + 480 = **660ms** (modal 自身 480ms 仍合规 ≤ 1000ms)。
> - `actionsheet-slide-up-elegant`: sheet 自身 **420ms** + 默认 `ELEGANT_CURVE`;
>   2 帧 keyframe (`100% → 0%` translateY); 同款 orchestration { 200, 180 };
>   总入场 = 0.9 × 200 + 420 = **600ms**。
>
> C1 / C2 共享 mask + mainDelay timing (200/180), 但主动作各自 480/420ms, 节奏略有差异
> (C1 含过冲略弹性, C2 平滑收尾)。范式默认仍为 520ms + `ELEGANT_CURVE`,
> 仅以上 3 个 skill 做 per-skill override (见 `catalog.js` / `gen_skills.py` / `gen_keyframes.py`
> 中的 `DURATION_OVERRIDES` / `CURVE_OVERRIDES`)。

### 3.1 退场矩阵

> v1.1 已移除原"利落 (Decisive)"7 个退场 skill (200ms 速度过快、用户难感知)。后续版本将基于优雅范式重新设计退场动效。

### 3.2 总计

**6 个 skill** (全部入场, 全部 elegant) + 1 份目录文档 (本文件)。

---

## 4. 自定义动效的 4 步流程

如果速查表里没有你需要的场景(例如"长按弹出菜单"、"答题正确反馈"),按以下流程自建,然后回灌到本目录:

1. **判定场景类型** -> 是入场 / 退场 / 反馈?(反馈类目前不在本目录,需另起 catalog)
2. **选取参考 skill** -> 从 [3. 场景速查表](#3-场景速查表)取一个最像的 skill 作为起点,复制到 `docs/skills/<新名字>-elegant.md`,改造代码
3. **保持 elegant 范式** -> 时长 520ms + `cubic-bezier(0.32, 1.18, 0.5, 1)` (除非有明确产品理由覆盖)
4. **跑自查报告** (motion.mdc 第 7.1 节四字段),确认无超时、无重排、有合成层

---

## 5. 命名规范

```
<场景缩写>-<动作>-elegant.md

场景缩写: modal / actionsheet / toast / card / popover / refresh

动作:    slide-up-in / slide-up / drop-in / stagger-in / anchor-in / pull-in
```

例:
- `modal-slide-up-in-elegant.md` = 居中弹窗 · 上滑浮入 · 优雅
- `toast-drop-in-elegant.md` = 顶部 Toast · 下落出现 · 优雅

> v1.2 起,后缀固定为 `-elegant` (本期单一范式)。未来若新增情绪,沿用 v1 的 `<场景>-<动作>-<情绪>` 三段式命名。

---

## 6. 物理参数到 CSS 的换算

elegant 范式下 spring 物理已预拟合为单一 cubic-bezier,无需运行时换算。本表列出参考关系备查 (见 [miniprogram-preview/utils/spring2bezier.js](../miniprogram-preview/utils/spring2bezier.js)):

| spring 参数 | 对应 cubic-bezier | overshoot | 推荐 duration |
| --- | --- | --- | --- |
| `(1, 220, 18)` | `cubic-bezier(0.32, 1.18, 0.5, 1)` | ~7% | **520ms (本期 elegant 范式)** |

> 如果需要更弹/更克制的体感,可参考 spring2bezier.js 重新拟合,但不属于本期 catalog 范围。

---

## 7. 变更日志

| 版本 | 日期 | 变更 |
| --- | --- | --- |
| v1   | 2026-05 | 首次发布,12 场景 + 4 情绪 + 24 skill |
| v1.1 | 2026-05 | 移除"利落 (Decisive)"情绪及对应 7 个退场 skill (200ms 速度过快、用户难感知);组件库变为 12 场景 + 3 情绪 + 19 skill (全部入场)。skill 中文命名规范同步落地 |
| v1.2 | 2026-05 | 移除"欢快 (Lively)"和"克制 (Restrained)"两种情绪;统一为**优雅 (Elegant)** 单一范式;每场景 1 个 skill,共 12 个 skill;首页移除"按场景/按情绪"切换 tab,直接按场景平铺;数据层删除 emotion 字段 |
| v1.3 | 2026-05 | 精简场景库,删除 C6 侧边抽屉 / C8 Tab 内容 / C9 图片懒加载 / C11 上拉加载 / C12 全屏遮罩 五个场景及对应 skill;保留 7 个核心场景 (C1/C2/C3/C4/C5/C7/C10),共 7 个 skill |
| v1.4 | 2026-05 | elegant 范式时长 320ms → **520ms**,以加强"含蓄、舒展"的体感;motion.mdc 红线 `> 400ms` 同步放宽至 `> 600ms`,确保协议与代码一致。同步更新 catalog.js / motion-card.wxss / 7 个 skill 文档 / 生成脚本 |
| v1.5 | 2026-05 | C1 modal: 缩放浮入 → 上滑浮入 (重命名 `modal-slide-up-in-elegant`) + 显式过冲 8rpx + curve override;C2 actionsheet + C1 modal 新增 orchestration (mask 200ms + mainDelay 180ms);删除 C7 骨架屏切内容 (应用场景不多);motion.mdc 红线 `> 600ms` 同步放宽至 `> 1000ms`;当前共 6 个场景 / 6 个 skill |
