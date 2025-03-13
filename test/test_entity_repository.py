from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy import Integer, Column
from sqlalchemy.orm import Session, Query

from config.models.base import Base
from models.entity_repository import EntityRepository


# Dummy entity for testing
class DummyEntity(Base):
    __tablename__ = "dummy"
    id = Column(Integer, primary_key=True)


@pytest.fixture
def mock_session():
    return MagicMock(spec=Session)


@pytest.fixture
def mock_query():
    return MagicMock(spec=Query)


@pytest.fixture
def entity_repository():
    return EntityRepository(DummyEntity)


@patch("logging.error")
def test_first(mock_log, entity_repository, mock_query):
    """Test retrieving the first result from a query"""
    mock_query.first.return_value = "dummy_value"
    result = entity_repository.first(mock_query)
    assert result == "dummy_value"

    # Exception handling
    mock_query.first.side_effect = Exception("Database error")
    result = entity_repository.first(mock_query)
    assert result is None
    mock_log.assert_called_with("Exception while getting DummyEntity: Database error")


@patch("logging.error")
def test_all(mock_log, entity_repository, mock_query):
    """Test retrieving all results from a query"""
    mock_query.all.return_value = ["dummy_value1", "dummy_value2"]
    result = entity_repository.all(mock_query)
    assert result == ["dummy_value1", "dummy_value2"]

    # Exception handling
    mock_query.all.side_effect = Exception("Database error")
    result = entity_repository.all(mock_query)
    assert result is None
    mock_log.assert_called_with("Exception while getting DummyEntity: Database error")


@patch("logging.error")
def test_save(mock_log, entity_repository, mock_session):
    """Test saving an entity successfully and handling errors"""
    entity = DummyEntity()
    result = entity_repository.save(mock_session, entity)
    assert result == entity
    mock_session.add.assert_called_with(entity)
    mock_session.commit.assert_called_once()

    # Simulate commit failure
    mock_session.commit.side_effect = Exception("Save error")
    result = entity_repository.save(mock_session, entity)
    assert result is None

@patch("logging.error")
def test_save_not_correct_object(mock_log, entity_repository, mock_session):
    """Test saving an entity successfully and handling errors"""
    entity = None
    result = entity_repository.save(mock_session, entity)
    assert result == None



@patch("logging.error")
def test_save_all(mock_log, entity_repository, mock_session):
    """Test saving multiple entities successfully and handling errors"""
    entities = [DummyEntity(), DummyEntity()]
    result = entity_repository.save_all(mock_session, entities)
    assert result == entities
    mock_session.add_all.assert_called_with(entities)
    mock_session.commit.assert_called_once()

    # Simulate commit failure
    mock_session.commit.side_effect = Exception("Save all error")
    result = entity_repository.save_all(mock_session, entities)
    assert result is None


@patch("logging.error")
def test_save_rollback_called_multiple_times(mock_log, entity_repository, mock_session):
    entity = DummyEntity()
    mock_session.commit.side_effect = Exception("Save error")

    # First attempt
    entity_repository.save(mock_session, entity)
    mock_session.rollback.assert_called_once()

    # Second attempt
    entity_repository.save(mock_session, entity)
    assert mock_session.rollback.call_count == 2  # Should be called twice
