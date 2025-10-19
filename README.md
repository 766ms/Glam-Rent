# 🌟 GLAM RENT - Sistema de Alquiler de Vestidos de Gala

Sistema web completo para la gestión de alquiler de vestidos de gala con panel de administración.

## ✨ Características Implementadas

### Para Usuarios
- ✅ Registro e inicio de sesión
- ✅ Catálogo de productos con filtros (categoría, color, precio)
- ✅ Sistema de favoritos
- ✅ Carrito de compras
- ✅ Sistema de pagos con tarjetas de prueba
- ✅ Historial de pedidos
- ✅ Perfil de usuario editable

### Para Administradores
- ✅ Panel de administración completo
- ✅ Gestión de pedidos con estados (Pendiente, Procesando, Enviado, Entregado, Cancelado)
- ✅ Gestión de stock de productos
- ✅ Estadísticas de ventas y pedidos
- ✅ Vista detallada de información de clientes

## 🔧 Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Base de datos**: SQLite
- **Autenticación**: JWT
- **Seguridad**: Werkzeug (hash de contraseñas)

## 📦 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd <nombre-del-proyecto>
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Inicializar la base de datos**
```bash
python3 seed_products.py
```
Este comando:
- Crea la base de datos
- Inserta productos de ejemplo
- Crea un usuario administrador por defecto

## 🚀 Uso

### Iniciar el servidor

```bash
python3 app.py
```

El servidor se iniciará en `http://localhost:5000`

### Abrir la aplicación

Abre tu navegador y visita:
```
http://localhost:5000/index.html
```

## 👤 Credenciales de Acceso

### Usuario Administrador (Creado automáticamente)
- **Email**: `admin@glamrent.com`
- **Contraseña**: `admin123`

### Crear Usuario Administrador Manual

Si necesitas crear un nuevo usuario administrador, ejecuta:

```bash
python3 crear_admin.py
```

El script te guiará paso a paso para crear el usuario.

## 💳 Tarjetas de Prueba

Para probar el sistema de pagos, usa las siguientes tarjetas:

- ✅ **Pago Exitoso**: `4242 4242 4242 4242`
- ❌ **Pago Rechazado**: `4000 0000 0000 0002`
- **CVV**: Cualquier 3 dígitos
- **Fecha de expiración**: Cualquier fecha futura (MM/AA)

## 🛠️ Correcciones Realizadas

### 1. Error en Favoritos
- **Problema**: Error al agregar productos a favoritos
- **Solución**: Corregida la verificación de estructura de datos en `toggleFavorite()`
- **Detalles**: Se agregó validación adicional para manejar correctamente la respuesta del backend

### 2. Error en Pagos
- **Problema**: Error al procesar pagos con tarjeta de prueba
- **Solución**: Sincronización del carrito local con el backend antes del pago
- **Detalles**: El carrito se mantenía solo en localStorage, ahora se sincroniza con la API antes de procesar el pedido

### 3. Panel de Administración
- **Agregado**: Sistema completo de gestión de stock
- **Características**:
  - Vista de todos los productos con su stock actual
  - Edición individual del stock de cada producto
  - Indicadores visuales (verde: stock OK, amarillo: stock bajo, rojo: sin stock)
  - Estadísticas de inventario

## 📱 Funcionalidades del Panel de Admin

### Gestión de Pedidos
- Ver todos los pedidos del sistema
- Información completa del cliente (nombre, email, dirección)
- Cambiar estado de pedidos
- Ver detalle de productos por pedido
- Estadísticas: total de pedidos, ingresos, pedidos pendientes

### Gestión de Inventario
- Ver todos los productos
- Editar stock de cada producto
- Alertas de stock bajo (≤ 2 unidades)
- Estadísticas: total productos, stock total, productos con bajo stock

## 📂 Estructura del Proyecto

```
/
├── app.py                  # Backend Flask
├── script.js              # Frontend JavaScript
├── index.html             # Interfaz principal
├── styles.css             # Estilos
├── requirements.txt       # Dependencias Python
├── seed_products.py       # Script de inicialización
├── crear_admin.py         # Script para crear admins
├── instance/
│   └── tienda_vestidos.db # Base de datos SQLite
└── imagenes/              # Recursos visuales
```

## 🔒 Seguridad

- Contraseñas hasheadas con Werkzeug
- Autenticación JWT con tokens
- Validación de roles (usuario/administrador)
- Protección de rutas administrativas

## 🎨 Características de UI/UX

- Diseño responsive (mobile-first)
- Animaciones suaves
- Notificaciones en tiempo real
- Modales para una mejor experiencia
- Filtros dinámicos de productos
- Sistema de búsqueda

## 📝 Endpoints de API

### Públicos
- `POST /api/registro` - Registrar nuevo usuario
- `POST /api/login` - Iniciar sesión
- `GET /api/productos` - Obtener todos los productos
- `GET /api/productos/buscar` - Buscar productos

### Autenticados (requieren token)
- `GET /api/perfil` - Obtener perfil del usuario
- `PUT /api/perfil` - Actualizar perfil
- `GET /api/favoritos` - Obtener favoritos
- `POST /api/favoritos` - Agregar a favoritos
- `DELETE /api/favoritos/<id>` - Eliminar de favoritos
- `GET /api/carrito` - Obtener carrito
- `POST /api/carrito` - Agregar al carrito
- `PUT /api/carrito/<id>` - Actualizar cantidad
- `DELETE /api/carrito/<id>` - Eliminar del carrito
- `GET /api/pedidos` - Obtener pedidos del usuario
- `POST /api/pedidos` - Crear nuevo pedido

### Administrativos (requieren token de admin)
- `GET /api/admin/pedidos` - Obtener todos los pedidos
- `PUT /api/admin/pedidos/<id>/estado` - Actualizar estado de pedido
- `GET /api/admin/productos` - Obtener todos los productos (admin)
- `PUT /api/admin/productos/<id>/stock` - Actualizar stock de producto

## 🐛 Reportar Problemas

Si encuentras algún error, por favor abre un issue en el repositorio.

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👥 Contacto

- **GitHub**: https://github.com/766ms
- **Discord**: 756193168965369958
- **Twitter**: @766ms_

---

🎉 ¡Gracias por usar GLAM RENT!
