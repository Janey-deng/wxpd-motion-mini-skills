/**
 * spring2bezier - spring 物理参数转 cubic-bezier 拟合工具
 *
 * 输入: spring(mass, tension, friction)
 * 输出: { curve, duration, overshoot, fallback }
 *
 * 算法:
 *   1. 用 RK4 数值积分阻尼弹簧 ODE: m*x'' = -k*(x-1) - c*x'
 *   2. 找到 settling time (到达稳定 ±1%)
 *   3. 从对照表中查最近的预计算 cubic-bezier
 *
 * 微信小程序原生 WebView 不支持 Web Animations API,
 * 故运行时不实时计算 spring,而是用本表预计算后烧到 wxss 中。
 *
 * 注: 当前 catalog.js 已经把 elegant 单一范式的 cubic-bezier 字符串烧死,
 * 本模块作为算法参考实现保留 (docs/skills/*.md 中多处链接引用),
 * 后续若需新增情绪/复刻 spring 物理,可直接调用 spring2bezier(m,t,f)。
 */

const PRESET_TABLE = [
  // 顺序: zeta 从小到大 (越前面 overshoot 越大)
  {
    spring: 'spring(1, 180, 12)',
    mass: 1, tension: 180, friction: 12,
    zeta: 0.447,
    curve: 'cubic-bezier(0.34, 1.56, 0.64, 1)',
    duration: 360,
    overshootPct: 20,
    label: 'lively',
    cn: '欢快',
  },
  {
    spring: 'spring(1, 220, 18)',
    mass: 1, tension: 220, friction: 18,
    zeta: 0.607,
    curve: 'cubic-bezier(0.32, 1.18, 0.5, 1)',
    duration: 520,
    overshootPct: 7,
    label: 'elegant',
    cn: '优雅',
  },
  {
    spring: 'spring(1, 280, 28)',
    mass: 1, tension: 280, friction: 28,
    zeta: 0.837,
    curve: 'cubic-bezier(0.4, 1.0, 0.6, 1)',
    duration: 280,
    overshootPct: 1,
    label: 'critical',
    cn: '临界',
  },
];

/**
 * RK4 数值积分一个阻尼弹簧
 * @param {number} mass
 * @param {number} tension
 * @param {number} friction
 * @param {number} dt
 * @param {number} maxT
 * @returns {{ samples: Array<{t:number,x:number}>, peakT:number, peakX:number }}
 */
function simulateSpring(mass, tension, friction, dt = 0.001, maxT = 2.0) {
  let x = 0;
  let v = 0;
  const target = 1.0;
  const samples = [{ t: 0, x: 0 }];
  let peakX = 0;
  let peakT = 0;
  let t = 0;

  function deriv(x, v) {
    const a = (-tension * (x - target) - friction * v) / mass;
    return [v, a];
  }

  while (t < maxT) {
    const [k1x, k1v] = deriv(x, v);
    const [k2x, k2v] = deriv(x + (dt / 2) * k1x, v + (dt / 2) * k1v);
    const [k3x, k3v] = deriv(x + (dt / 2) * k2x, v + (dt / 2) * k2v);
    const [k4x, k4v] = deriv(x + dt * k3x, v + dt * k3v);

    x += (dt / 6) * (k1x + 2 * k2x + 2 * k3x + k4x);
    v += (dt / 6) * (k1v + 2 * k2v + 2 * k3v + k4v);
    t += dt;

    if (x > peakX) {
      peakX = x;
      peakT = t;
    }
    samples.push({ t, x });
  }
  return { samples, peakT, peakX };
}

/**
 * 找到 settling time (持续在 ±1% 内的第一个时间点)
 * @returns {number} ms
 */
function findSettlingTime(samples) {
  let lastUnsettled = 0;
  samples.forEach(({ t, x }) => {
    if (Math.abs(x - 1) >= 0.01) lastUnsettled = t;
  });
  return Math.round((lastUnsettled + 0.001) * 1000);
}

/**
 * 主 API: spring 三参数 -> cubic-bezier 拟合
 *
 * @param {number} mass
 * @param {number} tension
 * @param {number} friction
 * @returns {{ curve:string, duration:number, overshoot:number, source:string, fallback:boolean }}
 */
function spring2bezier(mass, tension, friction) {
  const zeta = friction / (2 * Math.sqrt(mass * tension));

  // 1. 优先查预设表 (近似匹配 zeta)
  let nearest = PRESET_TABLE[0];
  let minDiff = Infinity;
  PRESET_TABLE.forEach((p) => {
    const diff = Math.abs(p.zeta - zeta);
    if (diff < minDiff) {
      minDiff = diff;
      nearest = p;
    }
  });

  // 容忍 zeta 偏差 < 0.1 视为命中预设
  if (minDiff < 0.1) {
    return {
      curve: nearest.curve,
      duration: nearest.duration,
      overshoot: nearest.overshootPct,
      source: `preset(${nearest.label})`,
      fallback: false,
    };
  }

  // 2. 偏差太大,数值积分后给警告 + 推荐改用 keyframes
  const sim = simulateSpring(mass, tension, friction);
  const overshootPct = Math.max(0, (sim.peakX - 1) * 100);
  const settling = findSettlingTime(sim.samples);
  return {
    curve: 'cubic-bezier(0.4, 1, 0.6, 1)',
    duration: Math.min(600, settling),
    overshoot: Math.round(overshootPct),
    source: 'simulated',
    fallback: true,
    note: 'zeta 偏离预设表过远,建议在 wxss 中改用 @keyframes 多关键帧拟合,而非 cubic-bezier。',
  };
}

module.exports = {
  spring2bezier,
  simulateSpring,
  findSettlingTime,
  PRESET_TABLE,
};
