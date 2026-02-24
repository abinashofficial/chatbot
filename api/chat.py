from fastapi import APIRouter, Request, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from services.chatbot import chatbot_reply
import os
import tempfile
from faster_whisper import WhisperModel

router = APIRouter()
# model = whisper.load_model("tiny")  # You can use tiny, base, small, medium, large
model = WhisperModel("tiny", device="cpu", compute_type="int8")



@router.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    q = ""

    message = data.get("message", "")
    vendor_id = data.get("vendorId", "")  # from React

    reply, confidence, q = chatbot_reply(message, vendor_id)
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
        "confidence": confidence,
        "keyword":q

    })


@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    tmp_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
            tmp_path = tmp.name
            content = await file.read()
            tmp.write(content)

        segments, info = model.transcribe(tmp_path)

        text = "".join([segment.text for segment in segments])

        return {"text": text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
