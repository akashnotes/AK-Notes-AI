import os, re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI

load_dotenv()
app = FastAPI(title="AK Notes AI API")

class NoteRequest(BaseModel):
    url: str
    language: str = "Hindi"
    note_type: str = "Short Notes"

def video_id(url: str):
    m = re.search(r"(?:v=|youtu\.be/|youtube\.com/shorts/)([A-Za-z0-9_-]{11})", url)
    return m.group(1) if m else None

@app.get("/health")
def health():
    return {"ok": True, "app": "AK Notes AI"}

@app.post("/notes")
def notes(req: NoteRequest):
    vid = video_id(req.url)
    if not vid:
        raise HTTPException(400, "Valid YouTube URL डालें")

    try:
        # API/library availability can vary by video; captions must be available.
        transcript = YouTubeTranscriptApi().fetch(vid)
        text = " ".join(x.text for x in transcript)
    except Exception as e:
        raise HTTPException(422, "इस वीडियो का transcript/captions उपलब्ध नहीं है।")

    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(500, "OPENAI_API_KEY backend में सेट नहीं है।")

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = f"""You are AK Notes AI, an educational note maker.
Create {req.note_type} from the transcript below.
Language: {req.language}.
Use clear headings, bullet points, definitions, examples where present, and exam-important points.
Do not invent facts not supported by the transcript.
Transcript:
{text[:120000]}
"""
    try:
        r = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            input=prompt
        )
        return {"notes": r.output_text, "video_id": vid}
    except Exception as e:
        raise HTTPException(500, f"AI generation failed: {e}")
