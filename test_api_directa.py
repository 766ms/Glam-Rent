#!/usr/bin/env python3
"""
Test directo de la API
"""
import requests
import json

print("="*70)
print("🧪 TEST DIRECTO DE LA API")
print("="*70)

# Test 1: Health check
print("\n1️⃣ Test de Health Check:")
print("-" * 70)
try:
    response = requests.get('http://localhost:5000/api/health', timeout=5)
    print(f"   Estado: {response.status_code}")
    print(f"   Respuesta: {response.json()}")
    if response.status_code == 200:
        print("   ✅ Servidor funcionando")
    else:
        print("   ❌ Servidor con problemas")
except Exception as e:
    print(f"   ❌ Error: {e}")
    print("   ⚠️  El servidor NO está corriendo")
    print("   🔧 Ejecuta: python3 app.py")
    exit(1)

# Test 2: Obtener productos
print("\n2️⃣ Test de API de Productos:")
print("-" * 70)
try:
    response = requests.get('http://localhost:5000/api/productos', timeout=5)
    print(f"   Estado: {response.status_code}")
    
    if response.status_code == 200:
        productos = response.json()
        print(f"   ✅ API funcionando correctamente")
        print(f"   📦 Productos recibidos: {len(productos)}")
        
        if len(productos) > 0:
            print("\n   📋 Primeros 3 productos:")
            for i, p in enumerate(productos[:3], 1):
                print(f"\n   {i}. {p['nombre']}")
                print(f"      Precio: ${p['precio']:,.0f}")
                print(f"      Stock: {p['stock']}")
                print(f"      Imagen: {p['imagen_url']}")
        else:
            print("   ⚠️  La API responde pero NO hay productos")
    else:
        print(f"   ❌ Error: {response.status_code}")
        print(f"   Respuesta: {response.text}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Verificar CORS
print("\n3️⃣ Test de CORS:")
print("-" * 70)
try:
    response = requests.get('http://localhost:5000/api/productos', timeout=5)
    headers = response.headers
    
    if 'Access-Control-Allow-Origin' in headers:
        print(f"   ✅ CORS habilitado: {headers['Access-Control-Allow-Origin']}")
    else:
        print("   ⚠️  CORS no encontrado en headers")
        print("   Esto podría causar problemas en el navegador")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: Verificar archivos estáticos
print("\n4️⃣ Test de Archivos Estáticos:")
print("-" * 70)
archivos_test = [
    ('/', 'index.html'),
    ('/script.js', 'script.js'),
    ('/styles.css', 'styles.css'),
    ('/imagenes/vestido%201.png', 'imagen vestido 1')
]

for url, nombre in archivos_test:
    try:
        response = requests.get(f'http://localhost:5000{url}', timeout=5)
        if response.status_code == 200:
            print(f"   ✅ {nombre} - {response.status_code} ({len(response.content):,} bytes)")
        else:
            print(f"   ❌ {nombre} - {response.status_code}")
    except Exception as e:
        print(f"   ❌ {nombre} - Error: {e}")

print("\n" + "="*70)
print("📊 CONCLUSIÓN")
print("="*70)

try:
    response = requests.get('http://localhost:5000/api/productos', timeout=5)
    if response.status_code == 200 and len(response.json()) > 0:
        print("\n✅ La API está funcionando PERFECTAMENTE")
        print("✅ Los productos EXISTEN y se pueden obtener")
        print("\n⚠️  Si los productos NO aparecen en el navegador:")
        print("   1. Abre la consola del navegador (F12)")
        print("   2. Ve a la pestaña 'Console'")
        print("   3. Busca errores en rojo")
        print("   4. Copia el error y dímelo")
        print("\n💡 También puedes:")
        print("   - Refrescar la página con Ctrl + Shift + R")
        print("   - Borrar caché del navegador")
        print("   - Probar en modo incógnito")
    else:
        print("\n❌ Hay un problema con la API o la base de datos")
        print("   Ejecuta: python3 diagnostico_completo.py")
except:
    print("\n❌ No se puede conectar al servidor")
    print("   Ejecuta: python3 app.py")

print("\n" + "="*70 + "\n")
