import json
from aio_pika.abc import AbstractIncomingMessage

from app.models.call.campaign import Campaign
from app.models.patient import Patient


class CampaignService:

    @staticmethod
    def get_campaign_id_from(message: AbstractIncomingMessage):
        # todo: hack
        message_body = message.body.decode('utf-8')
        patient_data = json.loads(message_body)
        return patient_data[0][0]["campaign_id"]

    @staticmethod
    def patient_meets_criteria(patient: Patient, campaign: Campaign) -> bool:
        return False
