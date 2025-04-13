@echo off

:: Verificar si Python está instalado
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python no está instalado. Por favor, instálalo antes de continuar.
    exit /b 1
)

:: Crear el entorno virtual
echo Creando el entorno virtual...
python -m venv venv

:: Activar el entorno virtual
echo Activando el entorno virtual...
call venv\Scripts\activate

:: Verificar si requirements.txt existe
if not exist "requirements.txt" (
    echo El archivo requirements.txt no se encontró en el directorio actual.
    deactivate
    exit /b 1
)

:: Instalar las dependencias
echo Instalando dependencias desde requirements.txt...
pip install -r requirements.txt

echo El entorno virtual está listo y las dependencias han sido instaladas.