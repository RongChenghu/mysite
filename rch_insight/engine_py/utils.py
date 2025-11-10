import os, numpy as np
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")
GEN_MODEL   = os.getenv("GEN_MODEL", "gpt-4o-mini")

def cosine(a: List[float], b: List[float]) -> float:
    va, vb = np.array(a, dtype=np.float32), np.array(b, dtype=np.float32)
    denom = (np.linalg.norm(va) * np.linalg.norm(vb)) + 1e-9
    return float(np.dot(va, vb) / denom)

def embed(text: str) -> List[float]:
    text = (text or "").strip()
    if not text:
        return [0.0]
    res = client.embeddings.create(model=EMBED_MODEL, input=text)
    return res.data[0].embedding

def clamp_zh(s: str, max_chars: int = 120) -> str:
    return (s or "")[:max_chars]

def gen_message(user: Dict, job: Dict, highlights: List[str], score: float) -> Dict:
    sys = (
        "你是「RCH Insight · 职业智能助理」。"
        "输出【企业概览】【岗位分析】【匹配度】【沟通首发话术】，话术≤120字，语气自然专业。"
    )
    payload = f"""
【用户画像】
技能：{", ".join(user.get("skills", []))}
行业：{", ".join(user.get("industries", []))}
项目：{", ".join([p.get("title","") for p in user.get("projects", [])])}

【岗位信息】
公司：{job.get("company_name","")}
岗位：{job.get("job_title","")}
职责：{(job.get("responsibilities") or "")[:300]}
要求：{(job.get("requirements") or "")[:300]}

【匹配亮点】{"；".join(highlights)}
匹配分：{score:.1f}%
"""
    chat = client.chat.completions.create(
        model=GEN_MODEL,
        temperature=0.4,
        messages=[{"role": "system", "content": sys}, {"role": "user", "content": payload}],
    )
    text = chat.choices[0].message.content or ""
    message = clamp_zh(text.split("【沟通首发话术】")[-1].strip() or text.strip(), 120)
    return {"raw": text, "message": message}
