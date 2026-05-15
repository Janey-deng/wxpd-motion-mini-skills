# ModalSlideUpInElegant

> 居中弹窗 · 上滑浮入 · **优雅 (Elegant)** 范式

---

```yaml
Skill名称: "ModalSlideUpInElegant"
场景编号: "C1"
场景名: "居中弹窗"
动作类型: "Entrance (入场)"
时长: "480ms"
缓动曲线: "cubic-bezier(0.4, 0, 0.2, 1)"
动画属性: "transform, opacity"
物理逻辑: "居中弹窗从下方 24rpx 处上浮并渐显, 60% 时刻过冲到目标上方 8rpx, 再回落到目标位置, 弹性收尾。"
AI唤醒词: "中文: 上滑浮入 / 弹窗优雅出现 / 居中浮起带过冲 / 弹出上滑回弹 / 优雅弹窗 - 英文: slide up in elegant / soft spring up / modal slide up overshoot / pop up in elegant / gentle lift up with bounce"
```

---

## 1. 实现代码

> 演示形态: 居中弹窗 + 全屏遮罩组合动画 orchestration + modal 显式过冲;
> - 遮罩 200ms fade-in (`opacity 0→1`, ease-out);
> - 遮罩走到 90% (180ms) 时, modal 启动 480ms 上滑浮入 (3 帧: `+24rpx → 60% 过冲到 -8rpx → 100% 回正到 0`, opacity 0→1);
> - modal curve 用 `cubic-bezier(0.4, 0, 0.2, 1)` ease-in-out, 不带隐式 overshoot, 让 keyframe 8rpx 过冲独立可控;
> - 总入场 = 0.9 × 200 + 480 = 660ms (modal 自身 480ms 仍合规 ≤ 1000ms)。
>
> 跟 C2 ActionSheet 共享 mask + mainDelay timing (200/180), 但 C1 modal 自身 480ms (含过冲) 比 C2 sheet 420ms 略长, 节奏更弹性。

### wxml

```xml
<view class="ml-modal-mask {{visible ? 'ml-modal-mask--show' : ''}}" bindtap="onClose">
  <view class="ml-modal {{visible ? 'ml-modal--in' : ''}}" catchtap="">
    <view class="ml-modal__title">标题</view>
    <view class="ml-modal__body"><slot></slot></view>
  </view>
</view>
```

### wxss

```css
.ml-modal-mask {
  position: fixed; inset: 0;
  background: rgba(0, 0, 0, .4);
  opacity: 0;
  pointer-events: none;
  transition: opacity 200ms cubic-bezier(0.4, 0, 0.2, 1);
}
.ml-modal-mask--show { opacity: 1; pointer-events: auto; }

.ml-modal {
  position: absolute; left: 50%; top: 50%;
  width: 560rpx;
  background: #fff; border-radius: 24rpx;
  transform: translate3d(-50%, -50%, 0);
  opacity: 0;
  will-change: transform, opacity;
}
/* 主动作延迟 180ms 启动 (遮罩走完 90%), 形成 "遮罩 → modal" 顺序入场 */
.ml-modal--in {
  animation: ml-slide-up-in-elegant 480ms cubic-bezier(0.4, 0, 0.2, 1) both;
  animation-delay: 180ms;
}

/* 3 帧 keyframe: 上滑 24rpx → 60% 过冲到目标上方 8rpx → 100% 回正到目标位置 */
@keyframes ml-slide-up-in-elegant {
  0%   { transform: translate3d(-50%, calc(-50% + 24rpx), 0); opacity: 0; }
  60%  { transform: translate3d(-50%, calc(-50% - 8rpx), 0);  opacity: 1; }
  100% { transform: translate3d(-50%, -50%, 0);               opacity: 1; }
}
```

---

## 2. 物理参数换算

| 设计来源 | 缓动曲线 | 显式 overshoot | 推荐 duration |
| --- | --- | --- | --- |
| 手工 3 帧 keyframe | `cubic-bezier(0.4, 0, 0.2, 1)` (ease-in-out, 不带隐式 overshoot) | 8rpx (≈ 上滑距离 33%) | 480ms |

> C1 modal 不走 spring → cubic-bezier 拟合路径, 改为 keyframe 显式定义过冲距离 (60% 时刻 -8rpx),
> 让设计师可独立微调过冲幅度而不受 cubic-bezier 数值变化影响。
> 整体节奏: 0% → 60% (288ms) 上升 + 过冲, 60% → 100% (192ms) 回正。

---

## 3. 自查报告

```
FPS 预估:    60+
重排风险:    无
合成层:      已触发 GPU 加速 (translate3d + will-change)
时长合规:    ✅ 480ms ≤ 1000ms
```

---

## 4. AI 唤醒词扩展用法

### 在 Cursor 中

> "在 `pages/<your-page>` 给居中弹窗加一个**优雅入场**动效,参考 [modal-slide-up-in-elegant](../skills/modal-slide-up-in-elegant.md) skill"

### 在 Claude Code / Codex 中

> "Apply the `modal-slide-up-in-elegant` skill from `docs/motion-catalog.md` to `<component>`."

### 通用 prompt 片段

> "中文: 上滑浮入 / 弹窗优雅出现 / 居中浮起带过冲 / 弹出上滑回弹 / 优雅弹窗 - 英文: slide up in elegant / soft spring up / modal slide up overshoot / pop up in elegant / gentle lift up with bounce"

---

## 5. 适用边界

✅ 内容详情 / 商品详情 / 评论展开 / 设置面板 / 阅读类
❌ 紧急提示 / 工具类即时反馈 (本期未实现 lively / restrained 备选)

---

## 6. 引用

- 上一级目录: [docs/motion-catalog.md](../motion-catalog.md)
- 协议规则: [.cursor/rules/motion.mdc](../../.cursor/rules/motion.mdc)
- 命名规范: 见 [motion-catalog.md 第 5 节](../motion-catalog.md#5-命名规范)
