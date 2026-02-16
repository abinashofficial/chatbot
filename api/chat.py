from fastapi import APIRouter, Request, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from services.chatbot import chatbot_reply
import os
import tempfile
import whisper

router = APIRouter()
model = whisper.load_model("tiny")  # You can use tiny, base, small, medium, large


@router.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()

    message = data.get("message", "")
    vendor_id = data.get("vendorId", "")  # from React

    reply, confidence = chatbot_reply(message, vendor_id)
    msg = ""
    form = None
    if type(reply)==str:
        msg = reply
    else:
        msg = reply["message"]
        form = reply["form"]

    return JSONResponse({
        "response": {
            "message":msg,
            "form":form,
            },
        "confidence": confidence

    })


@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    tmp_path = None

    try:
        # Save uploaded WebM file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
            tmp_path = tmp.name
            content = await file.read()
            tmp.write(content)
            tmp.flush()

        # Whisper handles WebM/Opus internally
        result = model.transcribe(tmp_path, fp16=False)

        return {"text": result["text"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
