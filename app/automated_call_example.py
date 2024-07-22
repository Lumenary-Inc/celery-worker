from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from config import settings


def call_and_speak(to_num, from_num, texts):
    client = Client(settings.TW_ACCOUNT_SID, settings.TW_AUTH_TOKEN)
    response = VoiceResponse()
    for i, text in enumerate(texts):
        voice = None

        if i % 2 == 0:
            voice = 'Polly.Amy'
        elif i % 3 == 0:
            voice = 'Polly.Joey'
        elif i % 5 == 0:
            voice = 'Polly.Matthew'
        elif i % 7 == 0:
            voice = 'Polly.Emma'
        elif i % 9 == 0:
            voice = 'Polly.Kendra'

        response.say(text, voice=voice)

    call = client.calls.create(
        to=to_num,
        from_=from_num,
        twiml=response
    )

    print(f"Call initiated with SID: {call.sid}")


jfk_speech_parts = [
    "We choose to go to the Moon in this decade and do the other things, not because they are easy, but because they are hard,",
    "because that goal will serve to organize and measure the best of our energies and skills,",
    "because that challenge is one that we are willing to accept, one we are unwilling to postpone, and one which we intend to win, and the others, too.",
    "We have vowed that we shall not see space filled with weapons of mass destruction, but with instruments of knowledge and understanding.",
    "But why, some say, the Moon? Why choose this as our goal? And they may well ask, why climb the highest mountain?",
    "Why, 35 years ago, fly the Atlantic? Why does Rice play Texas?",
    "We choose to go to the Moon. We choose to go to the Moon in this decade and do the other things, not because they are easy, but because they are hard,",
    "because that goal will serve to organize and measure the best of our energies and skills,",
    "because that challenge is one that we are willing to accept, one we are unwilling to postpone, and one which we intend to win, and the others, too.",
    "Many years ago the great British explorer George Mallory, who was to die on Mount Everest, was asked why did he want to climb it.",
    "He said, 'Because it is there.' Well, space is there, and we're going to climb it, and the Moon and the planets are there, and new hopes for knowledge and peace are there.",
    "And, therefore, as we set sail we ask God's blessing on the most hazardous and dangerous and greatest adventure on which man has ever embarked.",
    "Thank you."
]

from_phone_number = "+16506949268"
to_phone_number = "+18665097816"

if __name__ == '__main__':
    call_and_speak(to_phone_number, from_phone_number, jfk_speech_parts)
