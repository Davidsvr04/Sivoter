import pytest
import sys
from unittest.mock import Mock, patch, MagicMock
from fastapi import HTTPException
from sqlalchemy.orm import Session

# Mock kafka before importing mesaVotacionService
sys.modules['kafka'] = MagicMock()
sys.modules['kafka.producer'] = MagicMock()

with patch('app.services.kafkaService.KafkaProducer'):
    from app.services.mesaVotacionService import (
        create_mesa_votacion, list_mesas_votacion, get_mesa_votacion,
        update_mesa_votacion, delete_mesa_votacion
    )


@pytest.fixture
def mock_db():
    return Mock(spec=Session)


@pytest.fixture
def mock_mesa_create():
    payload = Mock()
    payload.model_dump.return_value = {
        "nombre": "Mesa 001",
        "barrio_id": 1
    }
    return payload


@pytest.fixture
def mock_mesa_update():
    payload = Mock()
    payload.model_dump.return_value = {"nombre": "Mesa 002"}
    return payload


@pytest.fixture
def mock_mesa():
    mesa = Mock()
    mesa.id = 1
    mesa.nombre = "Mesa 001"
    mesa.barrio_id = 1
    return mesa


class TestMesaVotacionService:
    
    @patch('app.services.mesaVotacionService.kafka_producer')
    @patch('app.services.mesaVotacionService.base_service')
    def test_create_mesa_votacion_success(self, mock_base_service, mock_kafka,
                                         mock_db, mock_mesa_create, mock_mesa):
        """Test successful mesa votacion creation"""
        mock_base_service._validate_foreign_keys.return_value = None
        
        with patch('app.services.mesaVotacionService.MesaVotacion', return_value=mock_mesa):
            result = create_mesa_votacion(mock_db, mock_mesa_create, usuario_id=1)
        
        assert mock_db.add.called
        assert mock_db.commit.called
        assert mock_db.refresh.called
        mock_kafka.send_mesa_created.assert_called_once()
    
    @patch('app.services.mesaVotacionService.kafka_producer')
    @patch('app.services.mesaVotacionService.base_service')
    def test_create_mesa_votacion_invalid_fk(self, mock_base_service, mock_kafka,
                                            mock_db, mock_mesa_create):
        """Test mesa votacion creation with invalid foreign key"""
        mock_base_service._validate_foreign_keys.side_effect = HTTPException(
            status_code=400, detail="FK validation failed"
        )
        
        with pytest.raises(HTTPException):
            create_mesa_votacion(mock_db, mock_mesa_create)
    
    @patch('app.services.mesaVotacionService.base_service')
    def test_list_mesas_votacion(self, mock_base_service, mock_db, mock_mesa):
        """Test list all mesas votacion"""
        mock_base_service.list_all.return_value = [mock_mesa]
        
        result = list_mesas_votacion(mock_db, skip=0, limit=100)
        
        assert len(result) == 1
        mock_base_service.list_all.assert_called_once_with(mock_db, 0, 100)
    
    @patch('app.services.mesaVotacionService.base_service')
    def test_list_mesas_votacion_custom_pagination(self, mock_base_service, mock_db):
        """Test list mesas votacion with custom pagination"""
        mock_base_service.list_all.return_value = []
        
        result = list_mesas_votacion(mock_db, skip=5, limit=25)
        
        assert result == []
        mock_base_service.list_all.assert_called_once_with(mock_db, 5, 25)
    
    @patch('app.services.mesaVotacionService.base_service')
    def test_get_mesa_votacion_success(self, mock_base_service, mock_db, mock_mesa):
        """Test get mesa votacion by ID"""
        mock_base_service.get_by_id.return_value = mock_mesa
        
        result = get_mesa_votacion(mock_db, 1)
        
        assert result == mock_mesa
        mock_base_service.get_by_id.assert_called_once_with(mock_db, 1)
    
    @patch('app.services.mesaVotacionService.base_service')
    def test_get_mesa_votacion_not_found(self, mock_base_service, mock_db):
        """Test get mesa votacion that doesn't exist"""
        mock_base_service.get_by_id.side_effect = HTTPException(
            status_code=404, detail="Mesa votacion not found"
        )
        
        with pytest.raises(HTTPException):
            get_mesa_votacion(mock_db, 999)
    
    @patch('app.services.mesaVotacionService.kafka_producer')
    @patch('app.services.mesaVotacionService.base_service')
    def test_update_mesa_votacion_success(self, mock_base_service, mock_kafka,
                                         mock_db, mock_mesa_update, mock_mesa):
        """Test successful mesa votacion update"""
        mock_base_service.get_by_id.return_value = mock_mesa
        mock_base_service._validate_foreign_keys.return_value = None
        mock_mesa_update.model_dump.return_value = {"nombre": "Mesa Updated"}
        
        result = update_mesa_votacion(mock_db, 1, mock_mesa_update, usuario_id=1)
        
        assert mock_db.commit.called
        assert mock_db.refresh.called
        mock_kafka.send_mesa_updated.assert_called_once()
    
    @patch('app.services.mesaVotacionService.kafka_producer')
    @patch('app.services.mesaVotacionService.base_service')
    def test_update_mesa_votacion_without_usuario_id(self, mock_base_service, mock_kafka,
                                                     mock_db, mock_mesa_update, mock_mesa):
        """Test mesa votacion update without usuario_id"""
        mock_base_service.get_by_id.return_value = mock_mesa
        mock_base_service._validate_foreign_keys.return_value = None
        mock_mesa_update.model_dump.return_value = {"nombre": "Mesa Updated"}
        
        result = update_mesa_votacion(mock_db, 1, mock_mesa_update)
        
        assert mock_db.commit.called
        mock_kafka.send_mesa_updated.assert_called_once()
    
    @patch('app.services.mesaVotacionService.kafka_producer')
    @patch('app.services.mesaVotacionService.base_service')
    def test_delete_mesa_votacion_success(self, mock_base_service, mock_kafka,
                                         mock_db, mock_mesa):
        """Test successful mesa votacion deletion"""
        mock_base_service.delete.return_value = mock_mesa
        
        delete_mesa_votacion(mock_db, 1, usuario_id=1)
        
        mock_base_service.delete.assert_called_once_with(mock_db, 1)
        mock_kafka.send_mesa_deleted.assert_called_once()
    
    @patch('app.services.mesaVotacionService.kafka_producer')
    @patch('app.services.mesaVotacionService.base_service')
    def test_delete_mesa_votacion_without_usuario_id(self, mock_base_service, mock_kafka,
                                                     mock_db, mock_mesa):
        """Test mesa votacion deletion without usuario_id"""
        mock_base_service.delete.return_value = mock_mesa
        
        delete_mesa_votacion(mock_db, 1)
        
        mock_kafka.send_mesa_deleted.assert_called_once()
