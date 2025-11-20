from __future__ import annotations

from typing import Literal, Optional
from datetime import datetime
from pydantic import BaseModel, Field

CategoryType = Literal["expense", "income"]

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    type: CategoryType
    color: Optional[str] = Field(default=None)

class CategoryCreate(CategoryBase):
    is_system: bool = False # global/system category by default
    owner_id: Optional[str] = None

class CategoryInDB(CategoryBase):
    id: str
    is_system: bool
    owner_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class CategoryResponse(CategoryBase):
    id: str
    is_system: bool
    owner_id: Optional[str] = None

class CategoriesListResponse(BaseModel):
    items: list[CategoryResponse]