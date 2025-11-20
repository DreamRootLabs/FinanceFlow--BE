from __future__ import annotations

from fastapi import HTTPException, status

from src.models.category import (
    CategoryCreate,
    CategoryResponse,
    CategoriesListResponse,
)
from src.repos.category_repo import CategoryRepo


class CategoryService:
    def __init__(self, repo: CategoryRepo | None = None):
        self.repo = repo or CategoryRepo()

    # --------------------------------------------
    # LIST: user categories + system categories
    # --------------------------------------------
    def list_categories(self, owner_id: str) -> CategoriesListResponse:
        items_in_db = self.repo.list_for_owner(owner_id)
        items = [
            CategoryResponse(
                id=item.id,
                name=item.name,
                type=item.type,
                color=item.color,
                is_system=item.is_system,
            )
            for item in items_in_db
        ]
        return CategoriesListResponse(items=items)

    # --------------------------------------------
    # CREATE: user-owned category only
    # --------------------------------------------
    def create_category(self, owner_id: str, payload: CategoryCreate) -> CategoryResponse:
        created = self.repo.create_for_owner(owner_id, payload)
        return CategoryResponse(
            id=created.id,
            name=created.name,
            type=created.type,
            color=created.color,
            is_system=created.is_system,
        )

    # --------------------------------------------
    # DELETE: only user-owned categories
    # --------------------------------------------
    def delete_category(self, owner_id: str, category_id: str) -> None:
        ok = self.repo.delete_for_owner(owner_id, category_id)
        if not ok:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found or cannot be deleted",
            )
