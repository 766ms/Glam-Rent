from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
import random
import string
import os

app = Flask(__name__, static_folder='.', static_url_path='')
app.config['SECRET_KEY'] = 'glam-rent-cartagena-2024-super-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tienda_vestidos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db = SQLAlchemy(app)

# ==================== MODELOS ====================

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(200))
    ciudad = db.Column(db.String(100))
    es_admin = db.Column(db.Boolean, default=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    carritos = db.relationship('Carrito', backref='usuario', lazy=True, cascade='all, delete-orphan')
    favoritos = db.relationship('Favorito', backref='usuario', lazy=True, cascade='all, delete-orphan')
    pedidos = db.relationship('Pedido', backref='usuario', lazy=True)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float, nullable=False)
    talla = db.Column(db.String(10))
    color = db.Column(db.String(50))
    categoria = db.Column(db.String(50))  # vestido, corset
    imagen_url = db.Column(db.String(300))
    stock = db.Column(db.Integer, default=0)

class Carrito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, default=1)
    fecha_agregado = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    producto = db.relationship('Producto')

class Favorito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    fecha_agregado = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    producto = db.relationship('Producto')

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_pedido = db.Column(db.String(20), unique=True, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(50), default='Pendiente')  # Pendiente, Procesando, Enviado, Entregado, Cancelado
    metodo_pago = db.Column(db.String(50))
    direccion_envio = db.Column(db.String(300))
    fecha_pedido = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    items = db.relationship('ItemPedido', backref='pedido', lazy=True, cascade='all, delete-orphan')

class ItemPedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    producto = db.relationship('Producto')

# ==================== DECORADORES ====================

def token_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'mensaje': 'Token faltante'}), 401
        try:
            if token.startswith('Bearer '):
                token = token.split(' ')[1]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            usuario_actual = Usuario.query.get(data['usuario_id'])
            if not usuario_actual:
                return jsonify({'mensaje': 'Usuario no encontrado'}), 401
        except:
            return jsonify({'mensaje': 'Token inválido'}), 401
        return f(usuario_actual, *args, **kwargs)
    return decorador

def admin_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'mensaje': 'Token faltante'}), 401
        try:
            if token.startswith('Bearer '):
                token = token.split(' ')[1]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            usuario_actual = Usuario.query.get(data['usuario_id'])
            if not usuario_actual or not usuario_actual.es_admin:
                return jsonify({'mensaje': 'Acceso no autorizado'}), 403
        except:
            return jsonify({'mensaje': 'Token inválido'}), 401
        return f(usuario_actual, *args, **kwargs)
    return decorador

# ==================== AUTENTICACIÓN ====================

