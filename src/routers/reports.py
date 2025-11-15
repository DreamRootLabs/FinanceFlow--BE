from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request, status

from src.core.auth_dependency import get_current_owner_id
from src.models.report import MonthlyReportResponse
from src.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["reports"])


# -------- dependencies --------

def get_report_service() -> ReportService:
    return ReportService()


# -------- handlers --------

def _get_monthly_report(
    request: Request,
    year: int = Query(..., ge=2000, le=2100),
    month: int = Query(..., ge=1, le=12),
    owner_id: str = Depends(get_current_owner_id),
    service: ReportService = Depends(get_report_service),
) -> MonthlyReportResponse:
    """
    Return a monthly income/expense report for the authenticated owner.
    """
    return service.get_monthly_report(owner_id=owner_id, year=year, month=month)


# -------- route registrations --------

router.add_api_route(
    "/monthly",
    endpoint=_get_monthly_report,
    methods=["GET"],
    response_model=MonthlyReportResponse,
    status_code=status.HTTP_200_OK,
)
