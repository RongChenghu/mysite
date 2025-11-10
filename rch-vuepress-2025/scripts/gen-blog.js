// scripts/gen-blog.js
import fs from "fs";
import path from "path";
import matter from "gray-matter";
import fg from "fast-glob";

const ROOT = process.cwd();
const BLOG_DIR = path.join(ROOT, "docs/blog");
const OUT_DIR = path.join(ROOT, "docs/.vuepress/public");
const OUT_FILE = path.join(OUT_DIR, "blog-manifest.json");

(async () => {
  const files = await fg("**/*.md", { cwd: BLOG_DIR, dot: false });
  const items = [];

  for (const rel of files) {
    // 过滤掉入口页
    const base = rel.toLowerCase().replace(/\\/g, "/");
    if (base === "index.md" || base === "readme.md") continue;

    const full = path.join(BLOG_DIR, rel);
    const raw = fs.readFileSync(full, "utf8");
    const { data: fm, content } = matter(raw);

    // 取第一段作为摘要兜底
    const desc = (
      fm.description ||
      content
        .split("\n")
        .find((l) => l.trim())
        .slice(0, 160)
    ).trim();

    // 链接规则：/blog/路径 + .html
    // 假设文件名英文（你之前已规范），否则建议先重命名
    const noExt = rel.replace(/\.md$/i, "");
    const link = `/blog/${noExt}.html`;

    items.push({
      title: fm.title || noExt,
      date: fm.date || null,
      description: desc,
      tags: Array.isArray(fm.tags) ? fm.tags : fm.tags ? [fm.tags] : [],
      link,
      _order: fm.date ? new Date(fm.date).getTime() : 0,
    });
  }

  // 按日期倒序
  items.sort((a, b) => (b._order || 0) - (a._order || 0));

  fs.mkdirSync(OUT_DIR, { recursive: true });
  fs.writeFileSync(OUT_FILE, JSON.stringify(items, null, 2), "utf8");
  console.log(`✅ Generated ${OUT_FILE} with ${items.length} posts.`);
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
