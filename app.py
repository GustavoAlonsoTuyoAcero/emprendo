from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

import datetime

# Initialize Firestore
cred = credentials.Certificate('credentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Endpoint to add a new product to an emprendimiento
@app.route('/emprendimientos/<emprendimiento_id>/agregar_producto', methods=['POST'])
def add_product_to_emprendimiento(emprendimiento_id):
    data = request.get_json()
    
    # Validations
    required_fields = ['nombre', 'descripcion', 'flgDisponible', 'categoria', 'precio', 'images', 'cantidadFavoritos']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'El campo {field} es obligatorio'}), 400
    
    # Add product to the emprendimiento document
    emprendimiento_ref = db.collection('emprendimientos').document(emprendimiento_id)
    emprendimiento = emprendimiento_ref.get()
    if not emprendimiento.exists:
        return jsonify({'error': 'Emprendimiento no encontrado'}), 404
    
    product_data = {
        'nombre': data['nombre'],
        'descripcion': data['descripcion'],
        'flgDisponible': data['flgDisponible'],
        'categoria': data['categoria'],
        'precio': data['precio'],
        'images': data['images'],
        
    # Add current timestamp
    'createdAt': datetime.datetime.utcnow(),
        'cantidadFavoritos': data['cantidadFavoritos']
    }
    
    # Add the product as part of the 'productos' array in the emprendimiento document
    emprendimiento_ref.update({
        'productos': firestore.ArrayUnion([product_data])
    })
    
    return jsonify({'message': 'Producto agregado exitosamente'}), 201

# Endpoint to update a product within an emprendimiento
@app.route('/emprendimientos/<emprendimiento_id>/actualizar_producto', methods=['PUT'])
def update_product_in_emprendimiento(emprendimiento_id):
    data = request.get_json()
    
    # Validations
    if 'nombre' not in data:
        return jsonify({'error': 'El campo nombre es obligatorio para identificar el producto'}), 400
    
    emprendimiento_ref = db.collection('emprendimientos').document(emprendimiento_id)
    emprendimiento = emprendimiento_ref.get()
    if not emprendimiento.exists:
        return jsonify({'error': 'Emprendimiento no encontrado'}), 404
    
    emprendimiento_data = emprendimiento.to_dict()
    productos = emprendimiento_data.get('productos', [])
    
    # Find and update the product
    updated = False
    for product in productos:
        if product['nombre'] == data['nombre']:
            for key in data:
                if key != 'nombre':
                    product[key] = data[key]
            updated = True
            break
    
    if not updated:
        return jsonify({'error': 'Producto no encontrado'}), 404
    
    # Update the emprendimiento document with the modified products list
    emprendimiento_ref.update({
        'productos': productos
    })
    
    return jsonify({'message': 'Producto actualizado exitosamente'}), 200

# Endpoint to delete a product from an emprendimiento
@app.route('/emprendimientos/<emprendimiento_id>/borrar_producto', methods=['DELETE'])
def delete_product_from_emprendimiento(emprendimiento_id):
    data = request.get_json()
    
    # Validations
    if 'nombre' not in data:
        return jsonify({'error': 'El campo nombre es obligatorio para identificar el producto'}), 400
    
    emprendimiento_ref = db.collection('emprendimientos').document(emprendimiento_id)
    emprendimiento = emprendimiento_ref.get()
    if not emprendimiento.exists:
        return jsonify({'error': 'Emprendimiento no encontrado'}), 404
    
    emprendimiento_data = emprendimiento.to_dict()
    productos = emprendimiento_data.get('productos', [])
    
    # Find and remove the product
    productos = [product for product in productos if product['nombre'] != data['nombre']]
    
    # Update the emprendimiento document with the modified products list
    emprendimiento_ref.update({
        'productos': productos
    })
    
    return jsonify({'message': 'Producto eliminado exitosamente'}), 200

# Endpoint to get all products of an emprendimiento
@app.route('/emprendimientos/<emprendimiento_id>/productos', methods=['GET'])
def get_products_of_emprendimiento(emprendimiento_id):
    emprendimiento_ref = db.collection('emprendimientos').document(emprendimiento_id)
    emprendimiento = emprendimiento_ref.get()
    if not emprendimiento.exists:
        return jsonify({'error': 'Emprendimiento no encontrado'}), 404
    
    productos = emprendimiento.to_dict().get('productos', [])
    return jsonify(productos), 200

# Endpoint to get all products from all emprendimientos with optional filtering by name or id
@app.route('/productos', methods=['GET'])
def get_all_products():
    nombre = request.args.get('nombre')
    emprendimientos = db.collection('emprendimientos').stream()
    all_products = []
    for emprendimiento in emprendimientos:
        productos = emprendimiento.to_dict().get('productos', [])
        for product in productos:
            if nombre:
                if product.get('nombre') == nombre:
                    all_products.append(product)
            else:
                all_products.append(product)
    return jsonify(all_products), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
