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

    def list_categories(self) -> CategoriesListResponse:
        items_in_db = self.repo.list()
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

    def create_category(self, payload: CategoryCreate) -> CategoryResponse:
        created = self.repo.create(payload)
        return CategoryResponse(
            id=created.id,
            name=created.name,
            type=created.type,
            color=created.color,
            is_system=created.is_system,
        )

    def delete_category(self, category_id: str) -> None:
        ok = self.repo.delete(category_id)
        if not ok:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )