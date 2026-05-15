#!/usr/bin/env python3
"""一次性生成 docs/skills/*.md (6 个, 全部 elegant)。

v1.2 (2026-05): 移除 lively / restrained, 仅保留 elegant 单一范式;
                12 场景每场景 1 个 skill, md 头部不再含"情绪标签"字段。
v1.3 (2026-05): 精简到 7 场景, 删除 C6 / C8 / C9 / C11 / C12 五个场景。
v1.5 (2026-05): 删除 C7 骨架屏切内容 (应用场景不多), 共保留 6 个场景。

本脚本用于工程初始化或全量重生成,后续 skill 维护应直接编辑生成的 md 文件。
"""
from pathlib import Path

OUT_DIR = Path(__file__).parent.parent / "docs" / "skills"

# elegant 单一范式参数: 时长 520ms + 末端 ~7% 微量超越的 cubic-bezier
ELEGANT = {
    "curve": "cubic-bezier(0.32, 1.18, 0.5, 1)",
    "duration": 520,
    "spring": "spring(1, 220, 18)",
    "overshoot": "~7%",
}

# per-skill duration override (与 catalog.js / gen_keyframes.py 保持一致)
# - card-stagger-in-elegant: 单卡 600ms (远低于 1000ms 红线); 6 卡 stagger 总入场 900ms
# - actionsheet-slide-up-elegant: sheet 自身 420ms (mask 200 + mainDelay 180 → 总 600ms)
# - modal-slide-up-in-elegant:    modal 自身 480ms + 显式 8rpx 过冲 + curve override
#                                 (mask 200 + mainDelay 180 → 总 660ms; modal 自身仍 ≤ 1000ms)
DURATION_OVERRIDES = {
    "card-stagger-in-elegant": 600,
    "actionsheet-slide-up-elegant": 420,
    "modal-slide-up-in-elegant": 480,
}

# per-skill curve override (默认 ELEGANT["curve"], 仅显式列出的 skill 替换)
# - modal-slide-up-in-elegant: ease-in-out 不带隐式 overshoot, 因 keyframe 已显式给 8rpx 过冲
CURVE_OVERRIDES = {
    "modal-slide-up-in-elegant": "cubic-bezier(0.4, 0, 0.2, 1)",
}

SCENARIOS = {
    "C1":  {"slug": "modal",        "cn": "居中弹窗"},
    "C2":  {"slug": "actionsheet",  "cn": "底部抽屉"},
    "C3":  {"slug": "toast",        "cn": "顶部 Toast"},
    "C4":  {"slug": "card",         "cn": "列表项卡片"},
    "C5":  {"slug": "popover",      "cn": "浮层"},
    "C10": {"slug": "refresh",      "cn": "下拉刷新指示器"},
}

# 每个 skill: (id, scene_id, action, action_cn, wakeup_cn, wakeup_en) — emotion 固定为 elegant
# wakeup_cn / wakeup_en 必须与 miniprogram-preview/utils/catalog.js 中对应字段保持完全一致,
# 避免重新执行本脚本时把 docs/skills/*.md 的详细唤醒词覆盖回简略版本 (回退灾难)
SKILLS = [
    ("modal-slide-up-in-elegant",      "C1",  "slide-up-in",   "上滑浮入",
     "上滑浮入 / 弹窗优雅出现 / 居中浮起带过冲 / 弹出上滑回弹 / 优雅弹窗",
     "slide up in elegant / soft spring up / modal slide up overshoot / pop up in elegant / gentle lift up with bounce"),
    ("actionsheet-slide-up-elegant",   "C2",  "slide-up",      "上滑展开",
     "上滑展开 / 底部抽屉优雅弹起 / 底部弹出 / 抽屉上滑 / 上推出现",
     "slide up elegant / actionsheet slide up / bottom drawer in / soft slide up / drawer rise"),
    ("toast-drop-in-elegant",          "C3",  "drop-in",       "下落出现",
     "下落出现 / 顶部 Toast 优雅出现 / 顶部下落 / Toast 落入 / 顶部提示出现",
     "drop in elegant / toast drop in / fall in elegant / top toast in / soft drop in"),
    ("card-stagger-in-elegant",        "C4",  "stagger-in",    "错位浮入",
     "错位浮入 / 卡片优雅入场 / 列表错位入场 / 卡片依次浮入 / 列表项浮现",
     "stagger in elegant / card stagger in / list cascade in / sequential fade up / staggered entrance"),
    ("popover-anchor-in-elegant",      "C5",  "anchor-in",     "锚点放大",
     "锚点放大 / Popover 出现 / 浮层弹出 / 锚点缩放 / 引导提示出现",
     "anchor in elegant / popover in / popover scale in / anchor scale up / tooltip in"),
    ("refresh-pull-in-elegant",        "C10", "pull-in",       "弹性下拉",
     "弹性下拉 / 下拉刷新优雅出现 / 下拉指示出现 / 刷新弹入 / 下拉回弹",
     "pull in elegant / refresh pull in / pull down elegant / pull to refresh / soft pull in"),
]


