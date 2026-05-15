const catalog = require('../../utils/catalog.js');

Component({
  properties: {
    skillId: {
      type: String,
      value: '',
      observer(newVal) {
        this._loadSkill(newVal);
      },
    },
    speed: { type: Number, value: 1 },
    autoPlay: { type: Boolean, value: true },
  },

  data: {
    skill: null,
    visible: false,
    actualDuration: 0,
  },

  methods: {
    _loadSkill(id) {
      if (!id) return;
      const raw = catalog.getById(id);
      const skill = catalog.withEnriched(raw);
      if (!skill) return;
      this.setData({
        skill,
        visible: false,
        actualDuration: Math.round(skill.duration / this.data.speed),
      }, () => {
        if (this.data.autoPlay) {
          setTimeout(() => this.setData({ visible: true }), 50);
        }
      });
    },

    replay() {
      const { skill, speed } = this.data;
      if (!skill) return;
      this.setData({ visible: false }, () => {
        setTimeout(() => {
          this.setData({
            visible: true,
            actualDuration: Math.round(skill.duration / speed),
          });
        }, 30);
      });
    },

    // 由外部 (e.g. detail 页控件区) 调用切换播放倍速并重播
    setSpeed(speed) {
      const { skill } = this.data;
      if (!skill) return;
      this.setData({
        speed,
        actualDuration: Math.round(skill.duration / speed),
      }, () => {
        this.replay();
      });
    },

  },
});
