from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field

TransactionType = Literal["expense", "income"]

class TransactionBase(BaseModel):
    amount: float = Field(..., gt=0)
    type: TransactionType
    category_id: Optional[str] = None
    description: Optional[str] = None
    occurred_at: datetime

class TransactionCreate(TransactionBase):
    pass

class TransactionInDB(TransactionBase):
    id: str
    owner_id: str
    created_at: datetime
    updated_at: datetime

class TransactionResponse(TransactionBase):
    id: str

class TransactionsListResponse(BaseModel):
    items: list[TransactionResponse]