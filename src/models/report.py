from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class MonthlyCategoryBreakdown(BaseModel):
    category_id: Optional[str] = None
    category_name: Optional[str] = None
    total_income: float
    total_expense: float


class MonthlyReportResponse(BaseModel):
    owner_id: str
    year: int
    month: int
    currency: str = "AUD"

    total_income: float
    total_expense: float
    net: float

    by_category: List[MonthlyCategoryBreakdown]
    generated_at: datetime
