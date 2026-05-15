const catalog = require('../../utils/catalog.js');

Page({
  data: {
    skills: [],
    totalCount: 0,
    safeTop: 88,
    // navSolid: 页面滚动后导航条背景从透明变 #fff (区分导航区与正文区)
    navSolid: false,
  },

  onLoad() {
    // 自定义导航栏: 用胶囊按钮底部 + 6px 作为内容安全顶距,避免大标题被胶囊遮挡
    let safeTop = 88;
    try {
      const menu = wx.getMenuButtonBoundingClientRect();
      if (menu && menu.bottom) safeTop = Math.round(menu.bottom + 6);
    } catch (e) {
      // 兼容性兜底,保持默认值
    }

    // 每场景 1 个 skill, 直接按 sceneId 顺序平铺
    const skills = catalog.ALL_SKILLS.map((s) => catalog.withEnriched(s));

    this.setData({
      skills,
      totalCount: skills.length,
      safeTop,
    });
  },

  goDetail(e) {
    const { id } = e.currentTarget.dataset;
    wx.navigateTo({ url: `/pages/detail/detail?id=${id}` });
  },

  // onPageScroll 触发频率高 (每帧), 用 prevState 比较, 只在状态翻转时 setData, 避免性能浪费
  onPageScroll(e) {
    const navSolid = e.scrollTop > 4;
    if (navSolid !== this.data.navSolid) {
      this.setData({ navSolid });
    }
  },
});
