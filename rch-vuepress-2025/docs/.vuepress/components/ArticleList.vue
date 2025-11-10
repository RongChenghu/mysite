<script setup>
import { ref, onMounted } from "vue";
import { withBase } from "@vuepress/client";

const items = ref([]);
const loading = ref(true);

onMounted(async () => {
  try {
    const res = await fetch(withBase("/articles.json"), { cache: "no-store" });
    const data = await res.json();
    // 只取最近 6 篇
    items.value = (data || []).slice(0, 6);
  } catch (e) {
    // 兜底：给一条示例
    items.value = [
      {
        title: "我如何设计聚合支付平台的多商户与对账体系",
        date: "2025-11-01",
        link: "/blog/36-open-payment-system.html",
        summary: "从内部系统到平台化开放，我如何重新设计聚合支付的对账与多商户账务体系。",
      },
    ];
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div class="thoughts">
    <div v-if="loading" class="skeletons">
      <div v-for="i in 3" :key="i" class="skeleton"></div>
    </div>

    <div v-else class="grid">
      <a v-for="post in items" :key="post.link" class="card" :href="post.link">
        <div class="meta">
          <span class="date">{{ post.date }}</span>
        </div>
        <h4>{{ post.title }}</h4>
        <p class="sum" v-if="post.summary">{{ post.summary }}</p>
      </a>
    </div>
  </div>
</template>

<style scoped>
.thoughts {
  margin: 1rem 0 2rem;
}
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
}
.card {
  display: block;
  padding: 14px 16px;
  border-radius: 10px;
  background: var(--vp-c-bg);
  border: 1px solid rgba(46, 110, 110, 0.12);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
  transition: all 0.25s ease;
}
.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(46, 110, 110, 0.18);
}
.meta {
  font-size: 12px;
  color: var(--vp-c-text-muted);
  margin-bottom: 6px;
}
.sum {
  color: var(--vp-c-text-muted);
  margin-top: 6px;
  font-size: 14px;
  line-height: 1.6;
}

/* skeleton */
.skeletons {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
}
.skeleton {
  height: 82px;
  border-radius: 10px;
  background: linear-gradient(90deg, #e7eceb, #f2f5f4, #e7eceb);
  animation: pulse 1.2s infinite;
}
@keyframes pulse {
  0% {
    opacity: 0.7;
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0.7;
  }
}

@media (max-width: 960px) {
  .grid,
  .skeletons {
    grid-template-columns: 1fr;
  }
}
</style>
