/**
 * 迁移旧 VuePress 站点的 Markdown 与图片到新结构
 * 用法：node scripts/migrate-old-site.js /path/to/old-site /path/to/new-site
 */

import fs from "fs-extra";
import path from "path";

const [,, oldRoot, newRoot] = process.argv;

if (!oldRoot || !newRoot) {
  console.error("❌ 用法：node scripts/migrate-old-site.js <旧站路径> <新站路径>");
  process.exit(1);
}

async function migrate() {
  console.log(`🚀 开始迁移旧站：${oldRoot}`);
  console.log(`➡️ 目标目录：${newRoot}`);

  const oldDocs = path.join(oldRoot, "docs");
  const newDocs = path.join(newRoot, "docs");

  const map = [
    { from: "blog", to: "blog" },
    { from: "projects", to: "projects" },
  ];

  for (const { from, to } of map) {
    const srcDir = path.join(oldDocs, from);
    const destDir = path.join(newDocs, to);
    if (fs.existsSync(srcDir)) {
      await fs.ensureDir(destDir);
      const files = await fs.readdir(srcDir);
      for (const file of files.filter(f => f.endsWith(".md"))) {
        const srcFile = path.join(srcDir, file);
        const destFile = path.join(destDir, file);
        let content = await fs.readFile(srcFile, "utf8");

        // 调整 Front-matter：补全日期与作者字段
        content = content.replace(/^---\s*[\s\S]*?---\s*/m, match => {
          if (match.includes("author")) return match;
          const date = new Date().toISOString().split("T")[0];
          return `${match.trim()}\nauthor: 容成呼\ndate: ${date}\n---\n\n`;
        });

        // 修复图片相对路径
        content = content.replace(/\(\.\.\/\.vuepress\/public\/img\//g, "(/img/");

        await fs.writeFile(destFile, content, "utf8");
        console.log(`✅ ${file} 已迁移`);
      }
    }
  }

  // 拷贝图片目录
  const oldImg = path.join(oldDocs, ".vuepress/public/img");
  const newImg = path.join(newDocs, ".vuepress/public/img");
  if (fs.existsSync(oldImg)) {
    await fs.ensureDir(newImg);
    await fs.copy(oldImg, newImg);
    console.log(`🖼️ 图片资源已复制到 ${newImg}`);
  }

  console.log("🎉 所有 Markdown 与图片迁移完成！");
}

migrate().catch(err => console.error("❌ 出错：", err));
