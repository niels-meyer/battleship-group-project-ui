from __future__ import annotations
from typing import Any
import pytest
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, create_engine
from src.database.player import Player as DbPlayer  # noqa: F401 – registers table in SQLModel.metadata
from src.database.match import Match  # noqa: F401 – registers table in SQLModel.metadata
import src.database.db as db_module


@pytest.fixture
def case_results() -> list[dict[str, Any]]:
    return []


@pytest.fixture
def in_memory_db():
    """Replace the global DB engine with a fresh in-memory SQLite database for one test."""
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(test_engine)
    original_engine = db_module.engine
    db_module.engine = test_engine
    yield test_engine
    db_module.engine = original_engine
