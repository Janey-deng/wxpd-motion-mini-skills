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
 */

// sceneId -> 中文名映射 (slug 字段已移除, 实际只有 gen_skills.py 脚本侧需要 slug 用于生成 wxml 类名)
const SCENARIOS = {
  C1:  { cn: '居中弹窗' },
  C2:  { cn: '底部抽屉' },
  C3:  { cn: '顶部 Toast' },
  C4:  { cn: '列表项卡片' },
  C5:  { cn: '浮层' },
  C7:  { cn: '骨架屏' },
  C10: { cn: '下拉刷新' },
};

// elegant 单一范式: 时长 520ms, cubic-bezier(0.32, 1.18, 0.5, 1), 末端 ~7% 微量超越
const ELEGANT_DURATION = 520;
const ELEGANT_CURVE = 'cubic-bezier(0.32, 1.18, 0.5, 1)';

// 每条 skill 的最小数据集 (元数据 + AI 唤醒词)
// 7 场景 × 1 elegant = 7 个 skill, 全部入场
// 唤醒词拆中文 (wakeupCN) + 英文 (wakeupEN), 各 5 个同义/变体词, 用 ' / ' 分隔, 详情页分两行展示
const ALL_SKILLS = [
  {
    id: 'modal-scale-in-elegant',          name: '居中弹窗 · 缩放浮入',          sceneId: 'C1',
    type: 'entrance', duration: ELEGANT_DURATION, curve: ELEGANT_CURVE,
    physics: '居中弹窗缓入缓出, 末端 ~7% 微量超越, 含蓄收尾.',
    wakeupCN: '缩放浮入 / 弹窗优雅出现 / 居中放大 / 弹出缩放 / 优雅弹窗',
    wakeupEN: 'scale in elegant / soft spring in / modal scale in / pop in elegant / gentle scale up',
  },
  {
    id: 'actionsheet-slide-up-elegant',    name: '底部抽屉 · 上滑展开',    sceneId: 'C2',
    type: 'entrance', duration: ELEGANT_DURATION, curve: ELEGANT_CURVE,
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
    type: 'entrance', duration: ELEGANT_DURATION, curve: ELEGANT_CURVE,
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
    id: 'skeleton-crossfade-in-elegant',   name: '骨架屏 · 渐显交叉',   sceneId: 'C7',
    type: 'entrance', duration: ELEGANT_DURATION, curve: ELEGANT_CURVE,
    physics: '骨架屏与内容做 opacity 双层交叉, 同步反向变化.',
    wakeupCN: '渐显交叉 / 骨架屏切内容 / 骨架渐显 / 内容渐显切换 / 交叉淡入',
    wakeupEN: 'crossfade in elegant / skeleton crossfade / content fade swap / cross fade in / skeleton to content',
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
  // 例: '居中弹窗 · 缩放浮入' -> '缩放浮入'
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
