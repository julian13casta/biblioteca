class Libro:
    def __init__(self, titulo, autor, isbn, cantidad_disponible):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.cantidad_disponible = cantidad_disponible
        self.prestamos = []  # Lista para registrar préstamos
        
    def __str__(self):
        return f"{self.titulo} - {self.autor} (ISBN: {self.isbn})"
    
    def get_id(self):
        return self.isbn
        
    def prestar(self, usuario):
        if self.cantidad_disponible > 0:
            self.cantidad_disponible -= 1
            self.prestamos.append(usuario)
            return True
        return False
        
    def devolver(self, usuario):
        if usuario in self.prestamos:
            self.prestamos.remove(usuario)
            self.cantidad_disponible += 1
            return True
        return False 