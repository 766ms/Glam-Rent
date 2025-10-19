#!/usr/bin/env python3
"""
Script de diagnóstico completo para GLAM RENT
"""
from app import app, db, Usuario, Producto
import os

print("="*70)
print("🔍 DIAGNÓSTICO COMPLETO DE GLAM RENT")
print("="*70)

with app.app_context():
    # 1. Verificar base de datos
    print("\n📦 1. VERIFICANDO BASE DE DATOS:")
    print("-" * 70)
    
    db_path = 'instance/tienda_vestidos.db'
    if os.path.exists(db_path):
        print(f"   ✅ Base de datos existe en: {db_path}")
        size = os.path.getsize(db_path)
        print(f"   📊 Tamaño: {size:,} bytes")
    else:
        print(f"   ❌ Base de datos NO existe en: {db_path}")
        print("   🔧 Solución: Ejecuta 'python3 seed_products.py'")
    
    # 2. Verificar productos
    print("\n🛍️  2. VERIFICANDO PRODUCTOS:")
    print("-" * 70)
    try:
        productos = Producto.query.all()
        print(f"   📦 Total productos en BD: {len(productos)}")
        
        if len(productos) == 0:
            print("   ❌ NO HAY PRODUCTOS EN LA BASE DE DATOS")
            print("   🔧 Solución: Ejecuta 'python3 seed_products.py'")
        else:
            print("\n   ✅ Productos encontrados:")
            for i, p in enumerate(productos[:5], 1):
                print(f"      {i}. {p.nombre}")
                print(f"         Stock: {p.stock} | Precio: ${p.precio:,.0f}")
                print(f"         Imagen: {p.imagen_url}")
            
            if len(productos) > 5:
                print(f"      ... y {len(productos) - 5} más")
    except Exception as e:
        print(f"   ❌ Error al consultar productos: {e}")
    
    # 3. Verificar usuario admin
    print("\n👤 3. VERIFICANDO USUARIO ADMIN:")
    print("-" * 70)
    try:
        admin = Usuario.query.filter_by(email='admin@glamrent.com').first()
        
        if admin:
            print(f"   ✅ Usuario admin encontrado:")
            print(f"      Email: {admin.email}")
            print(f"      Nombre: {admin.nombre}")
            print(f"      Es Admin: {admin.es_admin}")
            
            if not admin.es_admin:
                print("\n   ⚠️  EL USUARIO EXISTE PERO NO ES ADMIN")
                print("   🔧 Corrigiendo...")
                admin.es_admin = True
                db.session.commit()
                print("   ✅ Usuario actualizado a admin")
            
            # Probar password
            from werkzeug.security import check_password_hash
            if check_password_hash(admin.password, 'admin123'):
                print("   ✅ Contraseña 'admin123' es correcta")
            else:
                print("   ❌ Contraseña 'admin123' NO funciona")
                print("   🔧 Reseteando contraseña...")
                from werkzeug.security import generate_password_hash
                admin.password = generate_password_hash('admin123')
                db.session.commit()
                print("   ✅ Contraseña reseteada a 'admin123'")
        else:
            print("   ❌ Usuario admin NO existe")
            print("   🔧 Creando usuario admin...")
            from werkzeug.security import generate_password_hash
            nuevo_admin = Usuario(
                nombre='Admin GLAM RENT',
                email='admin@glamrent.com',
                password=generate_password_hash('admin123'),
                es_admin=True
            )
            db.session.add(nuevo_admin)
            db.session.commit()
            print("   ✅ Usuario admin creado exitosamente")
    except Exception as e:
        print(f"   ❌ Error al verificar admin: {e}")
    
    # 4. Verificar todos los usuarios
    print("\n👥 4. TODOS LOS USUARIOS EN LA BD:")
    print("-" * 70)
    try:
        usuarios = Usuario.query.all()
        print(f"   Total usuarios: {len(usuarios)}")
        for u in usuarios:
            admin_badge = "👑 ADMIN" if u.es_admin else "👤 Usuario"
            print(f"   {admin_badge} | {u.email} | {u.nombre}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 5. Verificar imágenes
    print("\n🖼️  5. VERIFICANDO IMÁGENES:")
    print("-" * 70)
    if os.path.exists('imagenes'):
        imagenes = os.listdir('imagenes')
        print(f"   📁 Carpeta 'imagenes' existe")
        print(f"   🖼️  Total archivos: {len(imagenes)}")
        
        # Mostrar algunas
        for img in sorted(imagenes)[:5]:
            path = os.path.join('imagenes', img)
            size = os.path.getsize(path)
            print(f"      ✅ {img} ({size:,} bytes)")
        
        if len(imagenes) > 5:
            print(f"      ... y {len(imagenes) - 5} más")
    else:
        print("   ❌ Carpeta 'imagenes' NO existe")
    
    # 6. Verificar archivos principales
    print("\n📄 6. VERIFICANDO ARCHIVOS PRINCIPALES:")
    print("-" * 70)
    archivos = ['app.py', 'script.js', 'styles.css', 'index.html']
    for archivo in archivos:
        if os.path.exists(archivo):
            size = os.path.getsize(archivo)
            print(f"   ✅ {archivo} ({size:,} bytes)")
        else:
            print(f"   ❌ {archivo} NO existe")

print("\n" + "="*70)
print("📋 RESUMEN DEL DIAGNÓSTICO")
print("="*70)

with app.app_context():
    productos_ok = Producto.query.count() > 0
    admin_ok = Usuario.query.filter_by(email='admin@glamrent.com', es_admin=True).first() is not None
    imagenes_ok = os.path.exists('imagenes') and len(os.listdir('imagenes')) > 0
    
    print(f"\n   {'✅' if productos_ok else '❌'} Productos: {'OK' if productos_ok else 'FALTA CORREGIR'}")
    print(f"   {'✅' if admin_ok else '❌'} Usuario Admin: {'OK' if admin_ok else 'FALTA CORREGIR'}")
    print(f"   {'✅' if imagenes_ok else '❌'} Imágenes: {'OK' if imagenes_ok else 'FALTA CORREGIR'}")
    
    if productos_ok and admin_ok and imagenes_ok:
        print("\n   🎉 ¡TODO ESTÁ LISTO!")
        print("\n   📝 PARA INICIAR:")
        print("      1. python3 app.py")
        print("      2. Abrir: http://localhost:5000")
        print("      3. Login: admin@glamrent.com / admin123")
    else:
        print("\n   ⚠️  HAY PROBLEMAS QUE CORREGIR")
        
        if not productos_ok:
            print("\n   🔧 Para corregir productos:")
            print("      python3 seed_products.py")
        
        if not admin_ok:
            print("\n   🔧 Para corregir admin:")
            print("      Este script ya lo corrigió automáticamente ✅")
        
        if not imagenes_ok:
            print("\n   🔧 Para corregir imágenes:")
            print("      Verifica que la carpeta 'imagenes' existe")

print("\n" + "="*70)
print("🎯 Ejecuta este diagnóstico después de cada cambio")
print("="*70 + "\n")
