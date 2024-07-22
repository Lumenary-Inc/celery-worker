from app.database.session import get_supabase_client
from app.models.patient import Patient
from typing import List
from fastapi import HTTPException


class PatientRepository:
    def __init__(self):
        self.supabase = get_supabase_client()

    def get_patient_by_id(self, patient_id: int) -> Patient:
        response = self.supabase.table("patients").select("*").eq("id", patient_id).execute()
        data = response.data
        if not data:
            raise HTTPException(status_code=404, detail="Patient not found")
        return Patient(**data[0])

    def create_patient(self, patient: Patient) -> Patient:
        response = self.supabase.table("patients").insert(patient.dict(exclude_unset=True)).execute()
        data = response.data
        if not data:
            raise HTTPException(status_code=500, detail="Failed to create patient")
        return Patient(**data[0])

    def get_all_patients(self) -> List[Patient]:
        response = self.supabase.table("patients").select("*").execute()
        data = response.data
        return [Patient(**patient) for patient in data]
