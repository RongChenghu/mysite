<script setup>
import { ref, onMounted } from "vue";
import { usePagesData } from "@vuepress/client";

const pagesData = usePagesData();
const posts = ref([]);
const loading = ref(true);

function toDateStr(v) {
  if (!v) return "";
  const d = typeof v === "number" ? new Date(v) : new Date(String(v));
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const dd = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${dd}`;
}

onMounted(async () => {
  const list = [];
  const pd = pagesData.value;

  for (const key in pd) {
    const load = pd[key];
    if (typeof load !== "function") continue;
    const page = await load();
    // 仅收集 /blog/ 下的文章，排除列表页本身
    if (
      !page?.path?.startsWith("/blog/") ||
      page.path === "/blog/" ||
      page.path === "/blog/index.html"
    )
      continue;

    const fm = page.frontmatter || {};
    const desc =
      fm.description ||
      (page.excerpt
        ? String(page.excerpt)
            .replace(/<[^>]+>/g, "")
            .trim()
        : "");
    const dateNum = fm.date
      ? new Date(fm.date).getTime()
      : page.git?.createdTime || 0;

    list.push({
      title: fm.title || page.title || "未命名文章",
      link: page.path,
      date: toDateStr(fm.date || page.git?.createdTime),
      description: desc,
      tags: fm.tags || [],
      _order: isNaN(dateNum) ? 0 : dateNum,
    });
  }

  // 按日期倒序
  list.sort((a, b) => b._order - a._order);
  posts.value = list;
  loading.value = false;
});
</script>

<template>
  <section class="blog-index">
    <h1 class="page-title">博客</h1>

    <div v-if="loading" class="skeletons">
      <div v-for="i in 6" :key="i" class="skeleton"></div>
    </div>

    <div v-else class="grid">
      <a v-for="p in posts" :key="p.link" :href="p.link" class="card">
        <div class="meta">
          <span class="date" v-if="p.date">{{ p.date }}</span>
          <span class="tags" v-if="p.tags.length">
            <span class="tag" v-for="t in p.tags" :key="t">{{ t }}</span>
          </span>
        </div>
        <h3 class="title">{{ p.title }}</h3>
        <p v-if="p.description" class="desc">{{ p.description }}</p>
      </a>
    </div>
  </section>
</template>

<style scoped>
.page-title {
  margin: 0 0 12px;
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
  transition: all 0.25s ease;
}
.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 22px rgba(46, 110, 110, 0.18);
}
.title {
  margin: 6px 0 8px;
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
