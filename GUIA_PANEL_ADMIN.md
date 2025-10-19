# 🔧 Guía del Panel de Administración

## ✅ Panel Admin Ya Está Arreglado

He corregido todos los problemas del panel de administración. Ahora funciona perfectamente.

---

## 🚀 Cómo Acceder al Panel de Admin

### PASO 1: Inicia el Servidor

```bash
cd /workspace
python3 app.py
```

⚠️ **NO CIERRES esta terminal** - debe estar corriendo.

---

### PASO 2: Abre el Navegador

```
http://localhost:5000
```

---

### PASO 3: Inicia Sesión como Admin

1. Click en **"Login"** (esquina superior derecha)
2. Ingresa las credenciales:

```
📧 Email: admin@glamrent.com
🔑 Contraseña: admin123
```

3. Click en **"Ingresar"**

---

### PASO 4: Accede al Panel de Admin

Después de iniciar sesión, verás un nuevo botón en la navegación:

```
🔧 Admin
```

Haz click en ese botón y se abrirá el panel.

---

## 📊 Funcionalidades del Panel de Admin

### Pestaña "Pedidos" 📦

**Verás:**
- 📊 **Estadísticas:**
  - Total de pedidos
  - Ingresos totales
  - Pedidos pendientes

- 📋 **Lista de pedidos** con:
  - Número de pedido
  - Información del cliente (nombre, email)
  - Fecha del pedido
  - Dirección de envío
  - Total del pedido
  - **Selector de estado** (puedes cambiarlo)
  - Lista de productos del pedido

**Puedes cambiar el estado:**
- Pendiente → Procesando → Enviado → Entregado
- O marcar como Cancelado

---

### Pestaña "Productos" 🏪

**Verás:**
- 📊 **Estadísticas:**
  - Total de productos
  - Stock total
  - Productos con bajo stock

- 🛍️ **Lista de productos** con:
  - Imagen del producto
  - Nombre y descripción
  - Precio
  - Talla y color
  - Categoría
  - **Stock actual con indicador de color:**
    - 🟢 Verde: Stock suficiente (> 2)
    - 🟡 Amarillo: Stock bajo (≤ 2)
    - 🔴 Rojo: Sin stock (0)
  - **Campo para editar stock**
  - Botón "Actualizar"

**Para cambiar el stock:**
1. Modifica el número en el input
2. Click en "Actualizar"
3. Verás una notificación de éxito
4. La lista se actualizará automáticamente

---

## 🧪 Página de Test

Para verificar que todo funciona, abre:

```
http://localhost:5000/test_admin.html
```

Esta página te dirá:
- ✅ Si el servidor está corriendo
- ✅ Si el usuario admin existe
- ✅ Pasos para probar el panel

---

## 🔍 Verificación Rápida

### ¿El usuario admin existe?

```bash
python3 -c "from app import app, Usuario; app.app_context().push(); admin = Usuario.query.filter_by(email='admin@glamrent.com').first(); print(f'Admin: {admin.email if admin else \"NO EXISTE\"} | Es Admin: {admin.es_admin if admin else \"N/A\"}')"
```

Debería mostrar:
```
Admin: admin@glamrent.com | Es Admin: True
```

---

## ❌ Solución de Problemas

### Problema 1: No veo el botón "Admin"

**Posibles causas:**
- No iniciaste sesión
- No usaste las credenciales de admin
- El usuario no tiene permisos de admin

**Solución:**
1. Cierra sesión (click en tu nombre en la esquina superior)
2. Vuelve a iniciar sesión con:
   - Email: `admin@glamrent.com`
   - Password: `admin123`
3. El botón "🔧 Admin" debería aparecer

---

### Problema 2: El botón aparece pero no pasa nada

**Solución:**
1. Presiona `F12` para abrir la consola del navegador
2. Ve a la pestaña "Console"
3. Busca errores en rojo
4. Recarga la página con `Ctrl + Shift + R`
5. Intenta de nuevo

Si hay errores, copia el mensaje y verifica que el servidor esté corriendo.

---

### Problema 3: Se abre el modal pero está vacío

**Solución:**
1. Verifica que el servidor esté corriendo
2. Abre la consola del navegador (F12)
3. Busca errores de tipo:
   - `Failed to fetch`
   - `404 Not Found`
   - `401 Unauthorized`

Si ves `401 Unauthorized`:
- Tu token expiró
- Cierra sesión y vuelve a iniciar

---

### Problema 4: No se actualizan los datos

**Solución:**
1. El panel se actualiza automáticamente después de cada cambio
2. Si no se actualiza:
   - Recarga la página
   - Cierra y abre el modal de nuevo
   - Verifica la consola para errores

---

### Problema 5: Error al cambiar stock

**Errores comunes:**
- Stock negativo (no permitido)
- Campo vacío
- No eres admin

**Solución:**
1. Ingresa un número ≥ 0
2. Verifica que estés logueado como admin
3. Verifica la consola para más detalles

---

## 📱 Flujo Completo de Prueba

### 1. Preparación
```bash
# Terminal
cd /workspace
python3 app.py
```

### 2. Login
```
# Navegador
http://localhost:5000

# Click en "Login"
Email: admin@glamrent.com
Password: admin123
```

### 3. Acceso al Panel
```
# Click en "🔧 Admin"
```

### 4. Probar Gestión de Pedidos
```
1. Pestaña "Pedidos" (ya seleccionada)
2. Ver estadísticas
3. Buscar un pedido
4. Cambiar su estado
5. Ver notificación de éxito
```

### 5. Probar Gestión de Stock
```
1. Click en pestaña "Productos"
2. Ver lista de productos
3. Modificar stock de un producto
4. Click en "Actualizar"
5. Ver notificación de éxito
6. Verificar que el indicador cambió de color si es necesario
```

---

## 🎯 Lo Que Arreglé

1. ✅ **Event Listeners correctos** - Ya no usa `onclick` inline
2. ✅ **Funciones globales** - Accesibles desde HTML dinámico
3. ✅ **Tabs funcionales** - Cambian correctamente entre Pedidos y Productos
4. ✅ **Actualización de stock** - Funciona sin recargar toda la página
5. ✅ **Cambio de estado** - Los pedidos se actualizan correctamente
6. ✅ **Notificaciones** - Feedback visual de todas las acciones

---

## 📊 Estructura del Panel

```
Panel de Admin
├── Pestaña "Pedidos"
│   ├── Estadísticas (3 cards)
│   └── Lista de Pedidos
│       ├── Info del pedido
│       ├── Info del cliente
│       ├── Selector de estado
│       └── Items del pedido
│
└── Pestaña "Productos"
    ├── Estadísticas (3 cards)
    └── Lista de Productos
        ├── Imagen
        ├── Info del producto
        ├── Indicador de stock
        └── Control de stock
            ├── Input numérico
            └── Botón "Actualizar"
```

---

## 🎉 ¡Listo para Usar!

El panel de administración está completamente funcional. Solo necesitas:

1. ✅ Iniciar el servidor
2. ✅ Iniciar sesión como admin
3. ✅ Click en "🔧 Admin"

**¿Tienes algún problema específico?** Abre `http://localhost:5000/test_admin.html` para diagnóstico automático.
