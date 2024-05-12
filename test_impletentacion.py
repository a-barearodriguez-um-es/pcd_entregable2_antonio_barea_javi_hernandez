import time
import random
from unittest.mock import patch
import pytest

from implementacion import *

@pytest.fixture
def mock_time():
    return time.time()

@pytest.fixture
def sistema_iot():
    estrategia = MediaDesviacionStrategy()
    return SistemaIoT.obtener_instancia(estrategia)

@pytest.fixture
def sensor():
    return Sensor()

def test_singleton_instance(sistema_iot):
    # Verificar que solo haya una instancia de SistemaIoT
    otra_instancia = SistemaIoT.obtener_instancia()
    assert sistema_iot is otra_instancia

def test_observer_register(sensor, sistema_iot):
    # Verificar que el sistema IoT se registra correctamente como observador del sensor
    sensor.registrar_observador(sistema_iot)
    assert sistema_iot in sensor._observadores

def test_media_desviacion_strategy():
    # Prueba para la estrategia de cálculo de media y desviación estándar
    strategy = MediaDesviacionStrategy()
    datos = [(1, 20), (2, 25), (3, 30)]
    with patch('builtins.print') as mock_print:
        strategy.ejecutar(datos)
        
        mock_print.assert_called_with('Media: 25.0, Desviación: 4.08')

def test_cuantiles_strategy():
    # Prueba para la estrategia de cálculo de cuantiles
    strategy = CuantilesStrategy()
    datos = [(0,0),(1, 10), (2, 20), (3, 30), (4, 40), (5, 50), (6, 60), (7, 70), (8, 80), (9, 90), (10, 100)]
    with patch('builtins.print') as mock_print:
        strategy.ejecutar(datos)
        mock_print.assert_called_with('Cuantil 25%: 25.0, Cuantil 75%: 75.0')

def test_min_max_strategy():
    # Prueba para la estrategia de cálculo de mínimo y máximo
    strategy = MinMaxStrategy()
    datos = [(1, 20), (2, 25), (3, 30), (4, 35)]
    with patch('builtins.print') as mock_print:
        strategy.ejecutar(datos)
        mock_print.assert_called_with('Mínimo: 20, Máximo: 35')





def test_aumento_datos_vacios():
    handler = Aumento(5)
    datos = []
    handler.manejar_dato(datos, 0)  # El tiempo inicial puede ser cualquier valor aquí



def test_manejador_sin_sucesor():
    handler = Manejador()
    handler.manejar_dato([1, 2, 3], 0)  # Datos y tiempo inicial ficticios



def test_umbral_mayor_que_datos():
    handler = Umbral(100)
    datos = [(1, 20), (2, 25), (3, 30)]
    handler.manejar_dato(datos, 0)  # Tiempo inicial ficticio



