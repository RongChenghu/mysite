import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

load_dotenv()

def get_engine() -> Engine:
    url = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}?charset=utf8mb4"
    )
    engine = create_engine(url, pool_pre_ping=True, pool_size=5, max_overflow=5, future=True)
    return engine

engine = get_engine()

def fetch_one(sql: str, **params):
    with engine.connect() as conn:
        row = conn.execute(text(sql), params).mappings().first()
        return dict(row) if row else None

def execute(sql: str, **params):
    with engine.begin() as conn:
        conn.execute(text(sql), params)
