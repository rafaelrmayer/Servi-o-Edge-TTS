import os
import re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel, Field
import edge_tts

app = FastAPI(title="Jornada de Bia - Edge TTS relay", version="1.0.0")
# Restrinja TTS_ALLOWED_ORIGINS às origens da sua aplicação em produção, separadas por vírgula.
origins = [x.strip() for x in os.getenv("TTS_ALLOWED_ORIGINS", "*").split(",") if x.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["GET", "POST", "OPTIONS"], allow_headers=["Content-Type", "Accept"])

class TTSRequest(BaseModel):
    text: str = Field(min_length=1, max_length=1200)
    voice: str = Field(default="pt-BR-FranciscaNeural", max_length=100)
    rate: int = Field(default=-8, ge=-50, le=50)
    pitch: int = Field(default=0, ge=-50, le=50)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "edge-tts-relay"}

@app.post("/api/tts")
async def synthesize(payload: TTSRequest):
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="O texto não pode ficar vazio.")
    # Permite apenas vozes portuguesas brasileiras para este app.
    if not re.fullmatch(r"pt-BR-[A-Za-z]+(?:Multilingual)?Neural", payload.voice):
        raise HTTPException(status_code=400, detail="Voz não permitida. Use uma voz pt-BR Neural.")
    try:
        communicate = edge_tts.Communicate(text, payload.voice, rate=f"{payload.rate:+d}%", pitch=f"{payload.pitch:+d}Hz")
        chunks = []
        async for chunk in communicate.stream():
            if chunk.get("type") == "audio":
                chunks.append(chunk["data"])
        audio = b"".join(chunks)
        if not audio:
            raise RuntimeError("O provedor não retornou áudio.")
        return Response(content=audio, media_type="audio/mpeg", headers={"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff"})
    except HTTPException:
        raise
    except Exception as exc:
        # Não devolve detalhes internos do provedor ao cliente.
        raise HTTPException(status_code=502, detail="Não foi possível gerar a voz online. Tente novamente.") from exc
