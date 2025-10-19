# 🚀 CÓMO INICIAR GLAM RENT

## ⚡ Proceso Simple en 2 Pasos:

---

### 📍 PASO 1: Abre una Terminal

**En tu computadora, abre una terminal/consola y escribe:**

```bash
cd /workspace
python3 app.py
```

**Presiona ENTER.**

---

### ✅ Verás esto:

```
🚀 Servidor GLAM RENT iniciado
📦 Backend en http://localhost:5000
🌐 Abre: http://localhost:5000
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server.
 * Running on http://127.0.0.1:5000
```

✅ **¡Perfecto!** El servidor está corriendo.

⚠️ **NO CIERRES ESTA TERMINAL** - debe quedarse abierta mientras usas la aplicación.

---

### 📍 PASO 2: Abre tu Navegador

**Con el servidor corriendo, abre tu navegador favorito (Chrome, Firefox, Edge, Safari) y escribe en la barra de direcciones:**

```
http://localhost:5000
```

**O prueba la página de test:**

```
http://localhost:5000/test_admin.html
```

---

## ✅ ¿Qué Deberías Ver?

### En el navegador (`http://localhost:5000`):
- Logo de GLAM RENT
- Banner principal
- 9 productos con imágenes
- Botones de Login, Carrito, etc.

### En la página de test (`http://localhost:5000/test_admin.html`):
- Pruebas automáticas
- Estado del servidor (✅ verde)
- Estado del usuario admin (✅ verde)
- Instrucciones paso a paso

---

## 🎮 Después de Ver la Página Principal:

1. **Click en "Login"**
2. **Ingresa:**
   - Email: `admin@glamrent.com`
   - Contraseña: `admin123`
3. **Click en "Ingresar"**
4. **Verás el botón "🔧 Admin"**
5. **Click en "Admin"** para abrir el panel

---

## ❌ Errores Comunes:

### Error 1: "No se puede conectar"

**Significa:** El servidor NO está corriendo

**Solución:** Ve al PASO 1 arriba e inicia el servidor con `python3 app.py`

---

### Error 2: "No aparecen las imágenes"

**Significa:** Estás abriendo el archivo HTML directamente (file://)

**Solución:** 
1. Cierra el navegador
2. Verifica que el servidor esté corriendo
3. Abre `http://localhost:5000` (no file://)

---

### Error 3: "No veo el botón Admin"

**Significa:** No iniciaste sesión como admin

**Solución:**
1. Click en "Login"
2. Usa: `admin@glamrent.com` / `admin123`
3. El botón aparecerá después del login

---

## 🔄 Para Detener el Servidor:

En la terminal donde está corriendo, presiona:

```
Ctrl + C
```

---

## 🔄 Para Reiniciar el Servidor:

```bash
# Si lo detuviste, vuelve a iniciar:
python3 app.py
```

---

## 📊 Resumen:

```
┌──────────────────────────────────┐
│  1. Terminal                     │
│     cd /workspace                │
│     python3 app.py               │
│     [DEJAR CORRIENDO]            │
└──────────────────────────────────┘
           ↓
┌──────────────────────────────────┐
│  2. Navegador                    │
│     http://localhost:5000        │
└──────────────────────────────────┘
           ↓
┌──────────────────────────────────┐
│  3. Login                        │
│     admin@glamrent.com           │
│     admin123                     │
└──────────────────────────────────┘
           ↓
┌──────────────────────────────────┐
│  4. Panel Admin                  │
│     Click en "🔧 Admin"          │
└──────────────────────────────────┘
```

---

## 🎉 ¡Eso es todo!

**Recuerda:** 
1. ✅ Primero la terminal con `python3 app.py`
2. ✅ Luego el navegador con `http://localhost:5000`

**NO al revés.**
