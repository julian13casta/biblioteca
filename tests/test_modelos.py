import unittest
from models.libro import Libro
from models.usuario import Usuario
from estructuras.lista_enlazada import ListaEnlazada

class TestModelos(unittest.TestCase):
    def setUp(self):
        # Se ejecuta antes de cada prueba
        self.libro = Libro("El Quijote", "Cervantes", "123-456", 5)
        self.usuario = Usuario("Juan Pérez", "U001", "juan@email.com")
        self.lista = ListaEnlazada()

    def test_crear_libro(self):
        """Prueba la creación correcta de un libro"""
        self.assertEqual(self.libro.titulo, "El Quijote")
        self.assertEqual(self.libro.autor, "Cervantes")
        self.assertEqual(self.libro.isbn, "123-456")
        self.assertEqual(self.libro.cantidad_disponible, 5)
        self.assertEqual(len(self.libro.prestamos), 0)

    def test_crear_usuario(self):
        """Prueba la creación correcta de un usuario"""
        self.assertEqual(self.usuario.nombre, "Juan Pérez")
        self.assertEqual(self.usuario.id_usuario, "U001")
        self.assertEqual(self.usuario.email, "juan@email.com")
        self.assertEqual(len(self.usuario.libros_prestados), 0)

    def test_prestamo_libro(self):
        """Prueba el proceso de préstamo de un libro"""
        # Verificar préstamo exitoso
        self.assertTrue(self.usuario.tomar_prestado(self.libro))
        self.assertEqual(self.libro.cantidad_disponible, 4)
        self.assertEqual(len(self.usuario.libros_prestados), 1)
        
        # Verificar que el libro está en la lista de préstamos
        self.assertIn(self.libro, self.usuario.libros_prestados)
        
        # Verificar que el usuario está en la lista de préstamos del libro
        self.assertIn(self.usuario, self.libro.prestamos)

    def test_devolucion_libro(self):
        """Prueba el proceso de devolución de un libro"""
        # Primero prestamos el libro
        self.usuario.tomar_prestado(self.libro)
        
        # Verificar devolución exitosa
        self.assertTrue(self.usuario.devolver_libro(self.libro))
        self.assertEqual(self.libro.cantidad_disponible, 5)
        self.assertEqual(len(self.usuario.libros_prestados), 0)
        
        # Verificar que el libro ya no está en la lista de préstamos
        self.assertNotIn(self.libro, self.usuario.libros_prestados)
        
        # Verificar que el usuario ya no está en la lista de préstamos del libro
        self.assertNotIn(self.usuario, self.libro.prestamos)

    def test_lista_enlazada(self):
        """Prueba las operaciones de la lista enlazada"""
        # Prueba agregar elementos
        self.lista.agregar(self.libro)
        self.lista.agregar(self.usuario)
        self.assertEqual(self.lista.longitud, 2)
        
        # Prueba búsqueda
        libro_encontrado = self.lista.buscar(lambda x: isinstance(x, Libro))
        self.assertEqual(libro_encontrado, self.libro)
        
        # Prueba eliminación
        self.assertTrue(self.lista.eliminar(self.libro))
        self.assertEqual(self.lista.longitud, 1) 