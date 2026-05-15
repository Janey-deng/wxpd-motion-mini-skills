#!/usr/bin/env python3
"""生成 7 个 elegant skill 的 keyframes 段, 追加到 motion-card.wxss。

v1.2 (2026-05): 移除 lively / restrained, 仅保留 elegant 单一范式;
                12 场景每场景 1 个 skill, 共 12 个 keyframes。
v1.3 (2026-05): 精简到 7 场景, 删除 C6 / C8 / C9 / C11 / C12 五个场景。

使用: python3 scripts/gen_keyframes.py
本脚本会重写 wxss 文件末尾的"自动生成段"区域,不影响手写部分。
"""
from pathlib import Path

WXSS_PATH = Path(__file__).parent.parent / "miniprogram-preview" / "components" / "motion-card" / "motion-card.wxss"
MARKER = "/* ========== 自动生成段: skill keyframes"

# elegant 单一范式参数 — 必须与 miniprogram-preview/utils/catalog.js 中保持一致
ELEGANT_CURVE = "cubic-bezier(0.32, 1.18, 0.5, 1)"
ELEGANT_DURATION = 520

# 每个 skill 的动画规格
# (skill_id, start_transform, start_opacity, end_transform, end_opacity, [extra_start, extra_end])
SPECS = [
    # C1 Modal: scale 0.85 -> 1.0
    ("modal-scale-in-elegant",
     "translate3d(-50%, -50%, 0) scale(0.85)", 0,
     "translate3d(-50%, -50%, 0) scale(1.0)",  1),
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
    # C7 Skeleton crossfade: opacity 0 -> 1
    ("skeleton-crossfade-in-elegant",
     None, 0,
     None, 1),
    # C10 Refresh: translateY -100% -> 0
    ("refresh-pull-in-elegant",
     "translate3d(0, -100%, 0)", 0,
     "translate3d(0, 0, 0)",     1),
]


def render_keyframes(spec):
    if len(spec) == 5:
        skill_id, st, so, et, eo = spec
        extra_s, extra_e = "", ""
    elif len(spec) == 7:  # has extra start/end (filter etc.)
        skill_id, st, so, et, eo, extra_s, extra_e = spec
    else:
        raise ValueError(f"unknown spec ({len(spec)}): {spec}")

    start_props = []
    if st: start_props.append(f"transform: {st};")
    if so is not None: start_props.append(f"opacity: {so};")
    if extra_s: start_props.append(extra_s)

    end_props = []
    if et: end_props.append(f"transform: {et};")
    if eo is not None: end_props.append(f"opacity: {eo};")
    if extra_e: end_props.append(extra_e)

    keyframes = f"""@keyframes mc-{skill_id} {{
  0%   {{ {" ".join(start_props)} }}
  100% {{ {" ".join(end_props)} }}
}}
.mc-anim-{skill_id} {{
  animation: mc-{skill_id} {ELEGANT_DURATION}ms {ELEGANT_CURVE} both;
}}"""
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
