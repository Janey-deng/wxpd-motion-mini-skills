# Skill Template (参考标杆,不是真正的 skill)

> 本文件是 [docs/skills/](.) 下所有 skill 文件的统一格式标杆。
> 新增 skill 时,直接复制本文件改造,**6 段必须齐全**。
>
> 本项目自 v1.2 起统一为 **优雅 (Elegant) 单一范式** (520ms + `cubic-bezier(0.32, 1.18, 0.5, 1)`),
> 不再分情绪。如其他项目需恢复多情绪,见 [.cursor/rules/motion.mdc 第 4.1 节](../../.cursor/rules/motion.mdc) 的扩展字段说明。

---

```yaml
Skill名称: "ExampleScaleInElegant"
场景编号: "C1"
场景名: "居中弹窗"
动作类型: "Entrance (入场)"
时长: "520ms"
缓动曲线: "cubic-bezier(0.32, 1.18, 0.5, 1)"
动画属性: "transform, opacity"
物理逻辑: "[1-2 句] 描述动效的加速方式、惯性及质感。例: 元素从 0.85 缩放经一次 ~7% 微量超越后稳定在 1.0,主动作完成后含蓄收尾。体感'呼吸感'。"
AI唤醒词: "中文: 缩放浮入 / <场景中文>缩放浮入 - 英文: scale in elegant / soft spring in"
```

> **核心字段** (motion.mdc 4.1 节 [MUST]): `Skill名称` / `物理逻辑` / `AI唤醒词` + 实现代码 (本项目放第 1 节)。
> **扩展字段** (motion.mdc 4.1 节 [MAY]): `场景编号` / `场景名` / `动作类型` / `时长` / `缓动曲线` / `动画属性`,本项目所有 skill 必须保持这 6 个扩展字段一致。

---

## 1. 实现代码 (wxml + wxss)

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
  transition: opacity 520ms cubic-bezier(0.4, 0, 0.2, 1);
}
.ml-modal-mask--show { opacity: 1; pointer-events: auto; }

.ml-modal {
  position: absolute; left: 50%; top: 50%;
  width: 560rpx;
  background: #fff; border-radius: 24rpx;
  transform: translate3d(-50%, -50%, 0) scale(0.85);
  opacity: 0;
  will-change: transform, opacity;
}
.ml-modal--in {
  animation: ml-scale-in-elegant 520ms cubic-bezier(0.32, 1.18, 0.5, 1) both;
}

@keyframes ml-scale-in-elegant {
  0%   { transform: translate3d(-50%, -50%, 0) scale(0.85); opacity: 0; }
  100% { transform: translate3d(-50%, -50%, 0) scale(1.0);  opacity: 1; }
}
```

---

## 2. 物理参数换算

| 输入 spring | 输出 cubic-bezier | 实测 overshoot | 推荐 duration |
| --- | --- | --- | --- |
| `spring(1, 220, 18)` | `cubic-bezier(0.32, 1.18, 0.5, 1)` | ~7% | 520ms |

> 拟合算法详见 [miniprogram-preview/utils/spring2bezier.js](../../miniprogram-preview/utils/spring2bezier.js)。
> Cubic-bezier 拟合误差 < 5%,体感等效。

---

## 3. 自查报告 (按 motion.mdc 第 7.1 节)

```
FPS 预估:    60+ (仅 transform/opacity, GPU 合成层)
重排风险:    无 (未触发 layout 属性)
合成层:      已触发 GPU 加速 (translate3d + will-change)
时长合规:    ✅ 520ms ≤ 600ms
```

---

## 4. AI 唤醒词扩展用法

### 在 Cursor 中

> "在 `pages/<your-page>` 给居中弹窗加一个**优雅入场**动效,参考 `modal-scale-in-elegant` skill"

### 在 Claude Code / Codex 中

> "Apply the `modal-scale-in-elegant` skill from `docs/motion-catalog.md` to `<component>`."

### 通用 prompt 片段

> "中文: 缩放浮入 / 居中弹窗缩放浮入 - 英文: scale in elegant / soft spring in"

---

## 5. 适用边界

✅ 内容详情 / 商品详情 / 评论展开 / 设置面板 / 阅读类
❌ 紧急提示 / 工具类即时反馈 (本期未实现 lively / restrained 备选)

---

## 6. 引用

- 上一级目录: [docs/motion-catalog.md](../motion-catalog.md)
- 协议规则: [.cursor/rules/motion.mdc](../../.cursor/rules/motion.mdc)
- 命名规范: 见 [motion-catalog.md 第 5 节](../motion-catalog.md#5-命名规范)
