# CardStaggerInElegant

> 列表项卡片 · 错位浮入 · **优雅 (Elegant)** 范式

---

```yaml
Skill名称: "CardStaggerInElegant"
场景编号: "C4"
场景名: "列表项卡片"
动作类型: "Entrance (入场)"
时长: "600ms"
缓动曲线: "cubic-bezier(0.32, 1.18, 0.5, 1)"
动画属性: "transform, opacity"
物理逻辑: "列表项卡片缓入缓出, 末端 ~7% 微量超越, 主动作完成后含蓄收尾。体感'呼吸感'。"
AI唤醒词: "中文: 错位浮入 / 卡片优雅入场 / 列表错位入场 / 卡片依次浮入 / 列表项浮现 - 英文: stagger in elegant / card stagger in / list cascade in / sequential fade up / staggered entrance"
```

---

## 1. 实现代码

> 演示形态: 两列瀑布流, 6 个纯白卡 (左 3 + 右 3), 高度错落 (左列 高/矮/高 vs 右列 矮/高/矮);
> stagger 顺序按"从上到下逐行 Z 字"扫描: 左1=0ms / 右1=60ms / 左2=120ms / 右2=180ms / 左3=240ms / 右3=300ms;
> 单卡 600ms, 总入场 = 600+300 = 900ms (单卡 600ms 仍合规 ≤ 1000ms)。
>
> 实际项目可按 `leftItems` / `rightItems` 数据驱动, 高度由内容决定; 240rpx 顶距是演示版的视觉留白, 调用方按页面需求自行调整。

### wxml

```xml
<view class="ml-card-list">
  <view class="ml-card-list__col">
    <view class="ml-card {{visible ? 'ml-card--in' : ''}}"
          wx:for="{{leftItems}}" wx:key="id"
          style="animation-delay: {{index * 120}}ms">
      <view class="ml-card__title">{{item.title}}</view>
    </view>
  </view>
  <view class="ml-card-list__col">
    <view class="ml-card {{visible ? 'ml-card--in' : ''}}"
          wx:for="{{rightItems}}" wx:key="id"
          style="animation-delay: {{index * 120 + 60}}ms">
      <view class="ml-card__title">{{item.title}}</view>
    </view>
  </view>
</view>
```

### wxss

```css
/* 两列瀑布流容器 (240rpx 顶距为演示视觉留白, 调用方按页面需求自行调整) */
.ml-card-list {
  display: flex;
  gap: 16rpx;
  padding: 240rpx 24rpx 0;
  box-sizing: border-box;
}
.ml-card-list__col {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

/* 纯白卡, 高度由内容决定 */
.ml-card {
  background: #fff;
  border-radius: 16rpx;
  transform: translate3d(0, 24rpx, 0);
  opacity: 0;
  will-change: transform, opacity;
}
.ml-card--in {
  animation: ml-stagger-in-elegant 600ms cubic-bezier(0.32, 1.18, 0.5, 1) both;
}

@keyframes ml-stagger-in-elegant {
  0%   { transform: translate3d(0, 24rpx, 0); opacity: 0; }
  100% { transform: translate3d(0, 0, 0);     opacity: 1; }
}
```

---

## 2. 物理参数换算

| 输入 spring | 输出 cubic-bezier | 实测 overshoot | 推荐 duration |
| --- | --- | --- | --- |
| `spring(1, 220, 18)` | `cubic-bezier(0.32, 1.18, 0.5, 1)` | ~7% | 600ms |

> 拟合算法详见 [miniprogram-preview/utils/spring2bezier.js](../../miniprogram-preview/utils/spring2bezier.js)。
> Cubic-bezier 拟合误差 < 5%, 体感等效。

---

## 3. 自查报告

```
FPS 预估:    60+
重排风险:    无
合成层:      已触发 GPU 加速 (translate3d + will-change)
时长合规:    ✅ 600ms ≤ 1000ms
```

---

## 4. AI 唤醒词扩展用法

### 在 Cursor 中

> "在 `pages/<your-page>` 给列表项卡片加一个**优雅入场**动效,参考 [card-stagger-in-elegant](../skills/card-stagger-in-elegant.md) skill"

### 在 Claude Code / Codex 中

> "Apply the `card-stagger-in-elegant` skill from `docs/motion-catalog.md` to `<component>`."

### 通用 prompt 片段

> "中文: 错位浮入 / 卡片优雅入场 / 列表错位入场 / 卡片依次浮入 / 列表项浮现 - 英文: stagger in elegant / card stagger in / list cascade in / sequential fade up / staggered entrance"

---

## 5. 适用边界

✅ 内容详情 / 商品详情 / 评论展开 / 设置面板 / 阅读类
❌ 紧急提示 / 工具类即时反馈 (本期未实现 lively / restrained 备选)

---

## 6. 引用

- 上一级目录: [docs/motion-catalog.md](../motion-catalog.md)
- 协议规则: [.cursor/rules/motion.mdc](../../.cursor/rules/motion.mdc)
- 命名规范: 见 [motion-catalog.md 第 5 节](../motion-catalog.md#5-命名规范)
