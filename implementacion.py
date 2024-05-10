import time
import random
from collections import deque
from abc import ABC, abstractmethod
from datetime import datetime, timedelta


# Singleton
class SistemaIoT:
    _instance = None

    @classmethod
    def obtener_instancia(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if SistemaIoT._instance is not None:
            raise Exception("Esta clase es un singleton")
        self.datos_temporales = deque(maxlen=12)  # Datos de los últimos 60 segundos (12*5)
        self.cadena_manejo = CalculoEstadisticas(MediaDesviacionStrategy())

    def procesar_dato(self, dato):
        self.datos_temporales.append(dato)
        self.cadena_manejo.manejar_dato(list(self.datos_temporales))

# Observer
class Sensor:
    def __init__(self):
        self._observadores = []

    def registrar_observador(self, observador):
        self._observadores.append(observador)

    def notificar_observadores(self, dato):
        for observador in self._observadores:
            observador.procesar_dato(dato)

    def recibir_dato(self, dato):
        self.notificar_observadores(dato)

# Estrategias para cálculo de estadísticas
class Estrategia(ABC):
    @abstractmethod
    def ejecutar(self, datos):
        pass

class MediaDesviacionStrategy(Estrategia):
    def ejecutar(self, datos):
        if len(datos)%12 == 0.00000000:
            media = sum(d[1] for d in datos) / len(datos)
            desviacion = (sum((x[1] - media) ** 2 for x in datos) / len(datos)) ** 0.5
            print(f'Media: {media}, Desviación: {desviacion}')

class CuantilesStrategy(Estrategia):
    def ejecutar(self, datos):
        datos = sorted([d[1] for d in datos])
        q1 = datos[len(datos) // 4]
        q3 = datos[len(datos) * 3 // 4]
        print(f'Cuantil 25%: {q1}, Cuantil 75%: {q3}')

class MinMaxStrategy(Estrategia):
    def ejecutar(self, datos):
        minimo = min(datos, key=lambda x: x[1])[1]
        maximo = max(datos, key=lambda x: x[1])[1]
        print(f'Mínimo: {minimo}, Máximo: {maximo}')

# Chain of Responsibility
class Manejador:
    def __init__(self, sucesor=None):
        self.sucesor = sucesor

    def manejar_dato(self, datos):
        if self.sucesor:
            self.sucesor.manejar_dato(datos)

class CalculoEstadisticas(Manejador):
    def __init__(self, estrategia):
        super().__init__(Umbral(25))
        self.estrategia = estrategia

    def manejar_dato(self, datos):
        self.estrategia.ejecutar(datos)
        super().manejar_dato(datos)

class Umbral(Manejador):
    def __init__(self, umbral):
        super().__init__(Aumento(10))
        self.umbral = umbral

    def manejar_dato(self, datos):
        ultimo_dato = datos[-1][1] if datos else None
        if ultimo_dato and ultimo_dato > self.umbral:
            print(f"Temperatura {ultimo_dato} por encima del umbral {self.umbral}.")
        super().manejar_dato(datos)

class Aumento(Manejador):
    def __init__(self, incremento_maximo):
        super().__init__()
        self.incremento_maximo = incremento_maximo

    def manejar_dato(self, datos):
        cortar = True   
        if len(datos) >= 6 and cortar == True:
            for i in range(len(datos)-5,len(datos)-1):
                if cortar == True:
                    temperatura_inicial = datos[i-1][1]
                    temperatura_final = datos[-1][1]
                    if temperatura_final - temperatura_inicial > self.incremento_maximo:
                        print("Aumento significativo en la temperatura detectado.")
                        cortar = False
        super().manejar_dato(datos)
import time

# Definir las clases y funciones aquí...

def main():
    sistema = SistemaIoT.obtener_instancia()
    sensor = Sensor()

    # Registramos el sistema IoT como observador del sensor
    sensor.registrar_observador(sistema)

    # Simulamos la recepción de datos de temperatura cada 5 segundos durante 2 minutos
    tiempo_inicial = time.time()
    ultimo_dato = 20  # Temperatura inicial

    while time.time() - tiempo_inicial < 120:  # Simular durante 2 minutos
        time.sleep(5) #para que empiece 
        # Generamos un cambio de temperatura entre -2 y +6 grados
        cambio = random.uniform(-2, 6)
        nuevo_dato = ultimo_dato + cambio
        dato = (time.time(), nuevo_dato)
        print(f"Enviando nuevo dato de temperatura: {round(nuevo_dato,2)} grados.")
        print("---------------------------------------------------------------")
        sensor.recibir_dato(dato)
        ultimo_dato = nuevo_dato
        

if __name__ == "__main__":
    main()
