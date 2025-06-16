#!/bin/bash

echo "🛠️ Configurando entorno para CULTIViA..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Entorno configurado. Ejecuta con: source venv/bin/activate"
