from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tienda_vestidos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(200))
    ciudad = db.Column(db.String(100))
    es_admin = db.Column(db.Boolean, default=False)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float, nullable=False)
    talla = db.Column(db.String(10))
    color = db.Column(db.String(50))
    categoria = db.Column(db.String(50))
    imagen_url = db.Column(db.String(300))
    stock = db.Column(db.Integer, default=0)

def seed_database():
    with app.app_context():
        db.create_all()
        
        # Verificar si ya hay datos
        if Producto.query.count() > 0:
            print("⚠️  Ya existen productos.")
            respuesta = input("¿Eliminar y recrear? (s/n): ")
            if respuesta.lower() != 's':
                print("❌ Cancelado")
                return
            Producto.query.delete()
            Usuario.query.delete()
            db.session.commit()
        
        # Crear usuario admin
        admin = Usuario(
            nombre='Admin',
            email='admin@glamrent.com',
            password=generate_password_hash('admin123'),
            es_admin=True
        )
        db.session.add(admin)
        
        # Productos
        productos = [
            # VESTIDOS
            {
                'nombre': 'Wings of Losie Corset Dress',
                'descripcion': 'Elegante vestido con corsé estilo wings, perfecto para eventos especiales',
                'precio': 299999,
                'talla': 'S/M/L',
                'color': 'Rosa',
                'categoria': 'vestido',
                'imagen_url': 'imagenes/vestido 1.png',
                'stock': 10
            },
            {
                'nombre': 'Secret Envoy Dress',
                'descripcion': 'Vestido secreto de gala con detalles únicos',
                'precio': 199999,
                'talla': 'S/M/L',
                'color': 'Blanco',
                'categoria': 'vestido',
                'imagen_url': 'imagenes/vestido 2.png',
                'stock': 15
            },
            {
                'nombre': 'Flowing Light Hymn Dress',
                'descripcion': 'Vestido fluido con detalles de luz, diseño exclusivo',
                'precio': 399999,
                'talla': 'S/M/L',
                'color': 'Azul',
                'categoria': 'vestido',
                'imagen_url': 'imagenes/vestido 3.png',
                'stock': 8
            },
            # CORSÉS
            {
                'nombre': 'Perla Encantada',
                'descripcion': 'Corsé elegante con detalles de perlas incrustadas',
                'precio': 249999,
                'talla': 'S/M/L',
                'color': 'Perla',
                'categoria': 'corset',
                'imagen_url': 'imagenes/CORSET 3.png',
                'stock': 12
            },
            {
                'nombre': 'Dama Carmesí',
                'descripcion': 'Corsé rojo carmesí con ajuste perfecto',
                'precio': 189999,
                'talla': 'S/M/L',
                'color': 'Rojo',
                'categoria': 'corset',
                'imagen_url': 'imagenes/CORSET 4.png',
                'stock': 10
            },
            {
                'nombre': 'Aurora de Cristal',
                'descripcion': 'Corsé con cristales brillantes, diseño premium',
                'precio': 329999,
                'talla': 'S/M/L',
                'color': 'Cristal',
                'categoria': 'corset',
                'imagen_url': 'imagenes/CORSET 5.png',
                'stock': 7
            },
            {
                'nombre': 'Susurro de Cielo',
                'descripcion': 'Corsé celestial azul con bordados delicados',
                'precio': 159999,
                'talla': 'S/M/L',
                'color': 'Azul Cielo',
                'categoria': 'corset',
                'imagen_url': 'imagenes/CORSET 6.png',
                'stock': 9
            },
            {
                'nombre': 'Rosa de Ensueño',
                'descripcion': 'Corsé rosa de ensueño con detalles románticos',
                'precio': 219999,
                'talla': 'S/M/L',
                'color': 'Rosa',
                'categoria': 'corset',
                'imagen_url': 'imagenes/CORSET 7.png',
                'stock': 11
            },
            {
                'nombre': 'Jardín Secreto',
                'descripcion': 'Vestido corsé con detalles florales y encajes',
                'precio': 349999,
                'talla': 'S/M/L',
                'color': 'Verde',
                'categoria': 'vestido',
                'imagen_url': 'imagenes/VESTIDO CORSET 1.png',
                'stock': 6
            }
        ]
        
        print("\n📦 Insertando productos...")
        for producto_data in productos:
            producto = Producto(**producto_data)
            db.session.add(producto)
        
        db.session.commit()
        print(f"✅ {len(productos)} productos insertados!")
        
        print("\n" + "="*70)
        print("📋 PRODUCTOS EN LA BASE DE DATOS:")
        print("="*70)
        for p in Producto.query.all():
            print(f"ID: {p.id:2d} | {p.nombre:35s} | ${p.precio:>10,.0f} | {p.categoria}")
        print("="*70)
        print("\n👤 Usuario Admin creado:")
        print("   Email: admin@glamrent.com")
        print("   Password: admin123")
        print("\n🎉 ¡Base de datos lista!")

if __name__ == '__main__':
    print("🌟 GLAM RENT - Inicializador de Base de Datos")
    print("="*70)
    seed_database()