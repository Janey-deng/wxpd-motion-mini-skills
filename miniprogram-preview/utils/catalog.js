/**
 * catalog.js - 动效目录数据源
 *
 * 由 docs/skills/*.md 的 YAML 头手工同步而来。
 * 小程序无 Node fs API, 故无法运行时解析 md, 只能在此手动维护。
 *
 * 同步规则: 新增 skill 时, 在 ALL_SKILLS 末尾追加一条记录, 并在
 * components/motion-card/motion-card.wxss 末尾追加对应 keyframes。
 *
 * v1.2 (2026-05): 移除 lively / restrained 情绪, 仅保留 elegant 单一范式;
 *                 12 场景每场景 1 个 skill, 共 12 个; 数据层删除 emotion 字段。
 * v1.3 (2026-05): 精简场景库, 删除 C6 侧边抽屉 / C8 Tab 内容 / C9 图片懒加载 /
 *                 C11 上拉加载 / C12 全屏遮罩 五个场景及其对应 skill, 共保留 7 个。
 * v1.5 (2026-05): 删除 C7 骨架屏切内容 (应用场景不多), 共保留 6 个。
 */

// sceneId -> 中文名映射 (slug 字段已移除, 实际只有 gen_skills.py 脚本侧需要 slug 用于生成 wxml 类名)
const SCENARIOS = {
  C1:  { cn: '居中弹窗' },
  C2:  { cn: '底部抽屉' },
  C3:  { cn: '顶部 Toast' },
  C4:  { cn: '列表项卡片' },
  C5:  { cn: '浮层' },
  C10: { cn: '下拉刷新' },
};

// elegant 单一范式: 时长 520ms, cubic-bezier(0.32, 1.18, 0.5, 1), 末端 ~7% 微量超越
const ELEGANT_DURATION = 520;
const ELEGANT_CURVE = 'cubic-bezier(0.32, 1.18, 0.5, 1)';
// C1 modal 专用 curve: ease-in-out, 不带隐式 overshoot (因 keyframe 已显式给 8rpx 过冲)
// 跟 ELEGANT_CURVE (隐式 ~7% overshoot) 共存: 显式 + 隐式 overshoot 不可叠加, 否则过头
const C1_MODAL_CURVE = 'cubic-bezier(0.4, 0, 0.2, 1)';

