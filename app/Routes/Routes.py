from flask import request, jsonify
from flask_restful import Resource
from app import db
from app.models import Libro, Cliente, Venta

class LibroResource(Resource):
    def get(self, id=None):
        if id:
            libro = Libro.query.get(id)
            if libro:
                return libro.to_dict(), 200  # Devuelve el diccionario directamente
            return {"message": "Libro no encontrado"}, 404

        libros = Libro.query.all()
        return [libro.to_dict() for libro in libros], 200  # Devuelve una lista de diccionarios

    def post(self):
        data = request.get_json()
        nuevo_libro = Libro(**data)
        db.session.add(nuevo_libro)
        db.session.commit()
        return {"message": "Libro agregado con éxito"}, 200  # Devuelve JSON directamente

    def put(self, id):
        libro = Libro.query.get(id)
        if not libro:
            return {"message": "Libro no encontrado"}, 404
        data = request.get_json()
        for key, value in data.items():
            setattr(libro, key, value)
        db.session.commit()
        return {"message": "Libro actualizado"}, 200

    def delete(self, id):
        libro = Libro.query.get(id)
        if not libro:
            return {"message": "Libro no encontrado"}, 404
        db.session.delete(libro)
        db.session.commit()
        return {"message": "Libro eliminado"}, 200
    

class ClienteResource(Resource):
    def get(self, id=None):
        if id:
            cliente = Cliente.query.get(id)
            return jsonify(cliente.__dict__) if cliente else (jsonify({'message': 'Cliente no encontrado'}), 404)
        clientes = Cliente.query.all()
        return jsonify([cliente.to_dict() for cliente in clientes])

    def post(self):
        data = request.get_json()
        nuevo_cliente = Cliente(**data)
        db.session.add(nuevo_cliente)
        db.session.commit()
        return jsonify({'message': 'Cliente agregado con éxito'})

    def put(self, id):
        cliente = Cliente.query.get(id)
        if not cliente:
            return jsonify({'message': 'Cliente no encontrado'}), 404
        data = request.get_json()
        for key, value in data.items():
            setattr(cliente, key, value)
        db.session.commit()
        return jsonify({'message': 'Cliente actualizado'})

    def delete(self, id):
        cliente = Cliente.query.get(id)
        if not cliente:
            return jsonify({'message': 'Cliente no encontrado'}), 404
        db.session.delete(cliente)
        db.session.commit()
        return jsonify({'message': 'Cliente eliminado'})
    

class VentaResource(Resource):
    def get(self, id=None):
        if id:
            venta = Venta.query.get(id)
            return jsonify(venta.__dict__) if venta else (jsonify({'message': 'Venta no encontrada'}), 404)
        ventas = Venta.query.all()
        return jsonify([venta.to_dict() for venta in ventas])

    def post(self):
        data = request.get_json()
        nueva_venta = Venta(**data)
        db.session.add(nueva_venta)
        db.session.commit()
        return jsonify({'message': 'Venta registrada con éxito'})

    def delete(self, id):
        venta = Venta.query.get(id)
        if not venta:
            return jsonify({'message': 'Venta no encontrada'}), 404
        db.session.delete(venta)
        db.session.commit()
        return jsonify({'message': 'Venta eliminada'})

def initialize_routes(api):
    api.add_resource(LibroResource, '/libros', '/libros/<int:id>')
    api.add_resource(ClienteResource, '/clientes', '/clientes/<int:id>')
    api.add_resource(VentaResource, '/ventas', '/ventas/<int:id>')
