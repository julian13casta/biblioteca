import unittest
from PyQt5.QtWidgets import QApplication
import sys
from main import BibliotecaGUI
from models.libro import Libro
from models.usuario import Usuario
from estructuras.lista_enlazada import ListaEnlazada

class TestIntegracion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Se ejecuta una vez antes de todas las pruebas
        cls.app = QApplication(sys.argv)
        cls.ventana = BibliotecaGUI()

    def setUp(self):
        # Limpiar datos antes de cada prueba
        self.ventana.libros = ListaEnlazada()
        self.ventana.usuarios = ListaEnlazada()
        self.ventana.actualizar_tabla_libros()
        self.ventana.actualizar_tabla_usuarios()
        self.ventana.actualizar_tabla_prestamos()

    def test_agregar_libro(self):
        """Prueba la funcionalidad de agregar libro"""
        # Simular agregar un libro
        libro = Libro("Test Libro", "Autor Test", "TEST-123", 1)
        self.ventana.libros.agregar(libro)
        self.ventana.actualizar_tabla_libros()
        
        # Verificar que el libro aparece en la tabla
        self.assertEqual(self.ventana.tabla_libros.rowCount(), 1)
        self.assertEqual(
            self.ventana.tabla_libros.item(0, 0).text(),
            "Test Libro"
        )

    def test_agregar_usuario(self):
        """Prueba la funcionalidad de agregar usuario"""
        # Simular agregar un usuario
        usuario = Usuario("Test Usuario", "TEST-001", "test@test.com")
        self.ventana.usuarios.agregar(usuario)
        self.ventana.actualizar_tabla_usuarios()
        
        # Verificar que el usuario aparece en la tabla
        self.assertEqual(self.ventana.tabla_usuarios.rowCount(), 1)
        self.assertEqual(
            self.ventana.tabla_usuarios.item(0, 0).text(),
            "Test Usuario"
        )

    def test_prestamo_completo(self):
        """Prueba el proceso completo de préstamo"""
        # Crear y agregar libro y usuario
        libro = Libro("Test Libro", "Autor Test", "TEST-123", 1)
        usuario = Usuario("Test Usuario", "TEST-001", "test@test.com")
        
        self.ventana.libros.agregar(libro)
        self.ventana.usuarios.agregar(usuario)
        
        # Simular préstamo
        usuario.tomar_prestado(libro)
        
        # Actualizar tablas
        self.ventana.actualizar_tabla_libros()
        self.ventana.actualizar_tabla_prestamos()
        
        # Verificar estado del préstamo
        self.assertEqual(libro.cantidad_disponible, 0)
        self.assertEqual(
            self.ventana.tabla_prestamos.rowCount(),
            1
        )

    def test_validaciones(self):
        """Prueba las validaciones del sistema"""
        libro = Libro("Test Libro", "Autor Test", "TEST-123", 1)
        usuario = Usuario("Test Usuario", "TEST-001", "test@test.com")
        
        # Intentar prestar más libros que los disponibles
        usuario.tomar_prestado(libro)
        self.assertFalse(usuario.tomar_prestado(libro))
        
        # Intentar devolver un libro no prestado
        libro2 = Libro("Otro Libro", "Otro Autor", "TEST-456", 1)
        self.assertFalse(usuario.devolver_libro(libro2)) 