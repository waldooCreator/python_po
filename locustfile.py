from locust import HttpUser, task, between

class InventarioUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.client.get('/api/productos')

    @task(3)
    def listar_productos(self):
        self.client.get('/api/productos')

    @task(2)
    def crear_producto(self):
        self.client.post('/api/productos', json={'nombre': 'Producto Locust', 'precio': 10, 'stock': 5})

    @task(1)
    def eliminar_producto(self):
        self.client.delete('/api/productos/1')
