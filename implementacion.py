import time
import random
from collections import deque
from abc import ABC, abstractmethod
from datetime import datetime, timedelta


# Singleton
class SistemaIoT:
    _instance = None

    @classmethod
    def obtener_instancia(cls, estrategia=None):
        if cls._instance is None:
            if estrategia is None:
                raise Exception("No se ha seleccionado una estrategia")
            cls._instance = cls(estrategia)
        return cls._instance

    def __init__(self, estrategia):
        self.estrategia = estrategia
        self.datos_temporales = deque(maxlen=12)  # Datos de los últimos 60 segundos (12*5) cola de maximo 12 elementos
        self.tiempo_inicial = time.time()
        self.manejador = CalculoEstadisticas(self.estrategia)

    def procesar_dato(self, dato,tiempo_inicial):
        self.datos_temporales.append(dato)
        self.manejador.manejar_dato(list(self.datos_temporales), tiempo_inicial)

# Observer
class Sensor:
    def __init__(self):
        self._observadores = []

    def registrar_observador(self, observador):
        self._observadores.append(observador)

    def notificar_observadores(self, dato, tiempo_inicial):
        for observador in self._observadores:
            observador.procesar_dato(dato, tiempo_inicial)

    def recibir_dato(self, dato, tiempo_inicial):
        self.notificar_observadores(dato, tiempo_inicial)

# Estrategias para cálculo de estadísticas
class Estrategia(ABC):
    @abstractmethod
    def ejecutar(self, datos):
        pass

class MediaDesviacionStrategy(Estrategia):
        
    def ejecutar(self, datos):
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

    def manejar_dato(self, datos, tiempo_inicial):
        if self.sucesor:
            self.sucesor.manejar_dato(datos, tiempo_inicial)

class CalculoEstadisticas(Manejador):
    def __init__(self, estrategia):
        super().__init__(Umbral(25))
        self.estrategia = estrategia
 
    def manejar_dato(self, datos,tiempo_inicial):
        if (time.time() - tiempo_inicial) %60 < 0.3: # no podmos poner ==0 porque nunca seran 60 segundos exactos
            
            self.estrategia.ejecutar(datos)
        super().manejar_dato(datos, tiempo_inicial)

class Umbral(Manejador):
    def __init__(self, umbral):
        super().__init__(Aumento(10))
        self.umbral = umbral

    def manejar_dato(self, datos, tiempo_inicial):
        ultimo_dato = datos[-1][1] if datos else None
        if ultimo_dato and ultimo_dato > self.umbral:
            print(f"-La temperatura ha superado el umbral de {self.umbral} Cº.")
        super().manejar_dato(datos, tiempo_inicial)

class Aumento(Manejador):
    def __init__(self, incremento_maximo):
        super().__init__()
        self.incremento_maximo = incremento_maximo

    def manejar_dato(self, datos, tiempo_inicial):
        if len(datos) > 1:  # Asegurarse de que haya al menos dos datos para comparar
            temperatura_final = datos[-1][1]
            # Encuentra la temperatura más baja en el rango considerado
            temperatura_minima = min(dato[1] for dato in datos[max(0, len(datos) - 6):len(datos) - 1])
            # Verificar si la temperatura final es al menos incremento_maximo unidades mayor que la temperatura mínima
            if temperatura_final - temperatura_minima > self.incremento_maximo:
                print("-Aumento de +10°C en los últimos 30 segundos")
        super().manejar_dato(datos, tiempo_inicial)

import time

# Definir las clases y funciones aquí...

def main():
    n = int(input("que estrategia quieres usar:"))
    if n ==1:
        estrategia = MediaDesviacionStrategy()
    elif n==2:
        estrategia = CuantilesStrategy()
    else:
        estrategia = MinMaxStrategy()
    sistema = SistemaIoT.obtener_instancia(estrategia)
    sensor = Sensor()

    # Registramos el sistema IoT como observador del sensor
    sensor.registrar_observador(sistema)

    # Simulamos la recepción de datos de temperatura cada 5 segundos durante 2 minutos
    ultimo_dato = 20  # Temperatura inicial
    temperaturas = []
    tiempo_ejecucion = int(input("cuanto tiempo quieres que dure la simulacion: "))
    tiempo_0 = time.time()

    while time.time() - tiempo_0 < tiempo_ejecucion:  # Simular durante 2 minutos
        time.sleep(5) #para que empiece 
        # Generamos un cambio de temperatura entre -2 y +6 grados
        cambio = random.uniform(-2, 6)
        nuevo_dato = ultimo_dato + cambio
        dato = (time.time(), nuevo_dato)
       
        temperaturas.append(nuevo_dato)
        sensor.recibir_dato(dato, tiempo_0)
        print(f"-La temparutra es: {round(nuevo_dato,2)} grados. Han pasado {int(time.time()-tiempo_0)} segundos.")
        print("---------------------------------------------------------------")

        ultimo_dato = nuevo_dato
        
    print   (temperaturas)
if __name__ == "__main__":
    main()
