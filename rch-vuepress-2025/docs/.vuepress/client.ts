import { defineClientConfig } from "vuepress/client";
import Layout from "./layouts/Layout.vue";
import HomeEnhance from "./components/HomeEnhance.vue";
import ArticleList from "./components/ArticleList.vue";
import BlogIndexWithTags from "./components/BlogIndexWithTags.vue";
import TagNavigator from "./components/TagNavigator.vue";
export default defineClientConfig({
  layouts: { Layout },
  enhance({ app }) {
    app.component("HomeEnhance", HomeEnhance);
    app.component("ArticleList", ArticleList);
    app.component("BlogIndexWithTags", BlogIndexWithTags);
    app.component("TagNavigator", TagNavigator);
  },
});
