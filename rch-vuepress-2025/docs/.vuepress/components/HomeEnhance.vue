<script setup>
import { withBase } from "@vuepress/client";

const profile = withBase("/img/profile.jpg"); // 可替换为你的头像

const projects = [
  {
    title: "智慧供热运营平台",
    desc: "能源中心数据中台，监控/预测/告警/调控一体化",
    cover: withBase("/img/project-heat.jpg"),
    link: "/projects/heat-platform.html",
  },
  {
    title: "聚合支付中台",
    desc: "跨境代收代付与结算路由，服务全球商户",
    cover: withBase("/img/project-pay.jpg"),
    link: "/projects/payment-hub.html",
  },
  {
    title: "供应链协同平台",
    desc: "端到端可视化链路，工厂/仓储/物流/门店协作",
    cover: withBase("/img/project-supply.jpg"),
    link: "/projects/supply.html",
  },
  {
    title: "AI个人助理平台",
    desc: "语言理解 + 知识推理 + 自动化执行的智能体",
    cover: withBase("/img/project-assistant.jpg"),
    link: "/projects/ai-assistant.html",
  },
];
</script>

<template>
  <section class="home-enhance">
    <h3 class="section-title">让逻辑有温度，让系统更懂人</h3>
    <div class="cards">
      <div class="card" v-for="p in projects" :key="p.title">
        <a :href="p.link">
          <img :src="p.cover" :alt="p.title" />
          <div class="c-body">
            <h4>{{ p.title }}</h4>
            <p>{{ p.desc }}</p>
          </div>
        </a>
      </div>
    </div>
  </section>
</template>

<style scoped>
.home-enhance {
  margin: 2.5rem 0 3rem;
  text-align: center;
}
.section-title {
  color: var(--vp-c-brand);
  margin: 10px 0 6px;
}
.section-sub {
  color: var(--vp-c-text-muted);
  margin-bottom: 1.2rem;
}
.intro {
  margin-bottom: 1rem;
}
.avatar {
  width: 84px;
  height: 84px;
  border-radius: 50%;
  border: 2px solid var(--vp-c-brand);
}

.cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
  margin-top: 10px;
}
.card {
  background: var(--vp-c-bg);
  border: 1px solid rgba(46, 110, 110, 0.12);
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.06);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.card:hover {
  transform: translateY(-6px);
  box-shadow: 0 10px 22px rgba(46, 110, 110, 0.2);
}
.card img {
  width: 100%;
  height: 150px;
  object-fit: cover;
  display: block;
}
.c-body {
  text-align: left;
  padding: 12px 14px 16px;
}
.c-body h4 {
  font-size: 16px;
}
.c-body p {
  color: var(--vp-c-text-muted);
  font-size: 14px;
  line-height: 1.5;
}

@media (max-width: 1200px) {
  .cards {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (max-width: 640px) {
  .cards {
    grid-template-columns: 1fr;
  }
  .card img {
    height: 140px;
  }
}
</style>
