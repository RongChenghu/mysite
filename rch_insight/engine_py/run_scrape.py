#!/usr/bin/env python3
import os
from dotenv import load_dotenv

load_dotenv()
source = os.getenv("SCRAPE_SOURCE", "boss")

if source == "boss":
    import scraper_boss as m
    m.run()
else:
    raise SystemExit(f"Unknown SCRAPE_SOURCE: {source}")
