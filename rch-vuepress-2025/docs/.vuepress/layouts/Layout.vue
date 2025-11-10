
<script setup>
import ParentLayout from '@vuepress/theme-default/layouts/Layout.vue'
</script>

<template>
  <ParentLayout>
    <template #page-bottom>
      <div class="my-footer">© 2025 成于腾，智于行</div>
    </template>
  </ParentLayout>
</template>

<style>
.my-footer{ text-align:center; padding:2rem 0; opacity:.7; font-size:14px; }
</style>
