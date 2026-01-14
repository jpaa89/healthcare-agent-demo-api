from datetime import date, datetime
import json
from typing import Iterable, List, Sequence, Any

import asyncpg

from app.domain.ehr_ingestion.ehr_context_models import (
    EHRContextItem,
    EHRContextSource,
)


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, (datetime, date)):
            return (
                o.isoformat()
            )  # Converts to 'YYYY-MM-DDTHH:MM:SS.microseconds' format
        return json.JSONEncoder.default(self, o)


class EhrContextsRepository:
    def __init__(self, conn: asyncpg.Connection) -> None:
        self.conn = conn

    async def insert_many(self, items: list[EHRContextItem]) -> None:
        if not items:
            return

        query = """
        INSERT INTO ehr_patient_context (
            id,
            patient_id,
            type,
            content,
            data,
            source_type,
            source_recorded_at,
            source_recorded_by,
            created_at
        )
        VALUES (
            $1, $2, $3, $4, $5, $6, $7, $8, $9
        )
        """

        async with self.conn.transaction():
            await self.conn.executemany(
                query,
                [
                    (
                        item.id,
                        item.patient_id,
                        item.type.value,
                        item.content,
                        (
                            json.dumps(item.data, default=str)
                            if item.data is not None
                            else None
                        ),
                        item.source.type.value,
                        item.source.recorded_at,
                        item.source.recorded_by,
                        item.created_at,
                    )
                    for item in items
                ],
            )

    async def delete_by_patient_id(self, patient_id: str) -> int:
        result = await self.conn.execute(
            """
            DELETE FROM
                ehr_patient_context
            WHERE
                patient_id = $1
            """,
            patient_id,
        )

        _, count = result.split()
        return int(count)

    async def list_by_patient(self, patient_id: str) -> Sequence[EHRContextItem]:
        rows = await self.conn.fetch(
            """
            SELECT *
                FROM 
                    ehr_patient_context
                WHERE 
                    patient_id = $1
            """,
            patient_id,
        )
        return [self._row_to_context_item(row) for row in rows]

    async def list_by_patient_and_types(
        self,
        patient_id: str,
        types: Iterable[str],
    ) -> list[EHRContextItem]:
        rows = await self.conn.fetch(
            """
            SELECT *
                FROM ehr_patient_context
            WHERE
                patient_id = $1
                AND type = ANY($2)
            """,
            patient_id,
            list(types),
        )
        return [self._row_to_context_item(row) for row in rows]

    @staticmethod
    def _row_to_context_item(row: asyncpg.Record) -> EHRContextItem:

        data = row["data"]

        if isinstance(data, str):
            data = json.loads(data)

        return EHRContextItem(
            id=row["id"],
            patient_id=row["patient_id"],
            type=row["type"],
            content=row["content"],
            data=data,
            source=EHRContextSource(
                type=row["source_type"],
                recorded_at=row["source_recorded_at"],
                recorded_by=row["source_recorded_by"],
            ),
            created_at=row["created_at"],
        )
