import os, re, jieba, pdfplumber
from docx import Document
from typing import Dict, List

COMMON_SKILLS = ["产品经理","需求分析","原型设计","Axure","PRD","项目管理","Vue","Node","MySQL","Python","Java","AI","数据分析","ToB","能源","供热","AIoT","自动化","SaaS","IoT"]
INDUSTRY_WORDS = ["能源","供热","智慧城市","政务","AI","工业互联网","财税","支付","供应链","跨境"]

def extract_text(file_path: str) -> str:
    if file_path.lower().endswith(".pdf"):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    elif file_path.lower().endswith(".docx"):
        doc = Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])
    else:
        raise ValueError("仅支持 PDF / DOCX 文件")

def extract_skills(text: str) -> List[str]:
    skills = [w for w in COMMON_SKILLS if w in text]
    words = jieba.lcut(text)
    for w in words:
        if len(w) > 1 and w not in skills:
            skills.append(w)
    return list(set(skills))[:20]

def extract_industries(text: str) -> List[str]:
    found = [w for w in INDUSTRY_WORDS if w in text]
    return list(set(found))

def extract_projects(text: str) -> List[Dict]:
    blocks = re.split(r"[项目经历|项目名称|项目描述]+", text)
    projects = []
    for blk in blocks:
        blk = blk.strip()
        if len(blk) < 20: continue
        title = blk.split("\n")[0][:30]
        desc = blk[:200]
        projects.append({"title": title, "desc": desc, "tags": []})
        if len(projects) >= 5: break
    return projects

def parse_resume(file_path: str) -> Dict:
    text = extract_text(file_path)
    return {"skills": extract_skills(text), "industries": extract_industries(text), "projects": extract_projects(text), "text": text[:1000]}
