from app.database.session import get_supabase_client
from app.models.call.campaign import CampaignRID
from app.models.call.campaign import Campaign
from typing import List
from fastapi import HTTPException

from app.repositories.deserializer import Deserializer


class CampaignRepository:
    def __init__(self):
        self.supabase = get_supabase_client()
        self.table_name = "campaign"

    def get_campaign_by_rid(self, campaign_rid: CampaignRID) -> Campaign:
        response = self.supabase.table(self.table_name).select("*").eq("rid", campaign_rid.to_string()).execute()
        data = response.data
        if not data:
            raise HTTPException(status_code=404, detail="Campaign not found")

        return Deserializer.deserialize(data[0], Campaign)

    def create_campaign(self, campaign: Campaign) -> Campaign:
        response = self.supabase.table(self.table_name).insert(campaign.model_dump(mode="json")).execute()
        data = response.data
        if not data:
            raise HTTPException(status_code=500, detail="Failed to create campaign")

        return Deserializer.deserialize(data[0], Campaign)

    def get_all_campaigns(self) -> List[Campaign]:
        response = self.supabase.table(self.table_name).select("*").execute()
        data = response.data
        return [Deserializer.deserialize(campaign, Campaign) for campaign in data]
