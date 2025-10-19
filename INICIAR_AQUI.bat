@echo off
chcp 65001 > nul
cls

echo ╔════════════════════════════════════════════════════════════════╗
echo ║         🌟 GLAM RENT - Iniciador Automático 🌟               ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo 📋 Verificando sistema...
echo.

if not exist "app.py" (
    echo ❌ Error: No se encuentra app.py
    echo    Por favor ejecuta este script desde la carpeta del proyecto
    pause
    exit /b 1
)

echo ✅ Archivos encontrados
echo.

python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado
    echo    Instala Python desde https://www.python.org/
    pause
    exit /b 1
)

echo ✅ Python instalado
echo.

echo 🔍 Ejecutando diagnóstico...
python diagnostico_completo.py

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                   🚀 INICIANDO SERVIDOR 🚀                    ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo 📝 CREDENCIALES DE ADMIN:
echo    📧 Email: admin@glamrent.com
echo    🔑 Password: admin123
echo.
echo 🌐 Abre tu navegador en:
echo    👉 http://localhost:5000
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ⚠️  NO CIERRES ESTA VENTANA mientras uses la aplicación
echo ⚠️  Para detener: presiona Ctrl+C
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo Iniciando en 3 segundos...
timeout /t 3 > nul

python app.py
