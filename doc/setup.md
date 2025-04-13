# Configuración del Entorno Virtual (venv) en Python

Sigue estos pasos para configurar y activar un entorno virtual en Python utilizando los scripts de la carpeta "Scripts".

## Requisitos Previos
- Asegúrate de tener Python instalado en tu sistema.

## Pasos para Configurar el Entorno Virtual

1. Abre una terminal o línea de comandos en la raíz del proyecto.
2. Ejecuta el script `setup` para crear el entorno virtual:
    - En Windows:
      ```cmd
      Scripts\setup.bat
      ```
    - En Linux/MacOS:
      ```bash
      ./Scripts/setup.sh
      ```

## Activar el Entorno Virtual

Antes de trabajar, activa el entorno virtual con los siguientes comandos:

- **Windows**:
  ```cmd
  venv\Scripts\activate
  ```
- **Linux/MacOS**:
  ```bash
  source venv/bin/activate
  ```

Una vez activado, puedes instalar dependencias o ejecutar tu aplicación dentro del entorno virtual.

