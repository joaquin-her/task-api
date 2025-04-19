from datetime import datetime

STATUS_VALUES = ["to-do", "done", "in-progress"]

class Task(object):
	"""docstring for Task"""
	def __init__(self, description: str):
		self.description = description
		self.status = 'to-do'
		self.created = datetime.now().isoformat()
		self.updated = self.created

	def to_dict(self)-> dict : 
		dict = {
			"description": self.description,
			"status": self.status,
			"created": self.created,
			"updated": self.updated
		}
		return dict
	
	def setStatus(self, status: str):
		if not isinstance(status, str):
			raise TypeError("El argumento 'status' debe ser de tipo str")
		if status in STATUS_VALUES:
			self.status = status
			self.updateDatetime()
			return
		raise UnknownStatusException(status)

	def setDescription(self, description: str):
		if not isinstance(description, str):
			raise TypeError("El argumento 'description' debe ser de tipo str")
		self.description = description
		self.updateDatetime()
		return

	@classmethod
	def fromDict(cls, dict: dict)-> dict :
		task = Task(dict["description"])
		for key, value in dict.items():
			if hasattr(task, key):
				setattr(task, key, value)
		return task
	
	def update(self, field:str, value:str):
		if (field == "description"):
			self.setDescription(value)
		elif (field == "status"):
			self.setStatus(value)
		else:
			raise UnknownFieldException(field)

	def updateDatetime(self):
		""" Actualiza el campo 'updated' a este instante """
		self.updated = datetime.now().isoformat()

	def __str__(self):
		""" Devuelve formateado a string el objeto Task """
		return (
			f"Task:\n"
			f"  Description: {self.description}\n"
			f"  Status: {self.status}\n"
			f"  Created: {self.created}\n"
			f"  Updated: {self.updated}"
		)
	
class UnknownStatusException(Exception):
	"""Excepcion que se lanza cuando se ingresa un Status desconocido"""
	def __init__(self, status):
		super().__init__(f"El status '{status}' no es valido o es deconocido ")
		self.mensaje = f"El status '{status}' no es valido o es deconocido "
		
class UnknownFieldException(Exception):
	"""Excepcion que se lanza cuando se ingresa un campo desconocido"""
	def __init__(self, field):
		super().__init__(f"El campo '{field}' no es valido. ")
		