@app.route('/api/registro', methods=['POST'])
def registro():
    try:
        data = request.get_json()
        if not data or not data.get('email') or not data.get('password') or not data.get('nombre'):
            return jsonify({'mensaje': 'Faltan campos requeridos'}), 400
        
        if Usuario.query.filter_by(email=data['email']).first():
            return jsonify({'mensaje': 'El email ya está registrado'}), 400
        
        password_hash = generate_password_hash(data['password'])
        nuevo_usuario = Usuario(
            nombre=data['nombre'],
            email=data['email'],
            password=password_hash
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify({'mensaje': 'Usuario registrado exitosamente'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'mensaje': f'Error: {str(e)}'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'mensaje': 'Email y contraseña son requeridos'}), 400
        
        usuario = Usuario.query.filter_by(email=data['email']).first()
        if not usuario or not check_password_hash(usuario.password, data['password']):
            return jsonify({'mensaje': 'Email o contraseña incorrectos'}), 401
        
        token = jwt.encode({
            'usuario_id': usuario.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        
        return jsonify({
            'token': token,
            'usuario': {
                'id': usuario.id,
                'nombre': usuario.nombre,
                'email': usuario.email,
                'es_admin': usuario.es_admin
            }
        }), 200
    except Exception as e:
        return jsonify({'mensaje': f'Error: {str(e)}'}), 500

# ==================== PERFIL DE USUARIO ====================

@app.route('/api/perfil', methods=['GET'])
@token_requerido
def obtener_perfil(usuario_actual):
    return jsonify({
        'id': usuario_actual.id,
        'nombre': usuario_actual.nombre,
        'email': usuario_actual.email,
        'telefono': usuario_actual.telefono,
        'direccion': usuario_actual.direccion,
        'ciudad': usuario_actual.ciudad,
        'fecha_registro': usuario_actual.fecha_registro.strftime('%Y-%m-%d')
    }), 200

@app.route('/api/perfil', methods=['PUT'])
@token_requerido
def actualizar_perfil(usuario_actual):
    try:
        data = request.get_json()
        if data.get('nombre'):
            usuario_actual.nombre = data['nombre']
        if data.get('telefono'):
            usuario_actual.telefono = data['telefono']
        if data.get('direccion'):
            usuario_actual.direccion = data['direccion']
        if data.get('ciudad'):
            usuario_actual.ciudad = data['ciudad']
        
        db.session.commit()
        return jsonify({'mensaje': 'Perfil actualizado exitosamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'mensaje': f'Error: {str(e)}'}), 500

# ==================== PRODUCTOS ====================

@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    try:
        # Filtros
        color = request.args.get('color')
        categoria = request.args.get('categoria')
        precio_min = request.args.get('precio_min', type=float)
        precio_max = request.args.get('precio_max', type=float)
        orden = request.args.get('orden')  # precio_asc, precio_desc, nombre
        
        query = Producto.query
        
        if color:
            query = query.filter(Producto.color.ilike(f'%{color}%'))
        if categoria:
            query = query.filter(Producto.categoria == categoria)
        if precio_min:
            query = query.filter(Producto.precio >= precio_min)
        if precio_max:
            query = query.filter(Producto.precio <= precio_max)
        
        if orden == 'precio_asc':
            query = query.order_by(Producto.precio.asc())
        elif orden == 'precio_desc':
            query = query.order_by(Producto.precio.desc())
        elif orden == 'nombre':
            query = query.order_by(Producto.nombre.asc())
        
        productos = query.all()
        
        resultado = []
        for p in productos:
            resultado.append({
                'id': p.id,
                'nombre': p.nombre,
                'descripcion': p.descripcion,
                'precio': p.precio,
                'talla': p.talla,
                'color': p.color,
                'categoria': p.categoria,
                'imagen_url': p.imagen_url,
                'stock': p.stock
            })
        
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'mensaje': f'Error: {str(e)}'}), 500

@app.route('/api/productos/buscar', methods=['GET'])
def buscar_productos():
    try:
        query = request.args.get('q', '').lower()
        if not query:
            return jsonify([]), 200
        
        productos = Producto.query.filter(
            db.or_(
                Producto.nombre.ilike(f'%{query}%'),
                Producto.descripcion.ilike(f'%{query}%'),
                Producto.color.ilike(f'%{query}%')
            )
        ).all()
        
        resultado = [{
            'id': p.id,
            'nombre': p.nombre,
            'descripcion': p.descripcion,
            'precio': p.precio,
            'talla': p.talla,
            'color': p.color,
            'categoria': p.categoria,
            'imagen_url': p.imagen_url,
            'stock': p.stock
        } for p in productos]
        
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'mensaje': f'Error: {str(e)}'}), 500

# ==================== FAVORITOS ====================

@app.route('/api/favoritos', methods=['GET'])
@token_requerido
def obtener_favoritos(usuario_actual):
    try:
        favoritos = Favorito.query.filter_by(usuario_id=usuario_actual.id).all()
        resultado = [{
            'id': f.id,
            'producto': {
                'id': f.producto.id,
                'nombre': f.producto.nombre,
                'precio': f.producto.precio,
                'imagen_url': f.producto.imagen_url,
                'stock': f.producto.stock
            }
        } for f in favoritos]
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'mensaje': f'Error: {str(e)}'}), 500

@app.route('/api/favoritos', methods=['POST'])
@token_requerido
def agregar_favorito(usuario_actual):
    try:
        data = request.get_json()
        if not data or not data.get('producto_id'):
            return jsonify({'mensaje': 'ID de producto requerido'}), 400
        
        # Verificar si ya existe
        existe = Favorito.query.filter_by(
            usuario_id=usuario_actual.id,
            producto_id=data['producto_id']
        ).first()
        
        if existe:
            return jsonify({'mensaje': 'Producto ya está en favoritos'}), 400
        
        nuevo_favorito = Favorito(
            usuario_id=usuario_actual.id,
            producto_id=data['producto_id']
        )
        db.session.add(nuevo_favorito)
        db.session.commit()
        return jsonify({'mensaje': 'Producto agregado a favoritos'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'mensaje': f'Error: {str(e)}'}), 500

