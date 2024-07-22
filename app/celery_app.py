import logging
from celery import Celery
from app.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print(f"RabbitMQ: {settings.RABBIT_MQ_USERNAME}, {settings.RABBIT_MQ_PASSWORD}")

celery = Celery(
    'worker',
    broker=f'amqp://{settings.RABBIT_MQ_USERNAME}:{settings.RABBIT_MQ_PASSWORD}@localhost:5672//',
    backend='rpc://'
)

celery.conf.update(
    task_routes={
        'app.services.jobs.composite.composite_jobs': {'queue': 'lumenary_composite_queue'},
        'app.services.jobs.campaign.campaign_jobs': {'queue': 'lumenary_campaign_queue'},
        'app.services.jobs.pipeline.transcript.transcript_jobs': {'queue': 'lumenary_pipeline_queue'},
        'app.services.jobs.pipeline.audio.audio_jobs': {'queue': 'lumenary_pipeline_queue'},
        'app.services.jobs.call.call_jobs': {'queue': 'lumenary_call_queue'}
    }
)

celery.autodiscover_tasks([
    'app.services.jobs.campaign.campaign_jobs',
    'app.services.jobs.call.call_jobs',
    'app.services.jobs.pipeline.transcript.transcript_jobs',
    'app.services.jobs.pipeline.audio.audio_jobs',
    'app.services.jobs.composite.composite_jobs',
])
