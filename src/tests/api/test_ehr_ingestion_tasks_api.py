from http import HTTPStatus
from typing import Any

import pytest
from httpx import AsyncClient


EHR_PAYLOAD_1: dict[str, Any] = {
    "patient_id": "P001",
    "demographics": {
        "name": "Juan Pérez",
        "age": 45,
        "gender": "M",
        "blood_type": "O+",
    },
    "medical_history": {
        "chronic_conditions": ["Diabetes Tipo 2", "Hipertensión"],
        "allergies": ["Penicilina"],
        "current_medications": [
            {"name": "Metformina", "dose": "850mg", "frequency": "2x/día"},
            {"name": "Losartán", "dose": "50mg", "frequency": "1x/día"},
        ],
    },
    "recent_visits": [
        {
            "date": "2024-10-15",
            "reason": "Control rutinario",
            "notes": "Glucosa en ayunas: 128 mg/dL. PA: 135/85. Se ajusta dosis de Losartán.",
            "doctor": "Dra. Martínez",
        },
        {
            "date": "2024-08-20",
            "reason": "Consulta por mareos",
            "notes": "Paciente reporta mareos ocasionales. Se solicitan estudios. ECG normal.",
            "doctor": "Dr. Gómez",
        },
    ],
    "lab_results": [
        {
            "date": "2024-10-10",
            "test": "Panel metabólico",
            "results": {
                "glucose": "128 mg/dL",
                "hba1c": "7.2%",
                "creatinine": "1.1 mg/dL",
            },
        }
    ],
}

EXPECTED_DEMOGRAPHICS: dict[str, Any] = {
    "patient_id": "P001",
    "type": "demographics",
    "content": "Juan Pérez, 45 years old, gender M, blood type O+",
    "data": {
        "name": "Juan Pérez",
        "age": 45,
        "gender": "M",
        "blood_type": "O+",
    },
    "source": {
        "type": "demographics",
        "recorded_at": None,
        "recorded_by": None,
    },
}

EXPECTED_CHRONIC_CONDITIONS: list[dict[str, Any]] = [
    {
        "patient_id": "P001",
        "type": "chronic_condition",
        "content": "Diabetes Tipo 2",
        "data": {"condition": "Diabetes Tipo 2"},
        "source": {
            "type": "medical_history",
            "recorded_at": None,
            "recorded_by": None,
        },
    },
    {
        "patient_id": "P001",
        "type": "chronic_condition",
        "content": "Hipertensión",
        "data": {"condition": "Hipertensión"},
        "source": {
            "type": "medical_history",
            "recorded_at": None,
            "recorded_by": None,
        },
    },
]

EXPECTED_ALLERGIES: list[dict[str, Any]] = [
    {
        "patient_id": "P001",
        "type": "allergy",
        "content": "Allergy to Penicilina",
        "data": {"allergy": "Penicilina"},
        "source": {
            "type": "medical_history",
            "recorded_at": None,
            "recorded_by": None,
        },
    },
]

EXPECTED_MEDICATIONS: list[dict[str, Any]] = [
    {
        "patient_id": "P001",
        "type": "medication",
        "content": "Metformina, 850mg, 2x/día",
        "data": {
            "name": "Metformina",
            "dose": "850mg",
            "frequency": "2x/día",
        },
        "source": {
            "type": "medical_history",
            "recorded_at": None,
            "recorded_by": None,
        },
    },
    {
        "patient_id": "P001",
        "type": "medication",
        "content": "Losartán, 50mg, 1x/día",
        "data": {
            "name": "Losartán",
            "dose": "50mg",
            "frequency": "1x/día",
        },
        "source": {
            "type": "medical_history",
            "recorded_at": None,
            "recorded_by": None,
        },
    },
]

