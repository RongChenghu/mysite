
<template>
  <div class="ai-tool">
    <h3>AI 绘本生成器（示例）</h3>
    <p>输入主题、主角与地点，点击生成预览。</p>
    <form @submit.prevent="generate">
      <input v-model="form.topic" placeholder="主题，如：腾冲奇遇记" />
      <input v-model="form.hero" placeholder="主角，如：暄暄和小汪汪" />
      <input v-model="form.place" placeholder="地点，如：云南火山公园" />
      <button :disabled="loading">{{ loading ? '生成中...' : '生成预览' }}</button>
    </form>
    <div v-if="img" class="preview">
      <img :src="img" alt="preview"/>
    </div>
    <p class="tip">* 当前为前端占位示例，实际项目请对接 /api/picturebook。</p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
const form = ref({ topic:'', hero:'', place:'' })
const img = ref<string | null>(null)
const loading = ref(false)

async function generate(){
  loading.value = true
  try{
    // 占位：随机图模拟
    const q = encodeURIComponent(form.value.topic || 'storybook')
    img.value = `https://picsum.photos/seed/${q}/800/500`
  }finally{
    loading.value = false
  }
}
</script>

<style scoped>
.ai-tool{ display:grid; gap:12px; }
form{ display:flex; gap:8px; flex-wrap:wrap }
input{ padding:8px 10px; border:1px solid #ddd; border-radius:6px; flex:1; min-width:200px }
button{ padding:8px 14px; border-radius:8px; border:none; background:var(--c-brand); color:#fff; cursor:pointer }
.preview{ margin-top:12px }
.preview img{ max-width:100%; border-radius:8px; border:1px solid #eee }
.tip{ opacity:.7; font-size:12px }
</style>
