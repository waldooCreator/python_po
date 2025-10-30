import pytest
from src.inventario.app import create_app
from src.inventario.database import db

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_crear_producto(client):
    res = client.post('/api/productos', json={'nombre': 'Laptop', 'precio': 1500, 'stock': 10})
    assert res.status_code == 201
    data = res.get_json()
    assert data['nombre'] == 'Laptop'

def test_listar_productos(client):
    client.post('/api/productos', json={'nombre': 'Mouse', 'precio': 25, 'stock': 50})
    res = client.get('/api/productos')
    assert res.status_code == 200
    assert 'productos' in res.get_json()

def test_actualizar_stock(client):
    client.post('/api/productos', json={'nombre': 'Teclado', 'precio': 100, 'stock': 20})
    res = client.put('/api/productos/1/stock', json={'stock': 99})
    assert res.status_code == 200
    assert res.get_json()['stock'] == 99

def test_eliminar_producto(client):
    client.post('/api/productos', json={'nombre': 'Monitor', 'precio': 300, 'stock': 15})
    res = client.delete('/api/productos/1')
    assert res.status_code == 200
