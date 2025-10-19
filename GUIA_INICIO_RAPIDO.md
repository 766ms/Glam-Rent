# 🚀 Guía de Inicio Rápido - GLAM RENT

## ✅ Todo está listo, solo sigue estos pasos:

### 1️⃣ Iniciar el Servidor

Abre una terminal en la carpeta `/workspace` y ejecuta:

```bash
python3 app.py
```

O usa el script de inicio:

```bash
./iniciar_servidor.sh
```

Deberías ver:

```
🚀 Servidor GLAM RENT iniciado
📦 Backend en http://localhost:5000
🌐 Abre: http://localhost:5000
 * Running on http://127.0.0.1:5000
```

### 2️⃣ Abrir en el Navegador

Abre tu navegador y ve a:

```
http://localhost:5000
```

O también puedes usar:

```
http://localhost:5000/index.html
```

### 3️⃣ Verificar que Todo Funciona

✅ **Deberías ver:**
- Logo de GLAM RENT en la esquina superior izquierda
- Menú de navegación (Inicio, Quiénes Somos, Login, etc.)
- Banner principal con filtros
- **9 productos con imágenes**

Si ves los productos pero sin imágenes:
- Presiona `Ctrl + Shift + R` (recarga forzada)
- O abre en modo incógnito

### 4️⃣ Probar el Panel de Admin

1. Click en **"Login"**
2. Ingresa credenciales:
   - **Email:** `admin@glamrent.com`
   - **Contraseña:** `admin123`
3. Después de iniciar sesión, verás el botón **"🔧 Admin"**
4. Click en "Admin" para ver:
   - Gestión de pedidos
   - Gestión de inventario

---

## 🐛 Solución de Problemas

### ❌ No aparecen los productos

**Verifica que el servidor esté corriendo:**

```bash
# En otra terminal
curl http://localhost:5000/api/productos
```

Deberías ver un JSON con 9 productos.

### ❌ No aparecen las imágenes

**Verifica que las imágenes existan:**

```bash
ls -la imagenes/
```

Deberías ver:
- `vestido 1.png`
- `vestido 2.png`
- `CORSET 3.png`
- etc.

**Solución:**
1. Recarga la página con `Ctrl + Shift + R`
2. Abre la consola del navegador (F12) y busca errores
3. Asegúrate de que el servidor esté corriendo en `http://localhost:5000`

### ❌ Error "Module not found"

```bash
pip install -r requirements.txt
```

---

## 📊 Estado Actual del Sistema

```bash
# Ver productos en la base de datos
python3 -c "from app import app, Producto; app.app_context().push(); print(f'Productos: {Producto.query.count()}')"

# Ver usuario admin
python3 -c "from app import app, Usuario; app.app_context().push(); admin = Usuario.query.filter_by(es_admin=True).first(); print(f'Admin: {admin.email if admin else \"No existe\"}')"
```

---

## 🎮 Funcionalidades Listas para Probar

### Usuario Normal:
✅ Registrarse
✅ Iniciar sesión
✅ Ver productos
✅ Filtrar por categoría, color, precio
✅ Agregar a favoritos ❤️
✅ Agregar al carrito 🛒
✅ Realizar compras con tarjeta de prueba
✅ Ver historial de pedidos

### Usuario Admin:
✅ Ver todos los pedidos
✅ Cambiar estado de pedidos
✅ Ver todos los productos
✅ Editar stock de productos
✅ Ver estadísticas

---

## 💳 Tarjetas de Prueba

Para probar pagos:

- ✅ **Exitosa:** `4242 4242 4242 4242`
- ❌ **Rechazada:** `4000 0000 0000 0002`
- **CVV:** Cualquier 3 dígitos
- **Fecha:** Cualquier fecha futura (MM/AA)

---

## 📞 ¿Necesitas Ayuda?

Si algo no funciona:

1. Verifica que el servidor esté corriendo
2. Revisa la consola del navegador (F12)
3. Revisa la terminal donde corre el servidor
4. Asegúrate de estar en `http://localhost:5000` (no file://)

---

🎉 **¡Disfruta de GLAM RENT!**
