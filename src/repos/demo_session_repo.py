from datetime import datetime
from typing import List, Dict, Any

from db.db_connector import get_db

DEFAULT_CATEGORIES: List[Dict[str, Any]] = [
    {"name": "Salary",    "type": "INCOME"},
    {"name": "Bonus",     "type": "INCOME"},
    {"name": "Rent",      "type": "EXPENSE"},
    {"name": "Groceries", "type": "EXPENSE"},
    {"name": "Bills",     "type": "EXPENSE"},
]

class DemoSessionRepo:
    def __init__(self):
        self.db = get_db()

    def create_demo_session(self, demo_id: str, expires_at: datetime) -> None:
        doc_ref = self.db.collection("demo_sessions").document(demo_id)
        doc_ref.set({
            "owner_id": demo_id,
            "is_demo": True,
            "created_at": datetime.utcnow(),
            "expires_at": expires_at,
        })

    def seed_default_categories(self, owner_id: str) -> None:
        batch = self.db.batch()
        coll_ref = self.db.collection("categories")

        for cat in DEFAULT_CATEGORIES:
            doc_ref = coll_ref.document()  # auto id
            batch.set(doc_ref, {
                "owner_id": owner_id,
                "name": cat["name"],
                "type": cat["type"],
                "created_at": datetime.utcnow(),
            })

        batch.commit()

    def seed_example_transactions(self, owner_id: str) -> None:
        # optional – you can implement later
        pass