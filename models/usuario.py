class Usuario:
    def __init__(self, nombre, id_usuario, email):
        self.nombre = nombre
        self.id_usuario = id_usuario
        self.email = email
        self.libros_prestados = []  # Lista para almacenar los préstamos activos
        
    def __str__(self):
        return f"{self.nombre} (ID: {self.id_usuario})"
        
    def tomar_prestado(self, libro):
        if libro.prestar(self):
            self.libros_prestados.append(libro)
            return True
        return False
        
    def devolver_libro(self, libro):
        if libro in self.libros_prestados:
            if libro.devolver(self):
                self.libros_prestados.remove(libro)
                return True
        return False 