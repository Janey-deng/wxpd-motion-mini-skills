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
    // 遮罩 fade-in duration: 有 orchestration 时取 maskDuration / speed (C1 modal + C2 actionsheet);
    // 无 orchestration 时 fallback 到 actualDuration (适用于 C5 popover 等)
    actualMaskDuration: 0,
    // 主动作 (modal/sheet) 入场延迟: 有 orchestration 时取 mainDelay / speed (C1+C2);
    // 无则 0; 形成"遮罩走完 90% 后主动作才启动"的组合动画节奏
    actualMainDelay: 0,
  },

  methods: {
    // 根据 speed 计算 3 个实际 timing (actualDuration + actualMaskDuration + actualMainDelay)
    // 抽出独立函数, 避免 _loadSkill / replay / setSpeed 三处重复实现
    _calcTimings(skill, speed) {
      const o = skill.orchestration;
      const dur = Math.round(skill.duration / speed);
      return {
        actualDuration: dur,
        actualMaskDuration: o ? Math.round(o.maskDuration / speed) : dur,
        actualMainDelay: o ? Math.round(o.mainDelay / speed) : 0,
      };
    },

    _loadSkill(id) {
      if (!id) return;
      const raw = catalog.getById(id);
      const skill = catalog.withEnriched(raw);
      if (!skill) return;
      this.setData({
        skill,
        visible: false,
        ...this._calcTimings(skill, this.data.speed),
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
            ...this._calcTimings(skill, speed),
          });
        }, 30);
      });
    },

    // 由外部 (e.g. detail 页控件区) 调用切换播放倍速并重播
    // 不在此处直接算 timings: 让 replay() 统一负责 timing 计算, 避免重复实现
    setSpeed(speed) {
      if (!this.data.skill) return;
      this.setData({ speed }, () => this.replay());
    },

  },
});
