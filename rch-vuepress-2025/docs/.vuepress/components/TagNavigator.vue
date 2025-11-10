<template>
  <div class="tag-navigator">
    <!-- 左侧分类导航 -->
    <aside class="tag-sidebar">
      <ul>
        <li
          v-for="(cat, i) in categories"
          :key="cat.level_1"
          :class="{ active: activeIndex === i }"
          @click="activeIndex = i"
        >
          {{ cat.level_1 }}
        </li>
      </ul>
    </aside>

    <!-- 右侧标签展示区 -->
    <section class="tag-content">
      <div
        v-for="(sub, idx) in currentCategory.level_2"
        :key="idx"
        class="tag-block"
      >
        <h3 class="tag-title">{{ sub.name }}</h3>
        <div class="tag-list">
          <button
            v-for="(tag, j) in sub.keywords"
            :key="j"
            class="tag-btn"
            @click="handleTagClick(tag)"
          >
            #{{ tag }}
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { withBase } from "@vuepress/client";
// import categories from "./blog-tags.json"; // 刚才生成的 JSON 文件

const activeIndex = ref(0);
const res = await fetch(withBase("/blog-tags.json"), { cache: "no-store" });
const data = await res.json();
const currentCategory = computed(() => data[activeIndex.value]);

const handleTagClick = (tag) => {
  // 触发筛选或跳转逻辑，可根据你的博客结构调整
  window.location.href = `/blog?tag=${encodeURIComponent(tag)}`;
};
</script>

<style scoped>
.tag-navigator {
  display: flex;
  border-radius: 16px;
  background: #0f1115;
  border: 1px solid #1e2127;
  min-height: 480px;
  overflow: hidden;
}

/* 左侧分类导航 */
.tag-sidebar {
  width: 220px;
  background: #14161a;
  border-right: 1px solid #1f2125;
  padding: 16px 0;
}
.tag-sidebar ul {
  list-style: none;
  margin: 0;
  padding: 0;
}
.tag-sidebar li {
  padding: 14px 20px;
  font-weight: 500;
  color: #aaa;
  cursor: pointer;
  transition: all 0.2s ease;
  border-left: 3px solid transparent;
}
.tag-sidebar li:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.03);
}
.tag-sidebar li.active {
  color: #00bfff;
  background: rgba(0, 191, 255, 0.08);
  border-left: 3px solid #00bfff;
}

/* 右侧内容区 */
.tag-content {
  flex: 1;
  padding: 28px 36px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}
.tag-block {
  background: rgba(255, 255, 255, 0.02);
  padding: 20px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.06);
}
.tag-title {
  color: #fff;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
  border-left: 3px solid #00bfff;
  padding-left: 8px;
}
.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.tag-btn {
  background: rgba(255, 255, 255, 0.08);
  border: none;
  border-radius: 20px;
  padding: 6px 14px;
  font-size: 13px;
  color: #d5d5d5;
  cursor: pointer;
  transition: 0.2s ease;
}
.tag-btn:hover {
  background: #00bfff;
  color: #fff;
}
</style>
