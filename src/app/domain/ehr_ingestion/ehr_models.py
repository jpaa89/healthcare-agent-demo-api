import datetime
from typing import Dict, List
from uuid import UUID

from pydantic import BaseModel


class Demographics(BaseModel):
    name: str
    age: int
    gender: str
    blood_type: str


class Medication(BaseModel):
    name: str
    dose: str
    frequency: str


class MedicalHistory(BaseModel):
    chronic_conditions: List[str]
    allergies: List[str]
    current_medications: List[Medication]


class Visit(BaseModel):
    date: datetime.date
    reason: str
    notes: str
    doctor: str


class LabResult(BaseModel):
    date: datetime.date
    test: str
    results: Dict[str, str]


class ElectronicPatientRecord(BaseModel):
    patient_id: str
    demographics: Demographics
    medical_history: MedicalHistory
    recent_visits: List[Visit]
    lab_results: List[LabResult]
