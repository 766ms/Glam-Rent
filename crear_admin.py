#!/usr/bin/env python3
"""
Script para crear un usuario administrador en la base de datos
"""
from app import app, db, Usuario
from werkzeug.security import generate_password_hash

def crear_usuario_admin():
    with app.app_context():
        # Verificar si ya existe un admin
        admin_existente = Usuario.query.filter_by(email='admin@glamrent.com').first()
        
        if admin_existente:
            print("❌ Ya existe un usuario administrador con este email.")
            print(f"   Email: {admin_existente.email}")
            print(f"   Nombre: {admin_existente.nombre}")
            
            # Preguntar si quiere actualizar
            respuesta = input("\n¿Deseas actualizar este usuario a admin? (s/n): ")
            if respuesta.lower() == 's':
                admin_existente.es_admin = True
                db.session.commit()
                print("\n✅ Usuario actualizado a administrador exitosamente!")
                print(f"   Email: {admin_existente.email}")
                print(f"   Contraseña: (sin cambios)")
            else:
                print("Operación cancelada.")
            return
        
        # Crear nuevo usuario administrador
        print("=== Crear Usuario Administrador ===\n")
        
        nombre = input("Nombre del administrador [Admin GLAM RENT]: ").strip()
        if not nombre:
            nombre = "Admin GLAM RENT"
        
        email = input("Email [admin@glamrent.com]: ").strip()
        if not email:
            email = "admin@glamrent.com"
        
        # Verificar si el email ya existe
        if Usuario.query.filter_by(email=email).first():
            print(f"\n❌ Error: Ya existe un usuario con el email {email}")
            return
        
        password = input("Contraseña [admin123]: ").strip()
        if not password:
            password = "admin123"
        
        telefono = input("Teléfono (opcional): ").strip() or None
        direccion = input("Dirección (opcional): ").strip() or None
        ciudad = input("Ciudad (opcional): ").strip() or None
        
        # Crear el usuario administrador
        nuevo_admin = Usuario(
            nombre=nombre,
            email=email,
            password=generate_password_hash(password),
            telefono=telefono,
            direccion=direccion,
            ciudad=ciudad,
            es_admin=True
        )
        
        db.session.add(nuevo_admin)
        db.session.commit()
        
        print("\n✅ Usuario administrador creado exitosamente!")
        print(f"\n📋 Detalles del administrador:")
        print(f"   Nombre: {nombre}")
        print(f"   Email: {email}")
        print(f"   Contraseña: {password}")
        print(f"   Es Admin: Sí")
        if telefono:
            print(f"   Teléfono: {telefono}")
        if direccion:
            print(f"   Dirección: {direccion}")
        if ciudad:
            print(f"   Ciudad: {ciudad}")
        print("\n⚠️  Guarda esta información en un lugar seguro.")
        print("💡 Puedes iniciar sesión en http://localhost:5000 con estas credenciales.")

if __name__ == '__main__':
    try:
        crear_usuario_admin()
    except KeyboardInterrupt:
        print("\n\nOperación cancelada por el usuario.")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
