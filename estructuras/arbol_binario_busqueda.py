class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.izquierda = None
        self.derecha = None

class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None

    def esta_vacio(self):
        return self.raiz is None

    def agregar(self, dato):
        if self.esta_vacio():
            self.raiz = Nodo(dato)
        else:
            self._agregar_recursivo(self.raiz, dato)

    def _agregar_recursivo(self, nodo, dato):
        if dato.get_id() < nodo.dato.get_id():
            if nodo.izquierda is None:
                nodo.izquierda = Nodo(dato)
            else:
                self._agregar_recursivo(nodo.izquierda, dato)
        else:
            if nodo.derecha is None:
                nodo.derecha = Nodo(dato)
            else:
                self._agregar_recursivo(nodo.derecha, dato)

    def buscar(self, id_buscar):
        return self._buscar_recursivo(self.raiz, id_buscar)

    def _buscar_recursivo(self, nodo, id_buscar):
        if nodo is None or nodo.dato.get_id() == id_buscar:
            if nodo is not None:
                return nodo.dato
            else:
                return None
        if id_buscar < nodo.dato.get_id():
            return self._buscar_recursivo(nodo.izquierda, id_buscar)
        else:
            return self._buscar_recursivo(nodo.derecha, id_buscar)

    def eliminar(self, id_eliminar):
        self.raiz = self._eliminar_recursivo(self.raiz, id_eliminar)

    def _eliminar_recursivo(self, nodo, id_eliminar):
        if nodo is None:
            return nodo

        if id_eliminar < nodo.dato.get_id():
            nodo.izquierda = self._eliminar_recursivo(nodo.izquierda, id_eliminar)
        elif id_eliminar > nodo.dato.get_id():
            nodo.derecha = self._eliminar_recursivo(nodo.derecha, id_eliminar)
        else:
            if nodo.izquierda is None:
                return nodo.derecha
            elif nodo.derecha is None:
                return nodo.izquierda

            nodo.dato = self._encontrar_minimo(nodo.derecha).dato
            nodo.derecha = self._eliminar_recursivo(nodo.derecha, nodo.dato.get_id())

        return nodo

    def _encontrar_minimo(self, nodo):
        while nodo.izquierda is not None:
            nodo = nodo.izquierda
        return nodo