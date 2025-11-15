from __future__ import annotations

from datetime import datetime, timezone
from typing import List

from db.db_connector import get_firestore
from src.models.category import CategoryCreate, CategoryInDB

class CategoryRepo:
    def __init__(self, client=None):
        self.client = client or get_firestore()

    def _collection(self):
        return self.client.collection("categories")

    def list(self) -> List[CategoryInDB]:
        docs = self._collection().order_by("name").stream()
        items: List[CategoryInDB] = []
        for doc in docs:
            data = doc.to_dict() or {}
            items.append(
                CategoryInDB(
                    id=doc.id,
                    name=data.get("name", ""),
                    type=data.get("type", "expense"),
                    color=data.get("color"),
                    is_system=data.get("is_system", True),
                    created_at=data.get("created_at"),
                    updated_at=data.get("updated_at"),
                )
            )
        return items

    def create(self, payload: CategoryCreate) -> CategoryInDB:
        now = datetime.now(timezone.utc)
        data = {
            "name": payload.name,
            "type": payload.type,
            "color": payload.color,
            "is_system": payload.is_system,
            "created_at": now,
            "updated_at": now,
        }
        doc_ref = self._collection().document()
        doc_ref.set(data)
        return CategoryInDB(
            id=doc_ref.id,
            created_at=now,
            updated_at=now,
            **payload.model_dump(),
        )

    def delete(self, category_id: str) -> bool:
        doc_ref = self._collection().document(category_id)
        if not doc_ref.get().exists:
            return False
        doc_ref.delete()
        return True