EXPECTED_VISITS: list[dict[str, Any]] = [
    {
        "patient_id": "P001",
        "type": "visit",
        "content": "Control rutinario. Glucosa en ayunas: 128 mg/dL. PA: 135/85. Se ajusta dosis de Losartán.",
        "data": {
            "date": "2024-10-15",
            "reason": "Control rutinario",
            "notes": "Glucosa en ayunas: 128 mg/dL. PA: 135/85. Se ajusta dosis de Losartán.",
            "doctor": "Dra. Martínez",
        },
        "source": {
            "type": "doctor",
            "recorded_at": "2024-10-15",
            "recorded_by": "Dra. Martínez",
        },
    },
    {
        "patient_id": "P001",
        "type": "visit",
        "content": "Consulta por mareos. Paciente reporta mareos ocasionales. Se solicitan estudios. ECG normal.",
        "data": {
            "date": "2024-08-20",
            "reason": "Consulta por mareos",
            "notes": "Paciente reporta mareos ocasionales. Se solicitan estudios. ECG normal.",
            "doctor": "Dr. Gómez",
        },
        "source": {
            "type": "doctor",
            "recorded_at": "2024-08-20",
            "recorded_by": "Dr. Gómez",
        },
    },
]

EXPECTED_LAB_RESULTS: list[dict[str, Any]] = [
    {
        "patient_id": "P001",
        "type": "lab_result",
        "content": "Lab Test - Panel metabólico: glucose=128 mg/dL, hba1c=7.2%, creatinine=1.1 mg/dL",
        "data": {
            "date": "2024-10-10",
            "test": "Panel metabólico",
            "results": {
                "glucose": "128 mg/dL",
                "hba1c": "7.2%",
                "creatinine": "1.1 mg/dL",
            },
        },
        "source": {
            "type": "lab_test",
            "recorded_at": "2024-10-10",
            "recorded_by": None,
        },
    },
]


@pytest.mark.asyncio
async def test_ehr_contexts_created_as_expected(
    client: AsyncClient,
) -> None:
    # 1. Ingest EHR
    ingest_response = await client.post(
        "/api/ehr-ingestion-tasks",
        json=EHR_PAYLOAD_1,
    )
    assert ingest_response.status_code == HTTPStatus.CREATED

    patient_id = EHR_PAYLOAD_1["patient_id"]

    # 2. Retrieve contexts for patient (using the other api here is not ideal, but it should be ok for the scope of the demo)
    response = await client.get(
        "/api/ehr-context-items",
        params={"patient_id": patient_id},
    )

    assert response.status_code == HTTPStatus.OK

    payload = response.json()
    items = payload["items"]

    items = [normalize_item(item) for item in items]

    assert len(items) > 0

    # 3. Basic sanity checks
    assert len(items) == 9

    for item in items:
        assert item["patient_id"] == patient_id
        assert "type" in item
        assert "source" in item

    # 4. Assert counts by type
    counts = count_by_type(items)

    assert counts["demographics"] == 1
    assert counts["chronic_condition"] == 2
    assert counts["allergy"] == 1
    assert counts["medication"] == 2
    assert counts["visit"] == 2
    assert counts["lab_result"] == 1

    assert_item_present(items, EXPECTED_DEMOGRAPHICS)

    for expected_condition in EXPECTED_CHRONIC_CONDITIONS:
        assert_item_present(items, expected_condition)

    for expected_visit in EXPECTED_VISITS:
        assert_item_present(items, expected_visit)

    for expected_allergy in EXPECTED_ALLERGIES:
        assert_item_present(items, expected_allergy)

    for expected_medication in EXPECTED_MEDICATIONS:
        assert_item_present(items, expected_medication)

    for expected_lab_result in EXPECTED_LAB_RESULTS:
        assert_item_present(items, expected_lab_result)


def count_by_type(items: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        counts[item["type"]] = counts.get(item["type"], 0) + 1
    return counts


def normalize_item(item: dict[str, Any]) -> dict[str, Any]:
    item = dict(item)
    item.pop("id", None)
    item.pop("created_at", None)
    return item


def assert_item_present(
    items: list[dict[str, Any]],
    expected: dict[str, Any],
) -> None:
    for item in items:
        if item == expected:
            return
    raise AssertionError(f"Expected item not found:\n{expected}")
