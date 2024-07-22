from app.celery_app import celery
from app.models import Patient, Transcript

import random
import time
import logging

from app.models.call.campaign import CampaignRID
from app.models.hospital.encounter import EncounterRID

logger = logging.getLogger(__name__)


@celery.task
def call_patient_job(campaign_rid: CampaignRID, encounter_rid: EncounterRID) -> dict:
    logger.info(f"Calling...")
    time.sleep(random.randint(0, 5))
    logger.info(f"* Call concluded...")

    return Transcript(
        id=1,
        campaign_id=campaign_metadata.campaign_id,
        patient_id=patient.id,
        utterances=["Hello", "How are you?", "Goodbye"]
    ).model_dump()
