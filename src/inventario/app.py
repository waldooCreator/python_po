import os
from flask import Flask, jsonify, request
from flask_paginate import Pagination, get_page_parameter
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from .database import db
from .models import Producto

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///inventario.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/api/productos', methods=['POST'])
    def crear_producto():
        data = request.get_json()
        if not all(k in data for k in ('nombre', 'precio', 'stock')):
            return jsonify({'error': 'Faltan campos'}), 400
        producto = Producto(nombre=data['nombre'], precio=data['precio'], stock=data['stock'])
        db.session.add(producto)
        db.session.commit()
        return jsonify(producto.to_dict()), 201

    @app.route('/api/productos', methods=['GET'])
    def listar_productos():
        page = request.args.get(get_page_parameter(), type=int, default=1)
        per_page = 5
        productos = Producto.query.paginate(page=page, per_page=per_page, error_out=False)
        pagination = Pagination(page=page, total=productos.total, per_page=per_page, record_name='productos')
        return jsonify({'productos': [p.to_dict() for p in productos.items], 'total': productos.total})

    @app.route('/api/productos/<int:id>/stock', methods=['PUT'])
    def actualizar_stock(id):
        producto = Producto.query.get(id)
        if not producto:
            return jsonify({'error': 'Producto no encontrado'}), 404
        data = request.get_json()
        nuevo_stock = data.get('stock')
        if nuevo_stock is None:
            return jsonify({'error': 'Debe proporcionar el stock'}), 400
        producto.stock = nuevo_stock
        db.session.commit()
        return jsonify(producto.to_dict()), 200

    @app.route('/api/productos/<int:id>', methods=['DELETE'])
    def eliminar_producto(id):
        producto = Producto.query.get(id)
        if not producto:
            return jsonify({'error': 'Producto no encontrado'}), 404
        db.session.delete(producto)
        db.session.commit()
        return jsonify({'mensaje': 'Producto eliminado'}), 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host=os.getenv('HOST'), port=int(os.getenv('PORT', 5000)), debug=True)
