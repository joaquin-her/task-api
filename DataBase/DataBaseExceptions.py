"""
Módulo de excepciones personalizadas para una aplicación de gestión de tareas.

Este módulo define varias excepciones personalizadas que se utilizan en la aplicación
para representar diferentes tipos de errores.
"""

class UnknownIndexException(Exception):
    def __init__(self, mensaje):
        """
        Excepción que se lanza cuando se intenta crear o modificar una tarea con datos inválidos.

        Atributos:
            mensaje (str): Un mensaje que describe el error.
        """
        super().__init__(mensaje)
        self.mensaje = mensaje
        pass


class ModificationError(Exception):
    """Excepcion que se lanza al modificar un elemento de manera incorrecta """
    def __init__(self):
        super().__init__(f"El ojeto a modificar tuvo un error al modificarse")