// 每条 skill 的最小数据集 (元数据 + AI 唤醒词)
// 6 场景 × 1 elegant = 6 个 skill, 全部入场
// 唤醒词拆中文 (wakeupCN) + 英文 (wakeupEN), 各 5 个同义/变体词, 用 ' / ' 分隔, 详情页分两行展示
const ALL_SKILLS = [
  {
    id: 'modal-slide-up-in-elegant',       name: '居中弹窗 · 上滑浮入',          sceneId: 'C1',
    // duration override 480ms (modal 自身, 用于显式过冲 + 回正); curve override C1_MODAL_CURVE
    // (ease-in-out 不带隐式 overshoot, 让 keyframe 8rpx 显式过冲独立可控);
    // 配合 orchestration 形成"遮罩 90% → modal 启动"组合动画
    // 总入场 = 0.9 × 200 + 480 = 660ms (modal 自身 ≤ 1000ms, 总入场仍 ≤ 1000ms)
    type: 'entrance', duration: 480, curve: C1_MODAL_CURVE,
    orchestration: { maskDuration: 200, mainDelay: 180 },
    physics: '居中弹窗从下方 24rpx 处上浮并渐显, 60% 时刻过冲到目标上方 8rpx, 再回落到目标位置, 弹性收尾.',
    wakeupCN: '上滑浮入 / 弹窗优雅出现 / 居中浮起带过冲 / 弹出上滑回弹 / 优雅弹窗',
    wakeupEN: 'slide up in elegant / soft spring up / modal slide up overshoot / pop up in elegant / gentle lift up with bounce',
  },
  {
    id: 'actionsheet-slide-up-elegant',    name: '底部抽屉 · 上滑展开',    sceneId: 'C2',
    // duration override 420ms (sheet 自身): 因为是"遮罩 + 卡片"组合动画, sheet 自身缩短到 420ms
    // 让出空间给前置遮罩渐显; orchestration 字段表示组合动画 timing (跟 C1 modal 同款):
    //   - maskDuration: 200ms (遮罩快速渐显, 建立暗背景)
    //   - mainDelay: 180ms (= 0.9 × 200, 遮罩走完 90% 时主动作启动)
    //   - 总入场时长 = 0.9 × 200 + 420 = 600ms (1x 倍速)
    type: 'entrance', duration: 420, curve: ELEGANT_CURVE,
    orchestration: { maskDuration: 200, mainDelay: 180 },
    physics: '底部抽屉缓入缓出上滑, 末端微量超越后收住.',
    wakeupCN: '上滑展开 / 底部抽屉优雅弹起 / 底部弹出 / 抽屉上滑 / 上推出现',
    wakeupEN: 'slide up elegant / actionsheet slide up / bottom drawer in / soft slide up / drawer rise',
  },
  {
    id: 'toast-drop-in-elegant',           name: '顶部 Toast · 下落出现',           sceneId: 'C3',
    type: 'entrance', duration: ELEGANT_DURATION, curve: ELEGANT_CURVE,
    physics: 'Toast 缓入缓出从顶部下落, 末端微量超越后停稳, 含蓄出现.',
    wakeupCN: '下落出现 / 顶部 Toast 优雅出现 / 顶部下落 / Toast 落入 / 顶部提示出现',
    wakeupEN: 'drop in elegant / toast drop in / fall in elegant / top toast in / soft drop in',
  },
  {
    id: 'card-stagger-in-elegant',         name: '列表项卡片 · 错位浮入',         sceneId: 'C4',
    // duration override 600ms (单卡): 因 6 卡 stagger 总入场需要更舒展的"呼吸感",
    // 单卡延长到 600ms (远低于 1000ms 红线); 总入场 = 600 + 5×60 = 900ms
    type: 'entrance', duration: 600, curve: ELEGANT_CURVE,
    physics: '列表项错位浮入, 每项延迟 60ms, 末端 ~7% 微量超越.',
    wakeupCN: '错位浮入 / 卡片优雅入场 / 列表错位入场 / 卡片依次浮入 / 列表项浮现',
    wakeupEN: 'stagger in elegant / card stagger in / list cascade in / sequential fade up / staggered entrance',
  },
  {
    id: 'popover-anchor-in-elegant',       name: '浮层 · 锚点放大',       sceneId: 'C5',
    type: 'entrance', duration: ELEGANT_DURATION, curve: ELEGANT_CURVE,
    physics: '浮层从锚点 0.6 缩放放大, 末端 ~7% 微量超越.',
    wakeupCN: '锚点放大 / Popover 出现 / 浮层弹出 / 锚点缩放 / 引导提示出现',
    wakeupEN: 'anchor in elegant / popover in / popover scale in / anchor scale up / tooltip in',
  },
  {
    id: 'refresh-pull-in-elegant',         name: '下拉刷新 · 弹性下拉',         sceneId: 'C10',
    type: 'entrance', duration: ELEGANT_DURATION, curve: ELEGANT_CURVE,
    physics: '下拉刷新指示器缓入缓出从顶部出现, 末端微量超越后停稳.',
    wakeupCN: '弹性下拉 / 下拉刷新优雅出现 / 下拉指示出现 / 刷新弹入 / 下拉回弹',
    wakeupEN: 'pull in elegant / refresh pull in / pull down elegant / pull to refresh / soft pull in',
  },
];

function getById(id) {
  return ALL_SKILLS.find((s) => s.id === id);
}

function withEnriched(skill) {
  if (!skill) return null;
  // shortName: 去掉 name 中第一个 ' · ' 之前的场景部分,用于卡片显示
  // 例: '居中弹窗 · 上滑浮入' -> '上滑浮入'
  // 若 name 不含 ' · ',shortName 退化为 name 本身
  const sepIdx = skill.name.indexOf(' · ');
  const shortName = sepIdx >= 0 ? skill.name.slice(sepIdx + 3) : skill.name;
  return Object.assign({}, skill, {
    shortName,
    sceneName: SCENARIOS[skill.sceneId] ? SCENARIOS[skill.sceneId].cn : skill.sceneId,
  });
}

module.exports = {
  ALL_SKILLS,
  getById,
  withEnriched,
};
