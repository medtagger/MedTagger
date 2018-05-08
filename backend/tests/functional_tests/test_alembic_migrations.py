"""Tests for Alembic migrations."""
from typing import Any

from alembic.autogenerate.api import compare_metadata
from alembic.runtime.migration import MigrationContext

from medtagger.database import metadata, engine


def test_if_developer_commited_migrations(prepare_environment: Any) -> None:
    """Test that checks for left uncommited changes in SQL database schema."""
    context = MigrationContext.configure(engine.connect())
    diff = compare_metadata(context, metadata)
    assert not diff, 'You forgot to prepare a DB migration using Alembic!'