@app.route('/api/favoritos/<int:producto_id>', methods=['DELETE'])
@token_requerido
def eliminar_favorito(usuario_actual, producto_id):
    try:
        favorito = Favorito.query.filter_by(
            usuario_id=usuario_actual.id,
            producto_id=producto_id
        ).first()
        
        if not favorito:
            return jsonify({'mensaje': 'Favorito no encontrado'}), 404
        
        db.session.delete(favorito)
        db.session.commit()
        return jsonify({'mensaje': 'Producto eliminado de favoritos'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'mensaje': f'Error: {str(e)}'}), 500

# ==================== CARRITO ====================

@app.route('/api/carrito', methods=['GET'])
@token_requerido
def obtener_carrito(usuario_actual):
    try:
        items = Carrito.query.filter_by(usuario_id=usuario_actual.id).all()
        resultado = []
        total = 0
        
        for item in items:
            subtotal = item.producto.precio * item.cantidad
            total += subtotal
            resultado.append({
                'id': item.id,
                'producto': {
                    'id': item.producto.id,
                    'nombre': item.producto.nombre,
                    'precio': item.producto.precio,
                    'imagen_url': item.producto.imagen_url
                },
                'cantidad': item.cantidad,
                'subtotal': subtotal
            })
        
        return jsonify({'items': resultado, 'total': total}), 200
    except Exception as e:
        return jsonify({'mensaje': f'Error: {str(e)}'}), 500

@app.route('/api/carrito', methods=['POST'])
@token_requerido
def agregar_al_carrito(usuario_actual):
    try:
        data = request.get_json()
        if not data or not data.get('producto_id'):
            return jsonify({'mensaje': 'ID de producto requerido'}), 400
        
        producto = Producto.query.get(data['producto_id'])
        if not producto:
            return jsonify({'mensaje': 'Producto no encontrado'}), 404
        
        item_existente = Carrito.query.filter_by(
            usuario_id=usuario_actual.id,
            producto_id=data['producto_id']
        ).first()
        
        if item_existente:
            item_existente.cantidad += data.get('cantidad', 1)
            db.session.commit()
            return jsonify({'mensaje': 'Cantidad actualizada'}), 200
        
        nuevo_item = Carrito(
            usuario_id=usuario_actual.id,
            producto_id=data['producto_id'],
            cantidad=data.get('cantidad', 1)
        )
        db.session.add(nuevo_item)
        db.session.commit()
        return jsonify({'mensaje': 'Item añadido al carrito'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'mensaje': f'Error: {str(e)}'}), 500

@app.route('/api/carrito/<int:id>', methods=['DELETE'])
@token_requerido
def eliminar_del_carrito(usuario_actual, id):
    try:
        item = Carrito.query.filter_by(id=id, usuario_id=usuario_actual.id).first()
        if not item:
            return jsonify({'mensaje': 'Item no encontrado'}), 404
        db.session.delete(item)
        db.session.commit()
        return jsonify({'mensaje': 'Item eliminado'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'mensaje': f'Error: {str(e)}'}), 500

@app.route('/api/carrito/<int:id>', methods=['PUT'])
@token_requerido
def actualizar_cantidad_carrito(usuario_actual, id):
    try:
        data = request.get_json()
        item = Carrito.query.filter_by(id=id, usuario_id=usuario_actual.id).first()
        if not item:
            return jsonify({'mensaje': 'Item no encontrado'}), 404
        
        cantidad = data.get('cantidad', 1)
        if cantidad <= 0:
            db.session.delete(item)
        else:
            item.cantidad = cantidad
        db.session.commit()
        return jsonify({'mensaje': 'Cantidad actualizada'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'mensaje': f'Error: {str(e)}'}), 500

# ==================== PEDIDOS ====================

def generar_numero_pedido():
    return 'GR' + ''.join(random.choices(string.digits, k=10))

@app.route('/api/pedidos', methods=['POST'])
@token_requerido
def crear_pedido(usuario_actual):
    try:
        data = request.get_json()
        items_carrito = Carrito.query.filter_by(usuario_id=usuario_actual.id).all()
        
        if not items_carrito:
            return jsonify({'mensaje': 'El carrito está vacío'}), 400
        
        total = sum(item.producto.precio * item.cantidad for item in items_carrito)
        
        nuevo_pedido = Pedido(
            numero_pedido=generar_numero_pedido(),
            usuario_id=usuario_actual.id,
            total=total,
            metodo_pago=data.get('metodo_pago', 'Tarjeta'),
            direccion_envio=data.get('direccion_envio', usuario_actual.direccion)
        )
        db.session.add(nuevo_pedido)
        db.session.flush()
        
        for item in items_carrito:
            item_pedido = ItemPedido(
                pedido_id=nuevo_pedido.id,
                producto_id=item.producto_id,
                cantidad=item.cantidad,
                precio_unitario=item.producto.precio
            )
            db.session.add(item_pedido)
        
        Carrito.query.filter_by(usuario_id=usuario_actual.id).delete()
        db.session.commit()
        
        return jsonify({
            'mensaje': 'Pedido creado exitosamente',
            'numero_pedido': nuevo_pedido.numero_pedido,
            'total': total
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'mensaje': f'Error: {str(e)}'}), 500

