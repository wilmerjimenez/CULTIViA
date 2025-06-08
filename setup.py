"""
CultivIA - Script de Instalación y Configuración
Automatiza la instalación y configuración inicial del sistema
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import sqlite3

def print_header():
    """Mostrar header del instalador"""
    print("🌱" * 20)
    print("🌱  CultivIA - Instalador  🌱")
    print("🌱" * 20)
    print()
    print("Cultivos resilientes al cambio climático")
    print("con ayuda de la inteligencia artificial")
    print()

def check_python_version():
    """Verificar versión de Python"""
    print("🔍 Verificando versión de Python...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} no es compatible")
        print("   Se requiere Python 3.8 o superior")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def install_dependencies():
    """Instalar dependencias de Python"""
    print("\n📦 Instalando dependencias...")
    
    requirements_file = Path("requirements.txt")
    
    if not requirements_file.exists():
        print("❌ Archivo requirements.txt no encontrado")
        return False
    
    try:
        # Actualizar pip
        print("   Actualizando pip...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        
        # Instalar dependencias
        print("   Instalando paquetes...")
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                               check=True, capture_output=True, text=True)
        
        print("✅ Dependencias instaladas exitosamente")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias:")
        print(f"   {e.stderr}")
        return False

def create_directories():
    """Crear directorios necesarios"""
    print("\n📁 Creando estructura de directorios...")
    
    directories = [
        "data",
        "logs",
        "examples"
    ]
    
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"   ✅ Creado: {directory}/")
        else:
            print(f"   ℹ️ Ya existe: {directory}/")
    
    return True

def setup_environment_file():
    """Configurar archivo de variables de entorno"""
    print("\n⚙️ Configurando variables de entorno...")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("   ℹ️ Archivo .env ya existe")
        
        response = input("   ¿Deseas sobrescribirlo? (s/N): ").lower().strip()
        if response not in ['s', 'sí', 'si', 'y', 'yes']:
            print("   ⏭️ Manteniendo archivo .env existente")
            return True
    
    if not env_example.exists():
        print("   ❌ Archivo .env.example no encontrado")
        return False
    
    # Copiar archivo de ejemplo
    shutil.copy(env_example, env_file)
    print("   ✅ Archivo .env creado desde .env.example")
    
    # Solicitar configuración básica
    print("\n📝 Configuración básica (puedes cambiarla después en .env):")
    
    # API Key de OpenWeatherMap
    api_key = input("   🌤️ API Key de OpenWeatherMap (obligatorio): ").strip()
    if api_key:
        update_env_file(env_file, "OPENWEATHER_API_KEY", api_key)
        print("   ✅ API Key configurada")
    else:
        print("   ⚠️ API Key no configurada - deberás configurarla manualmente")
    
    # Email para alertas
    email = input("   📧 Email para alertas (opcional): ").strip()
    if email:
        update_env_file(env_file, "EMAIL_USERNAME", email)
        
        password = input("   🔐 Contraseña de aplicación de Gmail (opcional): ").strip()
        if password:
            update_env_file(env_file, "EMAIL_PASSWORD", password)
            print("   ✅ Email configurado")
        else:
            print("   ⚠️ Contraseña no configurada - solo se configuró el email")
    else:
        print("   ⏭️ Email no configurado")
    
    return True

def update_env_file(env_file, key, value):
    """Actualizar una variable en el archivo .env"""
    try:
        # Leer archivo
        with open(env_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Buscar y actualizar la línea
        updated = False
        for i, line in enumerate(lines):
            if line.strip().startswith(f"{key}="):
                lines[i] = f"{key}={value}\n"
                updated = True
                break
        
        # Si no se encontró, agregar al final
        if not updated:
            lines.append(f"{key}={value}\n")
        
        # Escribir archivo
        with open(env_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
    except Exception as e:
        print(f"   ⚠️ Error actualizando {key}: {e}")

def initialize_database():
    """Inicializar base de datos"""
    print("\n🗄️ Inicializando base de datos...")
    
    try:
        # Importar módulos después de instalar dependencias
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from modules.database import DatabaseManager
        from config.config import config
        
        # Crear gestor de base de datos
        db_manager = DatabaseManager(config.DATABASE_PATH)
        
        # Agregar ubicaciones por defecto
        locations = db_manager.get_locations()
        
        if not locations:
            print("   📍 Agregando ubicaciones por defecto...")
            
            for location in config.DEFAULT_LOCATIONS:
                db_manager.add_location(
                    name=location['name'],
                    latitude=location['lat'],
                    longitude=location['lon'],
                    country='España'
                )
            
            print(f"   ✅ {len(config.DEFAULT_LOCATIONS)} ubicaciones agregadas")
        else:
            print(f"   ℹ️ Base de datos ya tiene {len(locations)} ubicaciones")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error inicializando base de datos: {e}")
        return False

def test_installation():
    """Probar la instalación"""
    print("\n🧪 Probando instalación...")
    
    try:
        # Importar módulos principales
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from config.config import config
        from modules.database import DatabaseManager
        from modules.data_collector import WeatherDataCollector
        
        # Probar base de datos
        db_manager = DatabaseManager(config.DATABASE_PATH)
        stats = db_manager.get_database_stats()
        print(f"   ✅ Base de datos: {stats.get('locations_count', 0)} ubicaciones")
        
        # Probar API si está configurada
        if config.OPENWEATHER_API_KEY and config.OPENWEATHER_API_KEY != 'tu_api_key_aqui':
            collector = WeatherDataCollector(config.OPENWEATHER_API_KEY)
            if collector.test_api_connection():
                print("   ✅ API OpenWeatherMap: Conexión exitosa")
            else:
                print("   ⚠️ API OpenWeatherMap: Sin conexión")
        else:
            print("   ⚠️ API OpenWeatherMap: No configurada")
        
        print("   ✅ Instalación completada exitosamente")
        return True
        
    except Exception as e:
        print(f"   ❌ Error en pruebas: {e}")
        return False

def show_next_steps():
    """Mostrar próximos pasos"""
    print("\n🎉 ¡Instalación completada!")
    print("\n📋 Próximos pasos:")
    print()
    print("1️⃣ Configurar API Key (si no lo hiciste):")
    print("   • Visita: https://openweathermap.org/api")
    print("   • Crea una cuenta gratuita")
    print("   • Copia tu API key al archivo .env")
    print()
    print("2️⃣ Configurar alertas por email (opcional):")
    print("   • Habilita autenticación de 2 factores en Gmail")
    print("   • Genera una contraseña de aplicación")
    print("   • Configúrala en el archivo .env")
    print()
    print("3️⃣ Comandos útiles:")
    print("   • Probar sistema:     python cultivia_main.py test")
    print("   • Ver estado:         python cultivia_main.py status")
    print("   • Iniciar sistema:    python cultivia_main.py start")
    print("   • Abrir dashboard:    streamlit run dashboard.py")
    print()
    print("4️⃣ Ejemplos de uso:")
    print("   • Ejecutar ejemplos:  python examples/basic_usage.py")
    print()
    print("📚 Para más información, consulta el archivo README.md")
    print()
    print("🌱 ¡CultivIA está listo para proteger tus cultivos!")

def main():
    """Función principal del instalador"""
    print_header()
    
    try:
        # Verificar Python
        if not check_python_version():
            sys.exit(1)
        
        # Crear directorios
        if not create_directories():
            print("❌ Error creando directorios")
            sys.exit(1)
        
        # Instalar dependencias
        if not install_dependencies():
            print("❌ Error instalando dependencias")
            sys.exit(1)
        
        # Configurar entorno
        if not setup_environment_file():
            print("❌ Error configurando variables de entorno")
            sys.exit(1)
        
        # Inicializar base de datos
        if not initialize_database():
            print("❌ Error inicializando base de datos")
            sys.exit(1)
        
        # Probar instalación
        if not test_installation():
            print("❌ Error en pruebas de instalación")
            sys.exit(1)
        
        # Mostrar próximos pasos
        show_next_steps()
        
    except KeyboardInterrupt:
        print("\n⏹️ Instalación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado durante la instalación: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

