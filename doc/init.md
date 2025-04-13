# Comando: `uvicorn.exe main:app`

## Descripción
El comando `uvicorn.exe main:app` se utiliza para iniciar un servidor ASGI (Asynchronous Server Gateway Interface) que ejecuta una aplicación web desarrollada con frameworks como **FastAPI** o **Starlette**. Este comando es específico para entornos Windows, donde `uvicorn.exe` es el ejecutable de Uvicorn.

## Requisitos Previos
Antes de ejecutar este comando, asegúrate de:
1. Haber ejecutado el script de configuración (`setup`) necesario para preparar el entorno.
2. Haber activado el entorno virtual (venv).

## Sintaxis
Linux
```bash
uvicorn main:app
```
Windows
```bat
uvicorn.exe main:app
```