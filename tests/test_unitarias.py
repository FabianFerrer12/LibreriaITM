import pytest
from unittest.mock import patch, MagicMock
from app import app, db
from app.models import Libro, Cliente, Venta

@pytest.fixture
def client():
    app.config["TESTING"] = True  
    with app.app_context():  
        with app.test_client() as client:
            yield client  

@patch("app.Routes.Routes.Libro.query")
def test_get_libro(mock_query, client):
    """Prueba obtener un libro existente."""
    mock_libro = MagicMock()
    mock_libro.to_dict.return_value = {"id": 1, "titulo": "Libro de prueba", "autor": "Autor X", "precio": 100}
    mock_query.get.return_value = mock_libro  
    response = client.get("/libros/1")
    assert response.status_code == 200
    assert response.get_json() == {"id": 1, "titulo": "Libro de prueba", "autor": "Autor X", "precio": 100}

@patch("app.Routes.Routes.Libro.query")
def test_get_libro_no_existente(mock_query, client):
    """Prueba obtener un libro que no existe."""
    mock_query.get.return_value = None  

    response = client.get("/libros/1")
    assert response.status_code == 404
    assert response.get_json() == {"message": "Libro no encontrado"}

@patch("app.Routes.Routes.db.session")
@patch("app.Routes.Routes.Libro")
def test_post_libro(mock_libro, mock_session, client):
    """Prueba la creación de un libro."""
    mock_libro.return_value = MagicMock()
    
    response = client.post('/libros', json={"titulo": "Libro de prueba", "autor": "Autor X", "precio": 100})
    
    assert response.status_code == 200
    assert response.get_json() == {"message": "Libro agregado con éxito"}
    mock_session.add.assert_called_once()  
    mock_session.commit.assert_called_once() 

@patch("app.Routes.Routes.db.session")
@patch("app.Routes.Routes.Libro.query")
def test_put_libro(mock_query, mock_session, client):
    """Prueba actualizar un libro."""
    mock_libro = MagicMock()
    mock_query.get.return_value = mock_libro  

    response = client.put('/libros/1', json={"titulo": "Libro actualizado", "autor": "Autor Y"})
    
    assert response.status_code == 200
    assert response.get_json() == {"message": "Libro actualizado"}
    mock_session.commit.assert_called_once()

@patch("app.Routes.Routes.db.session")
@patch("app.Routes.Routes.Libro.query")
def test_delete_libro(mock_query, mock_session, client):
    """Prueba eliminar un libro."""
    mock_libro = MagicMock()
    mock_query.get.return_value = mock_libro  

    response = client.delete('/libros/1')
    
    assert response.status_code == 200
    assert response.get_json() == {"message": "Libro eliminado"}
    mock_session.delete.assert_called_once_with(mock_libro)  
    mock_session.commit.assert_called_once()


@patch("app.Routes.Routes.db.session")
@patch("app.Routes.Routes.Cliente")
def test_post_cliente(mock_cliente, mock_session, client):
    """Prueba la creación de un cliente."""
    mock_cliente.return_value = MagicMock()
    
    response = client.post('/clientes', json={"nombre": "Juan Pérez", "email": "juan@example.com"})
    
    assert response.status_code == 200
    assert response.get_json() == {"message": "Cliente agregado con éxito"}
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

@patch("app.Routes.Routes.db.session")
@patch("app.Routes.Routes.Cliente.query")
def test_delete_cliente(mock_query, mock_session, client):
    """Prueba eliminar un cliente."""
    mock_cliente = MagicMock()
    mock_query.get.return_value = mock_cliente  

    response = client.delete('/clientes/1')
    
    assert response.status_code == 200
    assert response.get_json() == {"message": "Cliente eliminado"}
    mock_session.delete.assert_called_once_with(mock_cliente)
    mock_session.commit.assert_called_once()
