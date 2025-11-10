<h1 align="center">🧭 RCH Insight Engine</h1>
<p align="center">
<b>AI 求职智能助手 · RCH Insight（求职版）</b><br>
简历上传 → 智能匹配 → 自动生成沟通话术
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg" />
  <img src="https://img.shields.io/badge/FastAPI-Framework-brightgreen.svg" />
  <img src="https://img.shields.io/badge/OpenAI-API-orange.svg" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey.svg" />
</p>

---

## 🌟 项目简介

**RCH Insight Engine** 是一款基于 **FastAPI + OpenAI + MySQL** 的智能求职引擎。  
它可以帮助你从简历中提取技能与项目经验，自动匹配招聘岗位，并生成自然专业的首发沟通话术。

---

## 🚀 功能特性

| 模块                  | 功能说明                                         |
| --------------------- | ------------------------------------------------ |
| 📂 **简历解析**       | 支持上传 PDF / DOCX 简历，提取技能、行业与项目   |
| 🧠 **智能匹配**       | 对比岗位职责与个人画像，计算语义相似度与加权分数 |
| 💬 **沟通话术生成**   | 自动生成 ≤120 字的个性化沟通语                   |
| 🕵️ **职位采集脚本**   | 采集 Boss 直聘收藏页职位，写入数据库             |
| 🧩 **API 接口化设计** | 统一 JSON 格式输出，方便前端或其他系统调用       |
| 🛡️ **配置安全隔离**   | `.env` 保护私钥，不上传敏感信息                  |

---

## ⚙️ 技术栈

- **Backend**：FastAPI + SQLAlchemy
- **Database**：MySQL 8.0+
- **AI Models**：OpenAI GPT-4 / Embedding API
- **Parsing**：pdfplumber、python-docx、jieba
- **Scraping**：Playwright + BeautifulSoup4

---

## 🧩 系统架构

```text
[Boss直聘收藏页] → [采集脚本 scraper_boss.py]
        ↓
 [MySQL job_listings]
        ↓
 [上传简历 /internal/profile/upload]
        ↓
 [简历解析 → user_profile]
        ↓
 [智能匹配 /internal/match]
        ↓
 [生成沟通话术 + 保存 match_result]
```
