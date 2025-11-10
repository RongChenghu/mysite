# RCH Insight Engine — Scraper 使用说明

本目录提供 **招聘网站收藏页采集** 脚本（目前内置 Boss 直聘），功能：
- 使用 Playwright 读取你的“已收藏职位”列表；
- 解析公司、岗位、描述标签等；
- 写入 MySQL 的 `job_listings`（已做 upsert）。

## 1) 额外依赖安装
在项目根目录执行：
```bash
pip install playwright beautifulsoup4 lxml
python -m playwright install
```

> Windows/Mac M1 也一样；若无法联网安装浏览器，请参考 Playwright 文档使用离线包。

## 2) 环境变量
在 `.env` 中新增或覆盖：
```
# 采集配置
SCRAPE_SOURCE=boss
FAVORITES_URL=https://www.zhipin.com/web/geek/favorite
STORAGE_STATE=./storage_state.json   # 你的已登录状态文件
```

如何获得 `storage_state.json`？
- 运行 `playwright codegen https://www.zhipin.com` 登录后保存状态，或参考官方示例；
- 也可自写一段登录脚本保存 `context.storage_state(path=...)`。

## 3) 运行采集
```bash
python run_scrape.py
```
运行结束后，控制台会输出 `OK, inserted/updated: N`。数据已写入 `job_listings` 表。

## 4) 定时任务（示例）
- crontab：每 30 分钟采集一次
```
*/30 * * * * cd /path/to/rch_insight_engine && /usr/bin/python3 run_scrape.py >> logs/scrape.log 2>&1
```
- 或使用 APScheduler/Celery 在 Python 服务里统一调度。
