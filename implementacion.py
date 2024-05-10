
from abc import ABC, abstractmethod



# R1
class SistemaIoT:
    _instancia = None
    
    def __init__(self, manager_chain):
            self.manager_chain = manager_chain                                  # Variable que habra que indicar al inicializar el sistema para indicar el manejador que empiza el chain responsability
            self.date_temp = []                                                 # Variable para almacenar cada tupla (timestamp, t) nueva
            self.date = []                                                      # Variable para almacenar cada timestamp de date_temp
            self.temp = []   

    @classmethod

    def obtener_instancia(cls):
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia
    


class Manejador(ABC):
    @abstractmethod
    def manejar_nueva_temperatura(self, marca_temporal, temperatura):
        pass

    def umbral(self, temperatura):
        if temperatura > 35:
            return True
        else:
            return False
        
class observable:
    