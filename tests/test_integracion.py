import pytest
from app import app, db
from app.models import Libro, Cliente, Venta

@pytest.fixture
def client():
    """Configura un cliente de prueba con una base de datos en memoria."""
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_post_libro(client):
    response = client.post('/libros', json={"titulo": "Libro de prueba","genero":"acción", "autor": "Autor X","isbn": "978-3-16-148410-0", "precio": 100})
    assert response.status_code == 200
    print(response)
    json_data = response.get_json() 
    assert json_data["message"] == "Libro agregado con éxito"

def test_get_libros(client):
    """Prueba obtener todos los libros."""
    response = client.get('/libros')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_get_libro_no_existente(client):
    """Prueba obtener un libro que no existe."""
    response = client.get('/libros/1')
    assert response.status_code == 404

def test_put_libro(client):
    """Prueba actualizar un libro."""
    client.post('/libros', json={"titulo": "Libro de prueba", "genero":"terror","autor": "Autor X","isbn": "978-3-16-148410-0","precio": 100})
    response = client.put('/libros/1', json={"titulo": "Libro actualizado"})
    assert response.status_code == 200
    assert response.get_json()["message"] == "Libro actualizado"

def test_delete_libro(client):
    """Prueba eliminar un libro."""
    client.post('/libros', json={"titulo": "Libro de prueba","genero":"terror", "autor": "Autor X","isbn": "978-3-16-148410-0", "precio": 100})
    response = client.delete('/libros/1')
    assert response.status_code == 200
    assert response.get_json()["message"] == "Libro eliminado"

# Pruebas para el recurso Cliente
def test_post_cliente(client):
    """Prueba la creación de un cliente."""
    response = client.post('/clientes', json={"nombre": "Cliente A", "email": "cliente@ejemplo.com"})
    assert response.status_code == 200
    assert response.get_json()["message"] == "Cliente agregado con éxito"

def test_get_clientes(client):
    """Prueba obtener todos los clientes."""
    response = client.get('/clientes')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_delete_cliente(client):
    """Prueba eliminar un cliente."""
    client.post('/clientes', json={"nombre": "Cliente A", "email": "cliente@ejemplo.com"})
    response = client.delete('/clientes/1')
    assert response.status_code == 200
    assert response.get_json()["message"] == "Cliente eliminado"

# Pruebas para el recurso Venta
def test_post_venta(client):
    """Prueba la creación de una venta."""
    response = client.post('/ventas', json={"cliente_id": 1, "libro_id": 1, "cantidad": 2,"total":29.0})
    assert response.status_code == 200
    assert response.get_json()["message"] == "Venta registrada con éxito"

def test_get_ventas(client):
    """Prueba obtener todas las ventas."""
    response = client.get('/ventas')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_delete_venta(client):
    """Prueba eliminar una venta."""
    client.post('/ventas', json={"cliente_id": 1, "libro_id": 1, "cantidad": 2,"total":29.0})
    response = client.delete('/ventas/1')
    assert response.status_code == 200
    assert response.get_json()["message"] == "Venta eliminada"
