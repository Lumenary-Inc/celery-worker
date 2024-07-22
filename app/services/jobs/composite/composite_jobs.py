from celery import chain, group
from app.celery_app import celery
from app.services.jobs import call_patient_job
from app.services.jobs.pipeline.transcript.transcript_jobs import analyze_transcript_job


@celery.task
def process_campaign_calls_job(campaign_calls_data: dict):
    campaign_calls = CampaignCalls.model_validate(campaign_calls_data)
    campaign_metadata = campaign_calls.metadata

    call_tasks = group(
        chain(
            call_patient_job.s(campaign_metadata.model_dump(), patient.model_dump()).set(queue='lumenary_call_queue'),
            analyze_transcript_job.s().set(queue='lumenary_pipeline_queue')
        )
        for patient in campaign_calls.patients
    )

    print(f"{len(campaign_calls.patients)} patients processed")

    call_tasks.apply_async()
