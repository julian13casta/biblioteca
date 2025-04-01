import unittest
import sys
from tests.test_modelos import TestModelos
from tests.test_integracion import TestIntegracion

def ejecutar_pruebas():
    # Crear el cargador de pruebas
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar las pruebas a la suite
    suite.addTests(loader.loadTestsFromTestCase(TestModelos))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegracion))
    
    # Ejecutar las pruebas
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Retornar código de salida apropiado
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(ejecutar_pruebas()) 