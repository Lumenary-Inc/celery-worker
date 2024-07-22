from app.celery_app import celery
from app.models.call.campaign import Campaign, CampaignEncountersToRequest
from app.services.matcher_service import match_encounters_to_campaign


@celery.task
def campaign_creation_job(campaign: dict) -> dict:
    campaign = Campaign(**campaign)
    encounters = match_encounters_to_campaign(campaign)

    campaign_encounters = CampaignEncountersToRequest(
        campaign_rid=campaign.rid,
        encounters=encounters
    )

    return campaign_encounters.model_dump()
