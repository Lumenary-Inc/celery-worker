from typing import List
from app.models.call.campaign import Campaign
from app.models.hospital.encounter import EncounterRID
from app.models.patient import Patient
from app.repositories.patient_repository import PatientRepository


def match_encounters_to_campaign(campaign: Campaign) -> List[EncounterRID]:
    patients_db = PatientRepository()
    all_patients: List[Patient] = patients_db.get_all_patients()

    return []
