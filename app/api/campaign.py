from fastapi import APIRouter, HTTPException, BackgroundTasks

from app.models.call.campaign import Campaign
from app.repositories.campaign_repository import CampaignRepository
from app.services.campaign_service import CampaignService
from app.services.jobs.campaign.campaign_jobs import campaign_creation_job
from app.services.jobs.composite.composite_jobs import process_campaign_calls_job
from celery import chain

from app.services.queue_service import remove_jobs_with_campaign_id

router = APIRouter()
campaigns_db = CampaignRepository()
campaign_service = CampaignService()


@router.post("/campaign")
async def create_campaign_endpoint(campaign: dict):
    try:
        campaign = Campaign(**campaign)

        campaign = campaigns_db.create_campaign(campaign)

        chain(
            campaign_creation_job.s(campaign.model_dump()).set(queue='lumenary_campaign_queue'),
            process_campaign_calls_job.s().set(queue='lumenary_composite_queue')
        ).apply_async()

        return {"message": "Campaign created successfully", "id": campaign.rid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/campaign/{campaign_id}")
async def delete_campaign(campaign_id: int, background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(remove_jobs_with_campaign_id, "lumenary_call_queue", campaign_id)
        return {"message": f"Campaign {campaign_id} deletion completed."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
