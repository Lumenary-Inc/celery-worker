from app.database.session import get_supabase_client
from app.models.call.call_request import CallRequest, CallRequestRID
from typing import List
from fastapi import HTTPException

from app.models.call.campaign import CampaignRID


class CallRepository:
    def __init__(self):
        self.supabase = get_supabase_client()

    def get_call_request_by_rid(self, call_request_rid: CallRequestRID) -> CallRequest:
        response = self.supabase.table("calls").select("*").eq("rid", call_request_rid.to_string()).execute()
        data = response.data
        if not data:
            raise HTTPException(status_code=404, detail="Call not found")
        return CallRequest(**data[0])

    def create_call(self, call: CallRequest) -> CallRequest:
        response = self.supabase.table("calls").insert(call.model_dump()).execute()
        data = response.data
        if not data:
            raise HTTPException(status_code=500, detail="Failed to create call")
        return CallRequest(**data[0])

    def get_calls_by_campaign_rid(self, campaign_rid: CampaignRID) -> List[CallRequest]:
        response = self.supabase.table("calls").select("*").eq("campaign_rid", campaign_rid).execute()
        data = response.data
        return [CallRequest(**call) for call in data]
