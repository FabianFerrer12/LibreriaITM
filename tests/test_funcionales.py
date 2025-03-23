import pytest
from app import app,db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    
    with app.app_context():
        db.create_all()
        with app.test_client() as client:
            yield client
# 🔹 PRUEBA: Agregar un libro
def test_post_libro(client):
    response = client.post("/libros", json={
        "titulo": "El principito",
        "autor": "xxxx",
        "genero":"xxx",
        "isbn":"978-3-16-148410-1s",
        "precio":20
    })
    
    assert response.status_code == 200
    assert response.get_json()["message"] == "Libro agregado con éxito"  
    
    
# 🔹 PRUEBA: Obtener lista de libros (debería devolver 1)
def test_get_libros(client):
    response = client.get("/libros")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
    assert len(response.get_json()) == 1 

# 🔹 PRUEBA: Obtener un libro por ID válido
def test_get_libro(client):
    response = client.get("/libros/1")  
    assert response.status_code == 200
    assert "titulo" in response.get_json()

# 🔹 PRUEBA: Obtener un libro por ID inexistente
def test_get_libro_no_existente(client):
    response = client.get("/libros/999") 
    assert response.status_code == 404
    assert response.get_json()["message"] == "Libro no encontrado"

# 🔹 PRUEBA: Actualizar un libro
def test_put_libro(client):
    response = client.put("/libros/1", json={
        "titulo": "El Principito (Edición Especial)"
    })
    assert response.status_code == 200
    assert response.get_json()["message"] == "Libro actualizado"

# 🔹 PRUEBA: Eliminar un libro
def test_delete_libro(client):
    response = client.delete("/libros/1")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Libro eliminado"

# 🔹 PRUEBA: Eliminar un libro que no existe
def test_delete_libro_no_existente(client):
    response = client.delete("/libros/999")  
    assert response.status_code == 404
    assert response.get_json()["message"] == "Libro no encontrado"