@app.route('/api/pedidos', methods=['GET'])
@token_requerido
def obtener_pedidos(usuario_actual):
    try:
        pedidos = Pedido.query.filter_by(usuario_id=usuario_actual.id).order_by(Pedido.fecha_pedido.desc()).all()
        resultado = []
        
        for p in pedidos:
            items = [{
                'producto': {
                    'nombre': item.producto.nombre,
                    'imagen_url': item.producto.imagen_url
                },
                'cantidad': item.cantidad,
                'precio_unitario': item.precio_unitario
            } for item in p.items]
            
            resultado.append({
                'id': p.id,
                'numero_pedido': p.numero_pedido,
                'total': p.total,
                'estado': p.estado,
                'fecha_pedido': p.fecha_pedido.strftime('%Y-%m-%d %H:%M'),
                'items': items
            })
        
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'mensaje': f'Error: {str(e)}'}), 500

# ==================== ADMIN ====================

@app.route('/api/admin/pedidos', methods=['GET'])
@admin_requerido
def admin_obtener_pedidos(usuario_actual):
    try:
        pedidos = Pedido.query.order_by(Pedido.fecha_pedido.desc()).all()
        resultado = []
        
        for p in pedidos:
            items = [{
                'producto': {
                    'nombre': item.producto.nombre,
                    'imagen_url': item.producto.imagen_url
                },
                'cantidad': item.cantidad,
                'precio_unitario': item.precio_unitario
            } for item in p.items]
            
            resultado.append({
                'id': p.id,
                'numero_pedido': p.numero_pedido,
                'cliente': {
                    'nombre': p.usuario.nombre,
                    'email': p.usuario.email
                },
                'total': p.total,
                'estado': p.estado,
                'direccion_envio': p.direccion_envio,
                'fecha_pedido': p.fecha_pedido.strftime('%Y-%m-%d %H:%M'),
                'items': items
            })
        
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'mensaje': f'Error: {str(e)}'}), 500

@app.route('/api/admin/pedidos/<int:id>/estado', methods=['PUT'])
@admin_requerido
def admin_actualizar_estado_pedido(usuario_actual, id):
    try:
        data = request.get_json()
        pedido = Pedido.query.get_or_404(id)
        pedido.estado = data.get('estado', pedido.estado)
        db.session.commit()
        return jsonify({'mensaje': 'Estado actualizado'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'mensaje': f'Error: {str(e)}'}), 500

@app.route('/api/admin/productos', methods=['GET'])
@admin_requerido
def admin_obtener_productos(usuario_actual):
    try:
        productos = Producto.query.all()
        resultado = [{
            'id': p.id,
            'nombre': p.nombre,
            'descripcion': p.descripcion,
            'precio': p.precio,
            'talla': p.talla,
            'color': p.color,
            'categoria': p.categoria,
            'imagen_url': p.imagen_url,
            'stock': p.stock
        } for p in productos]
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'mensaje': f'Error: {str(e)}'}), 500

@app.route('/api/admin/productos/<int:id>/stock', methods=['PUT'])
@admin_requerido
def admin_actualizar_stock(usuario_actual, id):
    try:
        data = request.get_json()
        producto = Producto.query.get_or_404(id)
        nuevo_stock = data.get('stock')
        
        if nuevo_stock is None:
            return jsonify({'mensaje': 'Stock requerido'}), 400
        
        if nuevo_stock < 0:
            return jsonify({'mensaje': 'El stock no puede ser negativo'}), 400
        
        producto.stock = nuevo_stock
        db.session.commit()
        return jsonify({'mensaje': 'Stock actualizado', 'stock': producto.stock}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'mensaje': f'Error: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 200

# Servir archivos estáticos
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    print("🚀 Servidor GLAM RENT iniciado")
    print("📦 Backend en http://localhost:5000")
    print("🌐 Abre: http://localhost:5000")
    app.run(debug=True, port=5000)