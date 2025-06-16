@echo off
cd /d C:\CULTIViA_paquete_2025jun16
echo Configurando entorno para CULTIViA...
python -m venv venv
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
echo Entorno listo. Usa: venv\Scripts\activate
