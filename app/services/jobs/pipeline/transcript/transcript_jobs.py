from app.celery_app import celery
from app.models.transcript import Transcript
from app.config import logger
import time
import random


@celery.task
def analyze_transcript_job(transcript_data: dict) -> None:
    if transcript_data is None:
        return

    transcript = Transcript.model_validate(transcript_data)
    logger.info(f"***** Analyzing transcript for patient: {transcript.patient_id}")
    time.sleep(random.randint(0, 5))
    logger.info("*Transcript analysis complete*")
