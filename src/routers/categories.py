from __future__ import annotations

from fastapi import APIRouter, Depends, Request, Response, status

from src.core.auth_dependency import get_current_owner_id
from src.models.category import (
    CategoryCreate,
    CategoryResponse,
    CategoriesListResponse,
)
from src.services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])


# -------- dependencies --------

def get_category_service() -> CategoryService:
    return CategoryService()


# -------- handlers --------

def _list_categories(
    request: Request,
    owner_id: str = Depends(get_current_owner_id),
    service: CategoryService = Depends(get_category_service),
) -> CategoriesListResponse:
    """
    Return system categories + user categories for the current owner.
    """
    return service.list_categories(owner_id)


def _create_category(
    request: Request,
    payload: CategoryCreate,
    owner_id: str = Depends(get_current_owner_id),
    service: CategoryService = Depends(get_category_service),
) -> CategoryResponse:
    """
    Create a new user-owned category.
    """
    return service.create_category(owner_id, payload)


def _delete_category(
    request: Request,
    category_id: str,
    owner_id: str = Depends(get_current_owner_id),
    service: CategoryService = Depends(get_category_service),
) -> Response:
    """
    Delete a user-owned category (system categories are protected).
    """
    service.delete_category(owner_id, category_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# -------- route registrations --------

router.add_api_route(
    "",
    endpoint=_list_categories,
    methods=["GET"],
    response_model=CategoriesListResponse,
    status_code=status.HTTP_200_OK,
)

router.add_api_route(
    "",
    endpoint=_create_category,
    methods=["POST"],
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)

router.add_api_route(
    "/{category_id}",
    endpoint=_delete_category,
    methods=["DELETE"],
    status_code=status.HTTP_204_NO_CONTENT,
)