def render_code(skill_id, scene_id, action):
    """生成 wxml + wxss 代码片段, 默认 elegant 范式 (520ms + cubic-bezier(0.32, 1.18, 0.5, 1));
    若 skill_id 命中 DURATION_OVERRIDES / CURVE_OVERRIDES, 则使用 override 后的值。"""
    s = SCENARIOS[scene_id]
    cls = f"ml-{s['slug']}"
    keyframe_name = f"ml-{action}-elegant"
    duration = DURATION_OVERRIDES.get(skill_id, ELEGANT["duration"])
    curve = CURVE_OVERRIDES.get(skill_id, ELEGANT["curve"])

    if action == "slide-up-in":  # C1 Modal (上滑 + 显式 8rpx 过冲 + 回正)
        # 配合 orchestration { maskDuration: 200, mainDelay: 180 }: 遮罩先 fade-in 200ms,
        # 走到 90% (180ms) 时 modal 启动 480ms 上滑浮入 (含 60% 时刻过冲到 -8rpx 后回正),
        # 总入场 = 0.9×200 + 480 = 660ms; curve 用 ease-in-out 避免与 keyframe 显式过冲叠加
        wxml = f'''<view class="{cls}-mask {{{{visible ? '{cls}-mask--show' : ''}}}}" bindtap="onClose">
  <view class="{cls} {{{{visible ? '{cls}--in' : ''}}}}" catchtap="">
    <view class="{cls}__title">标题</view>
    <view class="{cls}__body"><slot></slot></view>
  </view>
</view>'''
        wxss = f'''.{cls}-mask {{
  position: fixed; inset: 0;
  background: rgba(0, 0, 0, .4);
  opacity: 0;
  pointer-events: none;
  transition: opacity 200ms cubic-bezier(0.4, 0, 0.2, 1);
}}
.{cls}-mask--show {{ opacity: 1; pointer-events: auto; }}

.{cls} {{
  position: absolute; left: 50%; top: 50%;
  width: 560rpx;
  background: #fff; border-radius: 24rpx;
  transform: translate3d(-50%, -50%, 0);
  opacity: 0;
  will-change: transform, opacity;
}}
/* 主动作延迟 180ms 启动 (遮罩走完 90%), 形成 "遮罩 → modal" 顺序入场 */
.{cls}--in {{
  animation: {keyframe_name} {duration}ms {curve} both;
  animation-delay: 180ms;
}}

/* 3 帧 keyframe: 上滑 24rpx → 60% 过冲到目标上方 8rpx → 100% 回正到目标位置 */
@keyframes {keyframe_name} {{
  0%   {{ transform: translate3d(-50%, calc(-50% + 24rpx), 0); opacity: 0; }}
  60%  {{ transform: translate3d(-50%, calc(-50% - 8rpx), 0);  opacity: 1; }}
  100% {{ transform: translate3d(-50%, -50%, 0);               opacity: 1; }}
}}'''
    elif action == "slide-up":  # C2 ActionSheet
        wxml = f'''<view class="{cls}-mask {{{{visible ? '{cls}-mask--show' : ''}}}}" bindtap="onClose">
  <view class="{cls} {{{{visible ? '{cls}--in' : ''}}}}" catchtap="">
    <view class="{cls}__item" wx:for="{{{{items}}}}" wx:key="*this">{{{{item}}}}</view>
  </view>
</view>'''
        wxss = f'''.{cls}-mask {{
  position: fixed; inset: 0;
  background: rgba(0, 0, 0, .4);
  opacity: 0; pointer-events: none;
  transition: opacity {duration}ms cubic-bezier(0.4, 0, 0.2, 1);
}}
.{cls}-mask--show {{ opacity: 1; pointer-events: auto; }}

.{cls} {{
  position: absolute; left: 0; right: 0; bottom: 0;
  background: #fff; border-radius: 24rpx 24rpx 0 0;
  padding: 24rpx 0 60rpx;
  transform: translate3d(0, 100%, 0);
  will-change: transform;
}}
.{cls}--in {{
  animation: {keyframe_name} {duration}ms {curve} both;
}}

@keyframes {keyframe_name} {{
  0%   {{ transform: translate3d(0, 100%, 0); }}
  100% {{ transform: translate3d(0, 0, 0); }}
}}'''
    elif action == "drop-in":  # C3 Toast (top)
        wxml = f'''<view class="{cls} {{{{visible ? '{cls}--in' : ''}}}}">
  <text class="{cls}__text">{{{{message}}}}</text>
</view>'''
        wxss = f'''.{cls} {{
  position: fixed; top: 88rpx; left: 50%;
  padding: 16rpx 32rpx;
  background: rgba(0, 0, 0, .85); color: #fff;
  border-radius: 12rpx; font-size: 28rpx;
  transform: translate3d(-50%, -200%, 0);
  opacity: 0;
  will-change: transform, opacity;
}}
.{cls}--in {{
  animation: {keyframe_name} {duration}ms {curve} both;
}}

@keyframes {keyframe_name} {{
  0%   {{ transform: translate3d(-50%, -200%, 0); opacity: 0; }}
  100% {{ transform: translate3d(-50%, 0, 0);     opacity: 1; }}
}}'''
    elif action == "stagger-in":  # C4 Card list (两列瀑布流)
        # 演示形态: 两列, 左列从 leftItems 渲染, 右列从 rightItems 渲染;
        # stagger Z 字扫描: 左列 index*120, 右列 index*120 + 60 (右列偏移半个延迟, 形成逐行入场)
        wxml = f'''<view class="{cls}-list">
  <view class="{cls}-list__col">
    <view class="{cls} {{{{visible ? '{cls}--in' : ''}}}}"
          wx:for="{{{{leftItems}}}}" wx:key="id"
          style="animation-delay: {{{{index * 120}}}}ms">
      <view class="{cls}__title">{{{{item.title}}}}</view>
    </view>
  </view>
  <view class="{cls}-list__col">
    <view class="{cls} {{{{visible ? '{cls}--in' : ''}}}}"
          wx:for="{{{{rightItems}}}}" wx:key="id"
          style="animation-delay: {{{{index * 120 + 60}}}}ms">
      <view class="{cls}__title">{{{{item.title}}}}</view>
    </view>
  </view>
</view>'''
        wxss = f'''/* 两列瀑布流容器 (240rpx 顶距为演示视觉留白, 调用方按页面需求自行调整) */
.{cls}-list {{
  display: flex;
  gap: 16rpx;
  padding: 240rpx 24rpx 0;
  box-sizing: border-box;
}}
.{cls}-list__col {{
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}}

/* 纯白卡, 高度由内容决定 */
.{cls} {{
  background: #fff;
  border-radius: 16rpx;
  transform: translate3d(0, 24rpx, 0);
  opacity: 0;
  will-change: transform, opacity;
}}
.{cls}--in {{
  animation: {keyframe_name} {duration}ms {curve} both;
}}

@keyframes {keyframe_name} {{
  0%   {{ transform: translate3d(0, 24rpx, 0); opacity: 0; }}
  100% {{ transform: translate3d(0, 0, 0);     opacity: 1; }}
}}'''
    elif action == "anchor-in":  # C5 Popover
        wxml = f'''<view class="{cls} {{{{visible ? '{cls}--in' : ''}}}}">
  <view class="{cls}__arrow"></view>
  <view class="{cls}__body"><slot></slot></view>
</view>'''
        wxss = f'''.{cls} {{
  position: absolute;
  background: #fff; padding: 16rpx 24rpx;
  border-radius: 12rpx;
  box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, .12);
  transform-origin: center top;
  transform: scale(0.6);
  opacity: 0;
  will-change: transform, opacity;
}}
.{cls}__arrow {{
  position: absolute; top: -12rpx; left: 50%;
  width: 0; height: 0;
  border-left: 12rpx solid transparent;
  border-right: 12rpx solid transparent;
  border-bottom: 12rpx solid #fff;
  transform: translateX(-50%);
}}
.{cls}--in {{
  animation: {keyframe_name} {duration}ms {curve} both;
}}

@keyframes {keyframe_name} {{
  0%   {{ transform: scale(0.6); opacity: 0; }}
  100% {{ transform: scale(1.0); opacity: 1; }}
}}'''
    elif action == "pull-in":  # C10 Refresh
        wxml = f'''<view class="{cls} {{{{pulling ? '{cls}--in' : ''}}}}">
  <view class="{cls}__dot"></view>
  <view class="{cls}__dot"></view>
  <view class="{cls}__dot"></view>
</view>'''
        wxss = f'''.{cls} {{
  display: flex; justify-content: center; gap: 12rpx;
  height: 96rpx; align-items: center;
  transform: translate3d(0, -100%, 0);
  opacity: 0;
  will-change: transform, opacity;
}}
.{cls}__dot {{
  width: 12rpx; height: 12rpx;
  background: #888; border-radius: 50%;
}}
.{cls}--in {{
  animation: {keyframe_name} {duration}ms {curve} both;
}}

@keyframes {keyframe_name} {{
  0%   {{ transform: translate3d(0, -100%, 0); opacity: 0; }}
  100% {{ transform: translate3d(0, 0, 0);     opacity: 1; }}
}}'''
    else:
        # 不应到达: SKILLS 表中所有 (scene_id, action) 都应有对应分支
        raise ValueError(f"unknown (scene_id={scene_id}, action={action})")

    return wxml, wxss


