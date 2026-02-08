from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from services.chatbot import chatbot_reply

router = APIRouter()

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
