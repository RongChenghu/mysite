<script setup>
import { ref, computed, onMounted } from "vue";
import { withBase } from "@vuepress/client"; // 仅用于处理子路径部署；如果不想依赖也可改成纯 '/blog-manifest.json'

const posts = ref([]);
const loading = ref(true);
const activeTag = ref("全部");
const keyword = ref("");

onMounted(async () => {
  try {
    const res = await fetch(withBase("/blog-manifest.json"), {
      cache: "no-store",
    });
    posts.value = await res.json();
  } catch (e) {
    console.error("load blog-manifest.json failed:", e);
    posts.value = [];
  } finally {
    loading.value = false;
  }
});

const allTags = computed(() => {
  const set = new Set();
  posts.value.forEach((p) => (p.tags || []).forEach((t) => set.add(t)));
  return ["全部", ...Array.from(set)];
});

const filtered = computed(() => {
  const k = keyword.value.trim().toLowerCase();
  return posts.value.filter((p) => {
    const hitTag =
      activeTag.value === "全部" || (p.tags || []).includes(activeTag.value);
    const hitKw =
      !k ||
      p.title?.toLowerCase().includes(k) ||
      p.description?.toLowerCase().includes(k);
    return hitTag && hitKw;
  });
});

function fmtDate(d) {
  if (!d) return "";
  const date = new Date(d);
  if (isNaN(date.getTime())) return "";
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(
    2,
    "0"
  )}-${String(date.getDate()).padStart(2, "0")}`;
}
</script>

<template>
  <section class="blog-index">
    <h1 class="page-title">博客</h1>

    <div class="toolbar">
      <!-- <div class="tag-filter" v-if="allTags.length > 1">
        <button
          v-for="t in allTags"
          :key="t"
          class="tag-btn"
          :class="{ active: t === activeTag }"
          @click="activeTag = t"
        >
          {{ t }}
        </button>
      </div> -->

      <input
        class="search"
        v-model="keyword"
        type="search"
        placeholder="搜索标题或摘要…"
      />
    </div>
    <div v-if="loading" class="skeletons">
      <div v-for="i in 6" :key="i" class="skeleton"></div>
    </div>

    <div v-else class="grid">
      <a v-for="p in filtered" :key="p.link" :href="p.link" class="card">
        <div class="meta">
          <span class="date" v-if="p.date">{{ fmtDate(p.date) }}</span>
          <span class="tags" v-if="p.tags?.length">
            <span class="tag" v-for="t in p.tags" :key="t">{{ t }}</span>
          </span>
        </div>
        <h3 class="title">{{ p.title }}</h3>
        <p v-if="p.description" class="desc">{{ p.description }}</p>
      </a>
    </div>

    <div v-if="!loading && !filtered.length" class="no-result">暂无结果</div>
  </section>
</template>

<style scoped>
.page-title {
  /* margin: 0 0 12px; */
}
.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}
.search {
  min-width: 220px;
  padding: 8px 12px;
  border-radius: 10px;
  border: 1px solid rgba(46, 110, 110, 0.2);
  background: var(--vp-c-bg);
  outline: none;
}
.search:focus {
  border-color: var(--vp-c-brand);
  box-shadow: 0 0 0 3px rgba(61, 170, 160, 0.12);
}

.tag-filter {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.tag-btn {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 14px;
  background: var(--vp-c-bg);
  border: 1px solid rgba(46, 110, 110, 0.2);
  cursor: pointer;
  transition: all 0.2s;
}
.tag-btn:hover {
  background: rgba(61, 170, 160, 0.1);
}
.tag-btn.active {
  background: var(--vp-c-brand);
  color: #fff;
  border-color: var(--vp-c-brand);
}

.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
}
.card {
  display: block;
  padding: 16px 18px;
  border-radius: 12px;
  background: var(--vp-c-bg);
  border: 1px solid rgba(46, 110, 110, 0.12);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.25s;
}
.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 22px rgba(46, 110, 110, 0.18);
}
.title {
  /* margin: 6px 0 8px; */
  font-size: 18px;
  line-height: 1.35;
}
.desc {
  color: var(--vp-c-text-muted);
  font-size: 14px;
  line-height: 1.65;
}
.meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: var(--vp-c-text-muted);
  font-size: 12px;
}
.tags {
  display: inline-flex;
  gap: 6px;
}
.tag {
  padding: 2px 8px;
  border-radius: 999px;
  background: rgba(61, 170, 160, 0.12);
  color: var(--vp-c-brand);
}

.skeletons {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
}
.skeleton {
  height: 120px;
  border-radius: 12px;
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

@media (max-width: 1100px) {
  .grid,
  .skeletons {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (max-width: 640px) {
  .grid,
  .skeletons {
    grid-template-columns: 1fr;
  }
}
</style>
