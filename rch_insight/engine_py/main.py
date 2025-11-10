from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import tempfile, os, json
from resume_parser import parse_resume
from db import execute
from services import match_once

app = FastAPI(title="RCH Insight Engine")

class MatchReq(BaseModel):
    userId: int
    jobId: int

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/internal/match")
def match(req: MatchReq):
    result = match_once(req.userId, req.jobId)
    if "error" in result:
        return {"code": 404, "msg": result["error"]}
    return {"code": 0, "data": result}

@app.post("/internal/profile/upload")
async def upload_resume(userId: int, file: UploadFile = File(...)):
    tmp_path = tempfile.mktemp(suffix=os.path.splitext(file.filename)[1])
    with open(tmp_path, "wb") as f:
        f.write(await file.read())
    parsed = parse_resume(tmp_path)
    os.remove(tmp_path)
    execute("""
    INSERT INTO user_profile (user_id, skills, industries, projects)
    VALUES (:uid, :skills, :inds, :projs)
    ON DUPLICATE KEY UPDATE skills=:skills, industries=:inds, projects=:projs, updated_at=NOW()
    """, uid=userId, skills=json.dumps(parsed["skills"], ensure_ascii=False), inds=json.dumps(parsed["industries"], ensure_ascii=False), projs=json.dumps(parsed["projects"], ensure_ascii=False))
    return {"code": 0, "msg": "上传并解析成功", "data": {"skills": parsed["skills"], "industries": parsed["industries"], "projects": parsed["projects"]}}
