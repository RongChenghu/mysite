import { defineUserConfig } from "vuepress";

import { defaultTheme } from "@vuepress/theme-default";
import { viteBundler } from "@vuepress/bundler-vite";
import { photoSwipePlugin } from "@vuepress/plugin-photo-swipe";
import { mediumZoomPlugin } from "@vuepress/plugin-medium-zoom";

export default defineUserConfig({
  lang: "zh-CN",
  title: "容成腾起 · Product Journey",
  description: "产品是逻辑的艺术，AI是想象的延伸。",
  head: [
    [
      "meta",
      { name: "viewport", content: "width=device-width, initial-scale=1.0" },
    ],
    ["link", { rel: "icon", href: "/favicon.ico" }],
  ],

  theme: defaultTheme({
    repo: "",
    editLink: false,
    lastUpdated: true,
    contributors: false,
    logo: "/img/logo.png",
    logoDark: "/img/logodark.png",

    navbar: [
      { text: "首页", link: "/" },
      { text: "项目经历", link: "/projects/" },
      { text: "博客", link: "/blog/" },
      { text: "AI 工具", link: "/ai-tools/" },
      { text: "关于", link: "/about.html" },
    ],
    sidebar: {
      "/projects/": [
        {
          text: "精选项目",
          collapsible: false,
          children: [
            "/projects/heat-platform.md",
            "/projects/payment-hub.md",
            "/projects/energy-center.md",
            "/projects/ai-picturebook.md",
            "/projects/supply.md",
            "/projects/ai-assistant.md",
          ],
        },
      ],
      "/blog/": [
        {
          text: "博客",
          children: [
            "/blog/36-open-payment-system.md",
            "/blog/32-ai-rule-engine.md",
            "/blog/27-energy-prediction-product.md",
            "/blog/34-payment-refactor.md",
            "/blog/30-supplychain-pricing-engine.md",
          ],
        },
      ],
      "/ai-tools/": [
        {
          text: "AI 工具",
          children: [
            "/ai-tools/picturebook.md",
            "/ai-tools/assistant.md",
            "/ai-tools/prompts.md",
            "/ai-tools/solution-factory.md",
            "/ai-tools/writing-companion.md",
          ],
        },
      ],
    },
  }),
  plugins: [
    photoSwipePlugin({}),
    mediumZoomPlugin({ selector: ".zoomable-images img" }),
  ],
  bundler: viteBundler({}),
});
