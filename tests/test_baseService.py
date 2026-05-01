import pytest
from unittest.mock import Mock, MagicMock, patch
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.services.baseService import BaseService


class MockModel:
    id = 1
    __name__ = "MockModel"


@pytest.fixture
def mock_db():
    return Mock(spec=Session)


@pytest.fixture
def base_service():
    fk_map = {"user_id": "users", "dept_id": "departments"}
    return BaseService(MockModel, fk_map)


class TestBaseService:
    
    def test_init(self):
        """Test BaseService initialization"""
        service = BaseService(MockModel, {"test": "table"})
        assert service.model_class == MockModel
        assert service.fk_map == {"test": "table"}
    
    def test_init_default_fk_map(self):
        """Test BaseService with default empty fk_map"""
        service = BaseService(MockModel)
        assert service.fk_map == {}
    
    def test_exists_returns_true(self, base_service, mock_db):
        """Test _exists returns True when record exists"""
        mock_db.execute.return_value.first.return_value = (1,)
        result = base_service._exists(mock_db, "users", 1)
        assert result is True
        mock_db.execute.assert_called_once()
    
    def test_exists_returns_false(self, base_service, mock_db):
        """Test _exists returns False when record doesn't exist"""
        mock_db.execute.return_value.first.return_value = None
        result = base_service._exists(mock_db, "users", 999)
        assert result is False
    
    def test_validate_foreign_keys_valid(self, base_service, mock_db):
        """Test _validate_foreign_keys with valid foreign keys"""
        mock_db.execute.return_value.first.return_value = (1,)
        data = {"user_id": 1, "dept_id": 2}
        base_service._validate_foreign_keys(mock_db, data)
    
    def test_validate_foreign_keys_invalid(self, base_service, mock_db):
        """Test _validate_foreign_keys with invalid foreign key"""
        mock_db.execute.return_value.first.return_value = None
        data = {"user_id": 999}
        
        with pytest.raises(HTTPException) as exc_info:
            base_service._validate_foreign_keys(mock_db, data)
        
        assert exc_info.value.status_code == 400
        assert "no existe" in exc_info.value.detail
    
    def test_validate_foreign_keys_null_value(self, base_service, mock_db):
        """Test _validate_foreign_keys with null value (should pass)"""
        data = {"user_id": None, "dept_id": 2}
        mock_db.execute.return_value.first.return_value = (1,)
        base_service._validate_foreign_keys(mock_db, data)
    
    def test_list_all_default(self, base_service, mock_db):
        """Test list_all with default parameters"""
        mock_entity = Mock()
        mock_db.query.return_value.offset.return_value.limit.return_value.all.return_value = [mock_entity]
        
        result = base_service.list_all(mock_db)
        
        assert len(result) == 1
        mock_db.query.assert_called_once_with(MockModel)
        mock_db.query.return_value.offset.assert_called_with(0)
        mock_db.query.return_value.offset.return_value.limit.assert_called_with(100)
    
    def test_list_all_with_pagination(self, base_service, mock_db):
        """Test list_all with custom skip and limit"""
        mock_db.query.return_value.offset.return_value.limit.return_value.all.return_value = []
        
        result = base_service.list_all(mock_db, skip=10, limit=50)
        
        assert result == []
        mock_db.query.return_value.offset.assert_called_with(10)
        mock_db.query.return_value.offset.return_value.limit.assert_called_with(50)
    
    def test_get_by_id_success(self, base_service, mock_db):
        """Test get_by_id returns entity when found"""
        mock_entity = Mock()
        mock_db.query.return_value.filter.return_value.first.return_value = mock_entity
        
        result = base_service.get_by_id(mock_db, 1)
        
        assert result == mock_entity
    
    def test_get_by_id_not_found(self, base_service, mock_db):
        """Test get_by_id raises exception when not found"""
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            base_service.get_by_id(mock_db, 999)
        
        assert exc_info.value.status_code == 404
        assert "no encontrado" in exc_info.value.detail
    
    def test_delete_success(self, base_service, mock_db):
        """Test delete successfully removes entity"""
        mock_entity = Mock()
        mock_db.query.return_value.filter.return_value.first.return_value = mock_entity
        
        result = base_service.delete(mock_db, 1)
        
        assert result == mock_entity
        mock_db.delete.assert_called_once_with(mock_entity)
        mock_db.commit.assert_called_once()
    
    def test_delete_not_found(self, base_service, mock_db):
        """Test delete raises exception when entity not found"""
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            base_service.delete(mock_db, 999)
        
        assert exc_info.value.status_code == 404
