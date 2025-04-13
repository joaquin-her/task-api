#!/bin/bash

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Python3 no está instalado. Por favor, instálalo antes de continuar."
    exit 1
fi

# Crear el entorno virtual
echo "Creando el entorno virtual..."
python3 -m venv venv

# Activar el entorno virtual
echo "Activando el entorno virtual..."
source venv/bin/activate

# Verificar si requirements.txt existe
if [ ! -f "requirements.txt" ]; then
    echo "El archivo requirements.txt no se encontró en el directorio actual."
    deactivate
    exit 1
fi

# Instalar las dependencias
echo "Instalando dependencias desde requirements.txt..."
pip install -r requirements.txt

echo "El entorno virtual está listo y las dependencias han sido instaladas."