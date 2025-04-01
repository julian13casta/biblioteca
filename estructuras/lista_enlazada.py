class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
        self.longitud = 0
        
    def esta_vacia(self):
        return self.cabeza is None
        
    def agregar(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.esta_vacia():
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        self.longitud += 1
        
    def buscar(self, criterio):
        actual = self.cabeza
        while actual:
            if criterio(actual.dato):
                return actual.dato
            actual = actual.siguiente
        return None 

    def eliminar(self, dato):
        if self.esta_vacia():
            return False
        
        if self.cabeza.dato == dato:
            self.cabeza = self.cabeza.siguiente
            self.longitud -= 1
            return True
        
        actual = self.cabeza
        while actual.siguiente:
            if actual.siguiente.dato == dato:
                actual.siguiente = actual.siguiente.siguiente
                self.longitud -= 1
                return True
            actual = actual.siguiente
        return False 