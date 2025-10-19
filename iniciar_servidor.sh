#!/bin/bash

echo "🚀 Iniciando GLAM RENT..."
echo ""
echo "📍 Carpeta actual: $(pwd)"
echo "✅ Productos: $(python3 -c "from app import app, Producto; app.app_context().push(); print(Producto.query.count())")"
echo ""
echo "🌐 El servidor estará disponible en:"
echo "   http://localhost:5000"
echo ""
echo "🔐 Login de admin:"
echo "   Email: admin@glamrent.com"
echo "   Password: admin123"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

python3 app.py
