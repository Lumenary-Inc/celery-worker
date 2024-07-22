from fastapi import APIRouter, Request, Response, HTTPException, WebSocket, WebSocketDisconnect, Depends, Header

from app.models.call.call_request import CallRequest
from app.repositories.call_repository import CallRepository
from app.services.twilio.twilio_service import TwilioService
from app.config import settings
from twilio.twiml.voice_response import VoiceResponse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
call_repository = CallRepository()

twilio_service = TwilioService(
    settings.TW_ACCOUNT_SID,
    settings.TW_AUTH_TOKEN,
    settings.TW_API_KEY,
    settings.TW_API_SECRET,
    settings.TW_TWIML_APP_SID,
    settings.TW_NUMBER
)


def get_twilio_service():
    return twilio_service


@router.get("/")
async def root():
    try:
        return {"message": "Welcome to the Twilio Voice API"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


"""
This is the main entryway for Twilio voice calls, inbound and outbound.
Requests come from Twilio's webhook, triggered by an inbound phone call or an outbound dial.
Through TwiML, we can control the flow of the call, such as routing streams of audio.
"""

INBOUND_OPENING_MESSAGE = "Start talking now."


@router.post("/create")
async def create():
    call: CallRequest = call_repository.create_call()
    return {"call": call}


@router.post("/voice")
async def voice(request: Request, twilio: TwilioService = Depends(get_twilio_service)):
    form_data = await request.form()
    to = form_data.get('To')
    direction = form_data.get('Direction')

    response = VoiceResponse()
    if direction == 'inbound':
        response.say(INBOUND_OPENING_MESSAGE)

        call_request: CallRequest = CallRequest
        response.connect().stream(url=f"wss://{settings.NGROK_URL}/api/ws/{rounding_call.id}/stream")
    else:
        dial = response.dial(caller_id=settings.TWILIO_NUMBER)
        if twilio.is_valid_phone_number(to):
            dial.number(to)
        else:
            dial.client(to)

    return Response(content=str(response), media_type="application/xml")


@router.get("/token")
async def get_token(twilio: TwilioService = Depends(get_twilio_service)):
    try:
        token = twilio.create_access_token("example_user")
        return {"token": token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))