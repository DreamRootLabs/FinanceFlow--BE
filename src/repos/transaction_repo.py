from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

from google.cloud import firestore

from db.db_connector import get_firestore
from src.models.transaction import TransactionCreate, TransactionInDB

class TransactionRepo:
    def __init__(self, client=None):
        self.client = client or get_firestore()

    def _collection(self):
        return self.client.collection("transactions")

    def list_for_owner(self, owner_id: str) -> List[TransactionInDB]:
        docs = (
            self._collection()
            .where("owner_id", "==", owner_id)
            # .order_by("occurred_at")
            .stream()
        )
        items: List[TransactionInDB] = []
        for doc in docs:
            data = doc.to_dict() or {}
            items.append(
                TransactionInDB(
                    id=doc.id,
                    owner_id=owner_id,
                    amount=data["amount"],
                    type=data["type"],
                    category_id=data["category_id"],
                    description=data.get("description"),
                    occurred_at=data["occurred_at"],
                    created_at=data["created_at"],
                    updated_at=data["updated_at"],
                )
            )
        return items

    def create_for_owner(
        self,
        owner_id: str,
        payload: TransactionCreate,
    ) -> TransactionInDB:
        now = datetime.now(timezone.utc)
        data = {
            "owner_id": owner_id,
            "amount": payload.amount,
            "type": payload.type,
            "category_id": payload.category_id,
            "description": payload.description,
            "occurred_at": payload.occurred_at,
            "created_at": now,
            "updated_at": now,
        }
        doc_ref = self._collection().document()
        doc_ref.set(data)
        return TransactionInDB(
            id=doc_ref.id,
            owner_id=owner_id,
            created_at=now,
            updated_at=now,
            **payload.model_dump(),
        )
    
    def list_for_owner_between(
        self,
        owner_id: str,
        start: datetime,
        end: datetime,
    ) -> List[Dict[str, Any]]:
        """
        Return all transactions for an owner where transaction_date is between [start, end).
        Assumes you store a timestamp field like 'transaction_date' or 'date'.
        """
        # 🔧 IMPORTANT: if your field is called something else (e.g. "date" or "occurred_at"),
        # change "transaction_date" below to match.
        field_name = "occurred_at"

        query = (
            self._collection()
            .where("owner_id", "==", owner_id)
            .where(field_name, ">=", start)
            .where(field_name, "<", end)
            .order_by(field_name)
        )

        docs = query.stream()
        results: List[Dict[str, Any]] = []
        
        for doc in docs:
            data = doc.to_dict() or {}
            data["id"] = doc.id
            results.append(data)

        return results