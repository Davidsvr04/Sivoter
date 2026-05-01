import pytest
import sys
from unittest.mock import Mock, patch, MagicMock
from fastapi import HTTPException
from sqlalchemy.orm import Session

# Mock kafka before importing candidatoService
sys.modules['kafka'] = MagicMock()
sys.modules['kafka.producer'] = MagicMock()

with patch('app.services.kafkaService.KafkaProducer'):
    from app.services.candidatoService import (
        create_candidato, list_candidatos, get_candidato, 
        update_candidato, delete_candidato
    )


@pytest.fixture
def mock_db():
    return Mock(spec=Session)


@pytest.fixture
def mock_candidato_create():
    payload = Mock()
    payload.model_dump.return_value = {
        "nombre": "Test Candidato",
        "partido_id": 1,
        "votacion_id": 1,
        "tipo_cargo_id": 1,
        "departamento_id": 1,
        "municipio_id": 1
    }
    return payload


@pytest.fixture
def mock_candidato_update():
    payload = Mock()
    payload.model_dump.return_value = {"nombre": "Updated Name"}
    return payload


@pytest.fixture
def mock_candidato():
    candidato = Mock()
    candidato.id = 1
    candidato.nombre = "Test Candidato"
    candidato.partido_id = 1
    return candidato


class TestCandidatoService:
    
    @patch('app.services.candidatoService.kafka_producer')
    @patch('app.services.candidatoService.base_service')
    def test_create_candidato_success(self, mock_base_service, mock_kafka, 
                                      mock_db, mock_candidato_create, mock_candidato):
        """Test successful candidato creation"""
        mock_base_service._validate_foreign_keys.return_value = None
        mock_db.query.return_value.filter.return_value.first.return_value = mock_candidato
        
        with patch('app.services.candidatoService.Candidato', return_value=mock_candidato):
            result = create_candidato(mock_db, mock_candidato_create, usuario_id=1)
        
        assert mock_db.add.called
        assert mock_db.commit.called
        assert mock_db.refresh.called
        mock_kafka.send_candidato_created.assert_called_once()
    
    @patch('app.services.candidatoService.kafka_producer')
    @patch('app.services.candidatoService.base_service')
    def test_create_candidato_invalid_fk(self, mock_base_service, mock_kafka, 
                                         mock_db, mock_candidato_create):
        """Test candidato creation with invalid foreign key"""
        mock_base_service._validate_foreign_keys.side_effect = HTTPException(
            status_code=400, detail="FK validation failed"
        )
        
        with pytest.raises(HTTPException):
            create_candidato(mock_db, mock_candidato_create)
    
    @patch('app.services.candidatoService.base_service')
    def test_list_candidatos(self, mock_base_service, mock_db, mock_candidato):
        """Test list all candidatos"""
        mock_base_service.list_all.return_value = [mock_candidato]
        
        result = list_candidatos(mock_db, skip=0, limit=100)
        
        assert len(result) == 1
        mock_base_service.list_all.assert_called_once_with(mock_db, 0, 100)
    
    @patch('app.services.candidatoService.base_service')
    def test_list_candidatos_custom_pagination(self, mock_base_service, mock_db):
        """Test list candidatos with custom pagination"""
        mock_base_service.list_all.return_value = []
        
        result = list_candidatos(mock_db, skip=10, limit=50)
        
        assert result == []
        mock_base_service.list_all.assert_called_once_with(mock_db, 10, 50)
    
    @patch('app.services.candidatoService.base_service')
    def test_get_candidato_success(self, mock_base_service, mock_db, mock_candidato):
        """Test get candidato by ID"""
        mock_base_service.get_by_id.return_value = mock_candidato
        
        result = get_candidato(mock_db, 1)
        
        assert result == mock_candidato
        mock_base_service.get_by_id.assert_called_once_with(mock_db, 1)
    
    @patch('app.services.candidatoService.base_service')
    def test_get_candidato_not_found(self, mock_base_service, mock_db):
        """Test get candidato that doesn't exist"""
        mock_base_service.get_by_id.side_effect = HTTPException(
            status_code=404, detail="Candidato not found"
        )
        
        with pytest.raises(HTTPException):
            get_candidato(mock_db, 999)
    
    @patch('app.services.candidatoService.kafka_producer')
    @patch('app.services.candidatoService.base_service')
    def test_update_candidato_success(self, mock_base_service, mock_kafka, 
                                      mock_db, mock_candidato_update, mock_candidato):
        """Test successful candidato update"""
        mock_base_service.get_by_id.return_value = mock_candidato
        mock_base_service._validate_foreign_keys.return_value = None
        mock_candidato_update.model_dump.return_value = {"nombre": "Updated Name"}
        
        result = update_candidato(mock_db, 1, mock_candidato_update, usuario_id=1)
        
        assert mock_db.commit.called
        assert mock_db.refresh.called
        mock_kafka.send_candidato_updated.assert_called_once()
    
    @patch('app.services.candidatoService.kafka_producer')
    @patch('app.services.candidatoService.base_service')
    def test_delete_candidato_success(self, mock_base_service, mock_kafka, 
                                      mock_db, mock_candidato):
        """Test successful candidato deletion"""
        mock_base_service.delete.return_value = mock_candidato
        
        delete_candidato(mock_db, 1, usuario_id=1)
        
        mock_base_service.delete.assert_called_once_with(mock_db, 1)
        mock_kafka.send_candidato_deleted.assert_called_once()
    
    @patch('app.services.candidatoService.kafka_producer')
    @patch('app.services.candidatoService.base_service')
    def test_delete_candidato_without_usuario_id(self, mock_base_service, mock_kafka, 
                                                  mock_db, mock_candidato):
        """Test candidato deletion without usuario_id"""
        mock_base_service.delete.return_value = mock_candidato
        
        delete_candidato(mock_db, 1)
        
        mock_kafka.send_candidato_deleted.assert_called_once()
