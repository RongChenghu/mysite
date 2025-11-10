import os, time, datetime, json
from urllib.parse import urljoin, urlparse

def now_iso():
    return datetime.datetime.utcnow().isoformat() + "Z"

def to_abs(url: str, base: str):
    if not url:
        return ""
    if url.startswith("http"):
        return url
    return urljoin(base, url)

def clamp255(s: str) -> str:
    return (s or "")[:255]

def upsert_job(conn, item: dict):
    from sqlalchemy import text
    sql = text("""
    INSERT INTO job_listings
      (source, company_name, job_title, responsibilities, requirements, industry_tags, collected_url, collected_at, raw_html)
    VALUES
      (:source, :company_name, :job_title, :responsibilities, :requirements, :industry_tags, :collected_url, :collected_at, :raw_html)
    ON DUPLICATE KEY UPDATE
      company_name=VALUES(company_name),
      job_title=VALUES(job_title),
      responsibilities=VALUES(responsibilities),
      requirements=VALUES(requirements),
      industry_tags=VALUES(industry_tags),
      collected_at=VALUES(collected_at),
      raw_html=VALUES(raw_html)
    """)
    item["industry_tags"] = json.dumps(item.get("industry_tags") or [], ensure_ascii=False)
    item["collected_url"] = clamp255(item.get("collected_url",""))
    conn.execute(sql, item)
    conn.commit()