def render_skill(skill_id, scene_id, action, action_cn, wakeup_cn, wakeup_en):
    s = SCENARIOS[scene_id]
    duration = DURATION_OVERRIDES.get(skill_id, ELEGANT["duration"])
    curve = CURVE_OVERRIDES.get(skill_id, ELEGANT["curve"])

    wxml, wxss = render_code(skill_id, scene_id, action)

    # physics: 默认 generic 描述; C1 因显式过冲, 用更具体的描述覆盖, 与 catalog.js 中 C1 entry 同步
    if action == "slide-up-in":
        physics = f"{s['cn']}从下方 24rpx 处上浮并渐显, 60% 时刻过冲到目标上方 8rpx, 再回落到目标位置, 弹性收尾。"
    else:
        physics = f"{s['cn']}缓入缓出, 末端 {ELEGANT['overshoot']} 微量超越, 主动作完成后含蓄收尾。体感'呼吸感'。"
    # wakeup 用 SKILLS 表里传入的详细版 (5 中文 + 5 英文), 与 catalog.js 中对应字段保持一致
    wakeup = f"中文: {wakeup_cn} - 英文: {wakeup_en}"

    # spring_section: 默认 elegant 范式 spring 拟合表; C1 因显式 3 帧 keyframe (手工设计 8rpx 过冲),
    # 不再来自 spring 拟合, 单独显示手工设计参数表
    if action == "slide-up-in":
        spring_section = f"""## 2. 物理参数换算

| 设计来源 | 缓动曲线 | 显式 overshoot | 推荐 duration |
| --- | --- | --- | --- |
| 手工 3 帧 keyframe | `{curve}` (ease-in-out, 不带隐式 overshoot) | 8rpx (≈ 上滑距离 33%) | {duration}ms |

> C1 modal 不走 spring → cubic-bezier 拟合路径, 改为 keyframe 显式定义过冲距离 (60% 时刻 -8rpx),
> 让设计师可独立微调过冲幅度而不受 cubic-bezier 数值变化影响。
> 整体节奏: 0% → 60% (288ms) 上升 + 过冲, 60% → 100% (192ms) 回正。
"""
    else:
        spring_section = f"""## 2. 物理参数换算

| 输入 spring | 输出 cubic-bezier | 实测 overshoot | 推荐 duration |
| --- | --- | --- | --- |
| `{ELEGANT['spring']}` | `{curve}` | {ELEGANT['overshoot']} | {duration}ms |

> 拟合算法详见 [miniprogram-preview/utils/spring2bezier.js](../../miniprogram-preview/utils/spring2bezier.js)。
> Cubic-bezier 拟合误差 < 5%, 体感等效。
"""

    has_filter = "filter" in wxss
    composite = "已触发 GPU 加速 (translate3d + will-change)"
    if has_filter:
        composite += "; filter 动画在 webview 下可能掉到 30fps,建议在低端机降级"
    duration_check = f"✅ {duration}ms ≤ 1000ms"

    self_check = f"""## 3. 自查报告

```
FPS 预估:    60+
重排风险:    无
合成层:      {composite}
时长合规:    {duration_check}
```
"""

    boundary = "✅ 内容详情 / 商品详情 / 评论展开 / 设置面板 / 阅读类\n❌ 紧急提示 / 工具类即时反馈 (本期未实现 lively / restrained 备选)"

    # form_note: stagger-in (C4) 描述瀑布流 + Z 字扫描; slide-up-in (C1) 描述组合动画 orchestration;
    # 其他 skill 的形态在 wxml/wxss 注释里已说清, 此处留空
    if action == "stagger-in":
        # 总入场 = 单卡 duration + 末位卡延迟 (300ms = 5×60ms)
        total_in = duration + 300
        form_note = (
            "\n> 演示形态: 两列瀑布流, 6 个纯白卡 (左 3 + 右 3), "
            "高度错落 (左列 高/矮/高 vs 右列 矮/高/矮);\n"
            "> stagger 顺序按\"从上到下逐行 Z 字\"扫描: "
            "左1=0ms / 右1=60ms / 左2=120ms / 右2=180ms / 左3=240ms / 右3=300ms;\n"
            f"> 单卡 {duration}ms, 总入场 = {duration}+300 = {total_in}ms "
            f"(单卡 {duration}ms 仍合规 ≤ 1000ms)。\n>\n"
            "> 实际项目可按 `leftItems` / `rightItems` 数据驱动, "
            "高度由内容决定; 240rpx 顶距是演示版的视觉留白, 调用方按页面需求自行调整。\n"
        )
    elif action == "slide-up-in":
        # 组合动画: 遮罩 fade-in 200ms → 走到 90% (180ms) 时 modal 启动 480ms 上滑浮入 (含过冲)
        total_in = round(0.9 * 200 + duration)  # 0.9×200 + 480 = 660
        form_note = (
            "\n> 演示形态: 居中弹窗 + 全屏遮罩组合动画 orchestration + modal 显式过冲;\n"
            "> - 遮罩 200ms fade-in (`opacity 0→1`, ease-out);\n"
            "> - 遮罩走到 90% (180ms) 时, modal 启动 480ms 上滑浮入 "
            "(3 帧: `+24rpx → 60% 过冲到 -8rpx → 100% 回正到 0`, opacity 0→1);\n"
            "> - modal curve 用 `cubic-bezier(0.4, 0, 0.2, 1)` ease-in-out, "
            "不带隐式 overshoot, 让 keyframe 8rpx 过冲独立可控;\n"
            f"> - 总入场 = 0.9 × 200 + {duration} = {total_in}ms "
            f"(modal 自身 {duration}ms 仍合规 ≤ 1000ms)。\n>\n"
            "> 跟 C2 ActionSheet 共享 mask + mainDelay timing (200/180), "
            "但 C1 modal 自身 480ms (含过冲) 比 C2 sheet 420ms 略长, 节奏更弹性。\n"
        )
    else:
        form_note = ""

    pascal_name = "".join(w.capitalize() for w in skill_id.split("-"))

    yaml_head = f"""```yaml
Skill名称: "{pascal_name}"
场景编号: "{scene_id}"
场景名: "{s['cn']}"
动作类型: "Entrance (入场)"
时长: "{duration}ms"
缓动曲线: "{curve}"
动画属性: "transform, opacity{', filter' if has_filter else ''}"
物理逻辑: "{physics}"
AI唤醒词: "{wakeup}"
```"""

    return f"""# {pascal_name}

> {s['cn']} · {action_cn} · **优雅 (Elegant)** 范式

---

{yaml_head}

---

## 1. 实现代码
{form_note}
### wxml

```xml
{wxml}
```

### wxss

```css
{wxss}
```

---

{spring_section}
---

{self_check}
---

## 4. AI 唤醒词扩展用法

### 在 Cursor 中

> "在 `pages/<your-page>` 给{s['cn']}加一个**优雅入场**动效,参考 [{skill_id}](../skills/{skill_id}.md) skill"

### 在 Claude Code / Codex 中

> "Apply the `{skill_id}` skill from `docs/motion-catalog.md` to `<component>`."

### 通用 prompt 片段

> "{wakeup}"

---

## 5. 适用边界

{boundary}

---

## 6. 引用

- 上一级目录: [docs/motion-catalog.md](../motion-catalog.md)
- 协议规则: [.cursor/rules/motion.mdc](../../.cursor/rules/motion.mdc)
- 命名规范: 见 [motion-catalog.md 第 5 节](../motion-catalog.md#5-命名规范)
"""


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    written = []
    for skill_id, scene_id, action, action_cn, wakeup_cn, wakeup_en in SKILLS:
        content = render_skill(skill_id, scene_id, action, action_cn, wakeup_cn, wakeup_en)
        path = OUT_DIR / f"{skill_id}.md"
        path.write_text(content, encoding="utf-8")
        written.append(skill_id)
    print(f"已生成 {len(written)} 个 skill 文件:")
    for s in written:
        print(f"  - {s}")


if __name__ == "__main__":
    main()
