from .IDataBase import IDataBase
from Task import Task, UnknownFieldException, UnknownStatusException
from .DataBaseExceptions import UnknownIndexException, ModificationError
import json
import os

class JsonDataBase(IDataBase):
    """ Docstring for JsonDataBase. The URI should be a json file path """
    def __init__(self, URI:str):
        self.URI = URI
        try:
            self.data = self.loadData(URI)
        except FileNotFoundError:
            self.data = self.createData(URI)

    def loadData(self, URI):
        """Lee el archivo y carga sus datos"""
        with open(URI, "r") as file:
            content = file.read()
            data = json.loads(content)
            return data

    def createData(self, URI):
        """Crea el archivo vacio para guardar tareas si en la ruta no hay ningun elemento"""
        # Handle absolute and relative paths
        if os.path.dirname(URI):
            # Create directories if path contains directories
            os.makedirs(os.path.dirname(URI), exist_ok=True)
        # Create and write the file
        with open(URI, "w") as file:
            data = {"tasks": {}, "items":0}
            json.dump(data, file)
        return data

    def saveData(self):
        """Guarda su contenido de .data en la ruta de self.URI"""
        with open(self.URI, "w") as file:
            json.dump(self.data, file, indent= 4)
        return

    def add(self, task_description:str):
        """Aniade una tarea a la base de datos"""
        task = Task(task_description)
        id = self.getLastId()
        self.data["tasks"][str(id)] = task.to_dict()
        self.data["items"] += 1
        self.saveData()
        pass

    def getItem(self, index:int)-> dict:
        """Devuelve un diccionario del objeto solicitado con ese indice """
        if self.exists(index):
            return {"id":index, **self.data["tasks"][str(index)]}

    def getLastId(self)-> int:
        """Devuelve el valor del ultimo Id de sus tareas"""
        return self.data["items"]
    
    def getItems(self) -> dict:
        """Devuelve el listado de objetos almacenados """
        tasks = {}
        for key, value in self.data["tasks"].items():
            task_copy = value.copy()
            task_copy["id"] = key
            tasks[key] = task_copy
        return tasks
    
    def filter(self, filter:str) -> dict:
        """Devuelve un listado de objetos almacenados que cumplen con el filtro"""
        tasks = {}
        if filter.isnumeric():
            raise TypeError(f"El status '{filter}' no es valido")
        for key, value in self.data["tasks"].items():
            if value["status"] == filter:
                task_copy = value.copy()
                task_copy["id"] = key
                tasks[key] = task_copy
        return tasks
    
    def getLast(self, limit)-> dict:
        """Devuelve los últimos 'limit' elementos de la base de datos con sus claves como 'id'."""
        items = self.getItems()
        items = dict(list(items.items())[-limit:])
        return items
    
    def removeItem(self, index:int):
        """Se elimina el objeto en el indice de la Clase y de su persistencia"""
        self.exists(index)
        tasks = self.data["tasks"]
        del tasks[str(index)]
        self.saveData()
        return

    def update(self, index:int, field:str, value:str):
        """Se convierte el indice del diccionario a Objeto, se modifica, y se guarda su modificado"""
        if (self.exists(index)):
            requestedTask = self.getItem(index)
            updatedTask = Task.fromDict(requestedTask)
            try:
                updatedTask.update(field, value)
                self.saveTask(index, updatedTask)
                self.saveData()
            except (UnknownStatusException, UnknownFieldException, TypeError) :
                raise ModificationError
        raise UnknownIndexException

    def updateFromObject(self, index:int, task:Task ):
        if (self.exists(index)):
            requestedTask = self.getItem(index)
            updatedTask = Task.fromDict(requestedTask)
            updatedTask.patch(task)
            self.saveTask(index, updatedTask)
            self.saveData()


    def saveTask(self, index:int, task:Task):
        self.data["tasks"][str(index)] = task.to_dict()


    def exists(self, index:int)->bool:
        if (str(index) in self.data["tasks"]):
            return True
        raise UnknownIndexException(f"El indice {index} no pudo encontrarse")
   
