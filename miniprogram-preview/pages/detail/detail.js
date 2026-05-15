const catalog = require('../../utils/catalog.js');

Page({
  data: {
    skillId: '',
    skill: null,
    currentSpeed: 1,
    // safeTop: stage padding-top (px), 让灰底贯通到状态栏 + 胶囊按钮 + 6px 呼吸
    // backTop / backHeight: 自造返回按钮跟胶囊按钮 "顶部对齐 + 等高", 视觉对称
    safeTop: 88,
    backTop: 28,
    backHeight: 32,
    // navSolid: 页面滚动后导航条背景从透明变 #fff (区分导航区与正文区)
    navSolid: false,
  },

  onLoad(options) {
    let safeTop = 88;
    let backTop = 28;
    let backHeight = 32;
    try {
      const menu = wx.getMenuButtonBoundingClientRect();
      if (menu && menu.bottom) {
        safeTop = Math.round(menu.bottom + 6);
        backTop = menu.top;
        backHeight = menu.height;
      }
    } catch (e) {
      // 兼容性兜底,保持默认值
    }

    const id = options.id;
    if (!id) {
      wx.showToast({ title: '缺少 skill id', icon: 'none' });
      this.setData({ safeTop, backTop, backHeight });
      return;
    }
    const raw = catalog.getById(id);
    const skill = catalog.withEnriched(raw);
    if (!skill) {
      wx.showToast({ title: '未找到 skill: ' + id, icon: 'none' });
      this.setData({ safeTop, backTop, backHeight });
      return;
    }
    this.setData({
      skillId: id,
      skill,
      safeTop,
      backTop,
      backHeight,
    });
  },

  goBack() {
    wx.navigateBack({ delta: 1 });
  },

  // onPageScroll 触发频率高 (每帧), 用 prevState 比较, 只在状态翻转时 setData, 避免性能浪费
  onPageScroll(e) {
    const navSolid = e.scrollTop > 4;
    if (navSolid !== this.data.navSolid) {
      this.setData({ navSolid });
    }
  },

  onReplay() {
    const mc = this.selectComponent('#mc');
    if (mc) mc.replay();
  },

  onSpeedTap(e) {
    const speed = Number(e.currentTarget.dataset.speed);
    if (!speed) return;
    this.setData({ currentSpeed: speed });
    const mc = this.selectComponent('#mc');
    if (mc) mc.setSpeed(speed);
  },

  copyCurve() {
    const { skill } = this.data;
    if (!skill) return;
    const text = `animation: ${skill.id} ${skill.duration}ms ${skill.curve} both;`;
    wx.setClipboardData({
      data: text,
      success: () => {
        wx.showToast({ title: 'CSS 已复制', icon: 'success' });
      },
    });
  },

  copySkillRef() {
    const { skill } = this.data;
    if (!skill) return;
    const text = `Apply the \`${skill.id}\` skill from docs/motion-catalog.md to <component>.`;
    wx.setClipboardData({
      data: text,
      success: () => {
        wx.showToast({ title: 'Cursor prompt 已复制', icon: 'success' });
      },
    });
  },
});
