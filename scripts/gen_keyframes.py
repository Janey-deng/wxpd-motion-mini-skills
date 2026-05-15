#!/usr/bin/env python3
"""生成 6 个 elegant skill 的 keyframes 段, 追加到 motion-card.wxss。

v1.2 (2026-05): 移除 lively / restrained, 仅保留 elegant 单一范式;
                12 场景每场景 1 个 skill, 共 12 个 keyframes。
v1.3 (2026-05): 精简到 7 场景, 删除 C6 / C8 / C9 / C11 / C12 五个场景。
v1.5 (2026-05): 删除 C7 骨架屏切内容 (应用场景不多), 共保留 6 个 keyframes。

使用: python3 scripts/gen_keyframes.py
本脚本会重写 wxss 文件末尾的"自动生成段"区域,不影响手写部分。
"""
from pathlib import Path

WXSS_PATH = Path(__file__).parent.parent / "miniprogram-preview" / "components" / "motion-card" / "motion-card.wxss"
MARKER = "/* ========== 自动生成段: skill keyframes"

# elegant 单一范式参数 — 必须与 miniprogram-preview/utils/catalog.js 中保持一致
ELEGANT_CURVE = "cubic-bezier(0.32, 1.18, 0.5, 1)"
ELEGANT_DURATION = 520

# per-skill duration override (与 catalog.js 中对应字段保持一致)
# - card-stagger-in-elegant: 单卡 600ms (远低于 1000ms 红线); 6 卡 stagger 总入场 900ms
# - actionsheet-slide-up-elegant: sheet 自身 420ms (mask 200 + mainDelay 180 → 总 600ms)
# - modal-slide-up-in-elegant:    modal 自身 480ms + 显式 8rpx 过冲 + curve override
#                                 (mask 200 + mainDelay 180 → 总 660ms; modal 自身仍 ≤ 1000ms)
DURATION_OVERRIDES = {
    "card-stagger-in-elegant": 600,
    "actionsheet-slide-up-elegant": 420,
    "modal-slide-up-in-elegant": 480,
}

# per-skill curve override (默认 ELEGANT_CURVE, 仅显式列出的 skill 替换为自定义 curve)
# - modal-slide-up-in-elegant: 用 ease-in-out 不带隐式 overshoot, 因 keyframe 已显式给 8rpx 过冲
CURVE_OVERRIDES = {
    "modal-slide-up-in-elegant": "cubic-bezier(0.4, 0, 0.2, 1)",
}

# 每个 skill 的动画规格
# 简单版 (5 元组): (skill_id, start_transform, start_opacity, end_transform, end_opacity)
# 带 extra (7 元组): + (extra_start, extra_end) — 用于 filter 等额外属性
# 带 mid_frames (6 元组): + mid_frames=[(percent, transform_or_None, opacity_or_None), ...]
#                        — 用于显式过冲/弹跳等多帧动画 (e.g. C1 modal 60% 过冲 -8rpx)
SPECS = [
    # C1 Modal: 短距离上滑浮入 (translateY +24rpx -> -8rpx 过冲 -> 0) + opacity 0 -> 1
    # 居中定位 translate3d(-50%, -50%); 60% 时刻过冲到 -50% 上方 8rpx
    ("modal-slide-up-in-elegant",
     "translate3d(-50%, calc(-50% + 24rpx), 0)", 0,
     "translate3d(-50%, -50%, 0)",               1,
     [(60, "translate3d(-50%, calc(-50% - 8rpx), 0)", 1)]),
    # C2 ActionSheet: translateY 100% -> 0
    ("actionsheet-slide-up-elegant",
     "translate3d(0, 100%, 0)", None,
     "translate3d(0, 0, 0)",    None),
    # C3 Toast: translateY -200% -> 0 (顶部下落)
    ("toast-drop-in-elegant",
     "translate3d(-50%, -200%, 0)", 0,
     "translate3d(-50%, 0, 0)",     1),
    # C4 Card stagger: translateY 24rpx -> 0
    ("card-stagger-in-elegant",
     "translate3d(0, 24rpx, 0)", 0,
     "translate3d(0, 0, 0)",     1),
    # C5 Popover: scale 0.6 -> 1.0
    ("popover-anchor-in-elegant",
     "scale(0.6)", 0,
     "scale(1.0)", 1),
    # C10 Refresh: translateY -100% -> 0
    ("refresh-pull-in-elegant",
     "translate3d(0, -100%, 0)", 0,
     "translate3d(0, 0, 0)",     1),
]


def _props(transform, opacity, extra=""):
    """单帧 props 字符串拼接 (transform / opacity / extra 任一可空)"""
    parts = []
    if transform: parts.append(f"transform: {transform};")
    if opacity is not None: parts.append(f"opacity: {opacity};")
    if extra: parts.append(extra)
    return " ".join(parts)


def render_keyframes(spec):
    """支持三种 spec 形态:
       - 5 元组: 简单两帧 (0% / 100%)
       - 6 元组 (末尾 mid_frames=list): 多帧 (0% / mid_frames... / 100%)
       - 7 元组 (末尾 extra_start, extra_end): 两帧 + filter 等额外属性
    """
    mid_frames = []
    extra_s, extra_e = "", ""
    if len(spec) == 5:
        skill_id, st, so, et, eo = spec
    elif len(spec) == 6:
        skill_id, st, so, et, eo, mid_frames = spec
    elif len(spec) == 7:
        skill_id, st, so, et, eo, extra_s, extra_e = spec
    else:
        raise ValueError(f"unknown spec ({len(spec)}): {spec}")

    duration = DURATION_OVERRIDES.get(skill_id, ELEGANT_DURATION)
    curve = CURVE_OVERRIDES.get(skill_id, ELEGANT_CURVE)

    frames = [f"  0%   {{ {_props(st, so, extra_s)} }}"]
    for percent, mid_t, mid_o in mid_frames:
        frames.append(f"  {percent}%  {{ {_props(mid_t, mid_o)} }}")
    frames.append(f"  100% {{ {_props(et, eo, extra_e)} }}")

    keyframes = (
        f"@keyframes mc-{skill_id} {{\n"
        + "\n".join(frames)
        + "\n}\n"
        f".mc-anim-{skill_id} {{\n"
        f"  animation: mc-{skill_id} {duration}ms {curve} both;\n"
        f"}}"
    )
    return keyframes


def main():
    text = WXSS_PATH.read_text(encoding="utf-8")
    # 找到第一次出现的 marker, 之后内容(包括 marker 自身)全部丢掉
    idx = text.find(MARKER)
    if idx >= 0:
        text = text[:idx].rstrip() + "\n\n"

    text += MARKER + " (由 scripts/gen_keyframes.py 自动生成,勿手动改) ====== */\n\n"

    for spec in SPECS:
        text += render_keyframes(spec) + "\n\n"

    WXSS_PATH.write_text(text, encoding="utf-8")
    print(f"已生成 {len(SPECS)} 个 skill keyframes 到 {WXSS_PATH.relative_to(Path.cwd())}")


if __name__ == "__main__":
    main()
