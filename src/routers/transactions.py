from __future__ import annotations

from fastapi import APIRouter, Depends, Request, status, Response

from src.core.auth_dependency import get_current_owner_id
from src.models.transaction import (
    TransactionCreate,
    TransactionResponse,
    TransactionsListResponse,
)
from src.services.transaction_service import TransactionService

router = APIRouter(prefix="/transactions", tags=["transactions"])


# -------- Dependencies --------

def get_transaction_service() -> TransactionService:
    return TransactionService()


# -------- Handlers --------

def _list_transactions(
    request: Request,
    owner_id: str = Depends(get_current_owner_id),
    service: TransactionService = Depends(get_transaction_service),
) -> TransactionsListResponse:
    """
    List all transactions belonging to the authenticated owner.
    """
    return service.list_transactions(owner_id)


def _create_transaction(
    request: Request,
    payload: TransactionCreate,
    owner_id: str = Depends(get_current_owner_id),
    service: TransactionService = Depends(get_transaction_service),
) -> TransactionResponse:
    """
    Create a new transaction for the authenticated owner.
    """
    return service.create_transaction(owner_id, payload)


# -------- Route Registrations --------

router.add_api_route(
    "",
    endpoint=_list_transactions,
    methods=["GET"],
    response_model=TransactionsListResponse,
    status_code=status.HTTP_200_OK,
)

router.add_api_route(
    "",
    endpoint=_create_transaction,
    methods=["POST"],
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)