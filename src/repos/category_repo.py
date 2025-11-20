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

    # -----------------------------
    # LIST: system categories + user categories
    # -----------------------------
    def list_for_owner(self, owner_id: str) -> List[CategoryInDB]:
        col = self._collection()

        # System/global categories
        system_docs = col.where("is_system", "==", True).stream()

        # User-owned categories
        user_docs = col.where("owner_id", "==", owner_id).stream()

        items: List[CategoryInDB] = []

        for doc in list(system_docs) + list(user_docs):
            data = doc.to_dict() or {}
            items.append(
                CategoryInDB(
                    id=doc.id,
                    name=data.get("name", ""),
                    type=data.get("type", "expense"),
                    color=data.get("color"),
                    is_system=data.get("is_system", True),
                    owner_id=data.get("owner_id"),
                    created_at=data.get("created_at"),
                    updated_at=data.get("updated_at"),
                )
            )

        # Sort alphabetically AFTER combining
        items.sort(key=lambda c: c.name.lower())
        return items

    # -----------------------------
    # CREATE: user category only
    # -----------------------------
    def create_for_owner(self, owner_id: str, payload: CategoryCreate) -> CategoryInDB:
        now = datetime.now(timezone.utc)

        data = {
            "name": payload.name,
            "type": payload.type,
            "color": payload.color,
            "is_system": False,
            "owner_id": owner_id,
            "created_at": now,
            "updated_at": now,
        }

        doc_ref = self._collection().document()
        doc_ref.set(data)

        return CategoryInDB(
            id=doc_ref.id,
            name=payload.name,
            type=payload.type,
            color=payload.color,
            is_system=False,
            owner_id=owner_id,
            created_at=now,
            updated_at=now,
        )

    # -----------------------------
    # DELETE: only allow deleting user-owned categories
    # -----------------------------
    def delete_for_owner(self, owner_id: str, category_id: str) -> bool:
        doc_ref = self._collection().document(category_id)
        snap = doc_ref.get()

        if not snap.exists:
            return False

        data = snap.to_dict() or {}

        # Prevent deleting system categories
        if data.get("is_system", False):
            return False

        # Prevent deleting OTHER users' categories
        if data.get("owner_id") != owner_id:
            return False

        doc_ref.delete()
        return True