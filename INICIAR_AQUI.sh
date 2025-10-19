#!/bin/bash

clear

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         🌟 GLAM RENT - Iniciador Automático 🌟               ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "📋 Verificando sistema..."
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "app.py" ]; then
    echo "❌ Error: No se encuentra app.py"
    echo "   Por favor ejecuta este script desde la carpeta del proyecto"
    exit 1
fi

echo "✅ Archivos encontrados"
echo ""

# Verificar Python
if command -v python3 &> /dev/null; then
    echo "✅ Python3 instalado"
else
    echo "❌ Python3 no encontrado"
    exit 1
fi

echo ""
echo "🔍 Ejecutando diagnóstico..."
python3 diagnostico_completo.py

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                   🚀 INICIANDO SERVIDOR 🚀                    ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "📝 CREDENCIALES DE ADMIN:"
echo "   📧 Email: admin@glamrent.com"
echo "   🔑 Password: admin123"
echo ""
echo "🌐 Abre tu navegador en:"
echo "   👉 http://localhost:5000"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚠️  NO CIERRES ESTA VENTANA mientras uses la aplicación"
echo "⚠️  Para detener: presiona Ctrl+C"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Iniciando en 3 segundos..."
sleep 3

python3 app.py
