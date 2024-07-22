from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
import re


class TwilioService:
    def __init__(self, account_sid: str, auth_token: str, api_key: str, api_secret: str, twiml_app_sid: str,
                 twilio_number: str):
        self.client = Client(account_sid, auth_token)
        self.api_key = api_key
        self.api_secret = api_secret
        self.account_sid = account_sid
        self.twiml_app_sid = twiml_app_sid
        self.number = twilio_number

    @staticmethod
    def is_valid_phone_number(number: str) -> bool:
        return re.match(r'^[\d\+\-\(\) ]+$', number) is not None

    def generate_voice_response(self, to: str, caller_id: str) -> str:
        response = VoiceResponse()
        if to:
            dial = response.dial(answer_on_bridge=True, caller_id=caller_id)
            if self.is_valid_phone_number(to):
                dial.number(to)
            else:
                dial.client(to)
        else:
            response.say('Thanks for calling!')
        return str(response)

    def create_access_token(self, identity: str) -> str:
        token = AccessToken(self.account_sid, self.api_key, self.api_secret, identity=identity)
        grant = VoiceGrant(
            outgoing_application_sid=self.twiml_app_sid,
            incoming_allow=True
        )
        token.add_grant(grant)
        return token.to_jwt()
