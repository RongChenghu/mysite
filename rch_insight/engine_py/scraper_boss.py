import os, time, json, datetime
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from sqlalchemy import create_engine
from dotenv import load_dotenv
from scraper_common import now_iso, to_abs, upsert_job, clamp255

load_dotenv()

FAVORITES_URL = os.getenv("FAVORITES_URL", "https://www.zhipin.com/web/geek/favorite")
STORAGE_STATE = os.getenv("STORAGE_STATE", "./storage_state.json")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "")
DB_NAME = os.getenv("DB_NAME", "rch_insight")

DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

def parse_card(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    title_el = soup.select_one(".job-title, .job-name, .job-card-body .title, .title")
    company_el = soup.select_one(".company-name, .company, .info-company .name a, .company-text .name")
    link_el = soup.select_one("a[href]")
    desc_text = " ".join([x.get_text(" ", strip=True) for x in soup.select(".job-tag, .job-desc, .desc, .job-info, .info-primary")])

    job_title = (title_el.get_text(strip=True) if title_el else "")[:255]
    company = (company_el.get_text(strip=True) if company_el else "")[:255]
    href = link_el.get("href") if link_el else ""

    responsibilities = desc_text[:4000] if desc_text else ""
    requirements = ""

    # 简单关键词标签
    tags = []
    for kw in ["能源","供热","AIoT","ToB","SaaS","Node","Vue","MySQL","Python","数据分析","自动化","边缘计算"]:
        if kw in desc_text:
            tags.append(kw)

    return {
        "company_name": company,
        "job_title": job_title,
        "collected_url": href,
        "responsibilities": responsibilities,
        "requirements": requirements,
        "industry_tags": list(set(tags)),
        "raw_html": html
    }

def run():
    engine = create_engine(DB_URL, pool_pre_ping=True, future=True)
    with engine.begin() as conn:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            ctx = browser.new_context(storage_state=STORAGE_STATE)
            page = ctx.new_page()
            page.goto(FAVORITES_URL, wait_until="networkidle")

            # 适度滚动加载
            for _ in range(10):
                page.mouse.wheel(0, 2000)
                time.sleep(0.4)

            cards = page.locator(".job-card, .favorite-job-card, .job-list-box li, .job-card-wrapper").all()
            base = "https://www.zhipin.com"
            now = now_iso()
            count = 0
            for c in cards:
                html = c.inner_html()
                item = parse_card(html)
                item["source"] = "boss"
                item["collected_at"] = now
                item["collected_url"] = clamp255(to_abs(item.get("collected_url",""), base))
                try:
                    upsert_job(conn, item)
                    count += 1
                except Exception as e:
                    print("UPSERT ERROR:", e)
            browser.close()
            print(f"OK, inserted/updated: {count}")

if __name__ == "__main__":
    run()
