from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List, Optional

from src.models.report import MonthlyReportResponse, MonthlyCategoryBreakdown
from src.repos.transaction_repo import TransactionRepo


class ReportService:
    def __init__(self, transactions: Optional[TransactionRepo] = None):
        self.transactions = transactions or TransactionRepo()

    def get_month_range(self, year: int, month: int):
        start = datetime(year, month, 1, tzinfo=timezone.utc)
        if month == 12:
            end = datetime(year + 1, 1, 1, tzinfo=timezone.utc)
        else:
            end = datetime(year, month + 1, 1, tzinfo=timezone.utc)
        return start, end

    def get_monthly_report(self, owner_id: str, year: int, month: int) -> MonthlyReportResponse:
        start, end = self.get_month_range(year, month)
        # You’ll implement this in your repo
        docs = self.transactions.list_for_owner_between(
            owner_id=owner_id,
            start=start,
            end=end,
        )

        # Aggregation
        total_income = 0.0
        total_expense = 0.0
        cat_map: Dict[str, MonthlyCategoryBreakdown] = {}

        for d in docs:
            amount = float(d.get("amount", 0) or 0)
            tx_type = (d.get("type") or "").lower()  # e.g. "income" / "expense"
            category_id = d.get("category_id") or ""
            category_name = d.get("category_name") or ""

            key = category_id or "__uncategorized__"
            if key not in cat_map:
                cat_map[key] = MonthlyCategoryBreakdown(
                    category_id=category_id or None,
                    category_name=category_name or None,
                    total_income=0.0,
                    total_expense=0.0,
                )

            entry = cat_map[key]

            if tx_type == "income":
                total_income += amount
                entry.total_income += amount
            else:
                # treat anything else as expense
                total_expense += amount
                entry.total_expense += amount

        net = total_income - total_expense

        return MonthlyReportResponse(
            owner_id=owner_id,
            year=year,
            month=month,
            total_income=total_income,
            total_expense=total_expense,
            net=net,
            by_category=list(cat_map.values()),
            generated_at=datetime.now(timezone.utc),
        )
