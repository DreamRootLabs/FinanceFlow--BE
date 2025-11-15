from __future__ import annotations

from src.models.transaction import (
    TransactionCreate,
    TransactionResponse,
    TransactionsListResponse,
)
from src.repos.transaction_repo import TransactionRepo

class TransactionService:
    def __init__(self, repo: TransactionRepo | None = None):
        self.repo = repo or TransactionRepo()

    def list_transactions(self, owner_id: str) -> TransactionsListResponse:
        items_in_db = self.repo.list_for_owner(owner_id)
        items = [
            TransactionResponse(
                id=item.id,
                amount=item.amount,
                type=item.type,
                category_id=item.category_id,
                description=item.description,
                occurred_at=item.occurred_at,
            )
            for item in items_in_db
        ]
        return TransactionsListResponse(items=items)

    def create_transaction(
        self,
        owner_id: str,
        payload: TransactionCreate,
    ) -> TransactionResponse:
        created = self.repo.create_for_owner(owner_id, payload)
        return TransactionResponse(
            id=created.id,
            amount=created.amount,
            type=created.type,
            category_id=created.category_id,
            description=created.description,
            occurred_at=created.occurred_at,
        )