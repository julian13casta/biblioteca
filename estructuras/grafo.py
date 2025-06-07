from typing import Dict, List, Set, Optional
from models.libro import Libro
from models.usuario import Usuario

class NodoGrafo:
    def __init__(self, id: str, tipo: str, datos: object):
        self.id = id
        self.tipo = tipo  # 'libro' o 'usuario'
        self.datos = datos
        self.vecinos: Dict[str, float] = {}  # id -> peso

class Grafo:
    def __init__(self):
        self.nodos: Dict[str, NodoGrafo] = {}
        
    def agregar_nodo(self, id: str, tipo: str, datos: object) -> None:
        """Agrega un nuevo nodo al grafo."""
        if id not in self.nodos:
            self.nodos[id] = NodoGrafo(id, tipo, datos)
            
    def agregar_arista(self, id_origen: str, id_destino: str, peso: float = 1.0) -> None:
        """Agrega una arista entre dos nodos."""
        if id_origen in self.nodos and id_destino in self.nodos:
            self.nodos[id_origen].vecinos[id_destino] = peso
            self.nodos[id_destino].vecinos[id_origen] = peso
            
    def eliminar_arista(self, id_origen: str, id_destino: str) -> None:
        """Elimina una arista entre dos nodos."""
        if id_origen in self.nodos and id_destino in self.nodos:
            if id_destino in self.nodos[id_origen].vecinos:
                del self.nodos[id_origen].vecinos[id_destino]
            if id_origen in self.nodos[id_destino].vecinos:
                del self.nodos[id_destino].vecinos[id_origen]
                
    def obtener_vecinos(self, id: str) -> Dict[str, float]:
        """Retorna los vecinos de un nodo con sus pesos."""
        if id in self.nodos:
            return self.nodos[id].vecinos
        return {}
    
    def obtener_nodo(self, id: str) -> Optional[NodoGrafo]:
        """Retorna un nodo por su ID."""
        return self.nodos.get(id)
    
    def obtener_libros_relacionados(self, isbn: str, max_libros: int = 5) -> List[Libro]:
        """Retorna libros relacionados basados en préstamos comunes."""
        if isbn not in self.nodos:
            return []
            
        # Obtener usuarios que han prestado este libro
        usuarios_prestadores = set()
        for vecino_id, peso in self.nodos[isbn].vecinos.items():
            if self.nodos[vecino_id].tipo == 'usuario':
                usuarios_prestadores.add(vecino_id)
                
        # Contar libros relacionados
        libros_relacionados: Dict[str, int] = {}
        for usuario_id in usuarios_prestadores:
            for vecino_id, peso in self.nodos[usuario_id].vecinos.items():
                if self.nodos[vecino_id].tipo == 'libro' and vecino_id != isbn:
                    libros_relacionados[vecino_id] = libros_relacionados.get(vecino_id, 0) + 1
                    
        # Ordenar por frecuencia y retornar los más relevantes
        libros_ordenados = sorted(libros_relacionados.items(), key=lambda x: x[1], reverse=True)
        return [self.nodos[libro_id].datos for libro_id, _ in libros_ordenados[:max_libros]]
    
    def obtener_recomendaciones_usuario(self, id_usuario: str, max_libros: int = 5) -> List[Libro]:
        """Retorna recomendaciones de libros para un usuario basadas en sus préstamos."""
        if id_usuario not in self.nodos:
            return []
            
        # Obtener libros que el usuario ha prestado
        libros_prestados = set()
        for vecino_id, peso in self.nodos[id_usuario].vecinos.items():
            if self.nodos[vecino_id].tipo == 'libro':
                libros_prestados.add(vecino_id)
                
        # Contar libros relacionados
        libros_recomendados: Dict[str, int] = {}
        for libro_id in libros_prestados:
            for vecino_id, peso in self.nodos[libro_id].vecinos.items():
                if self.nodos[vecino_id].tipo == 'usuario':
                    for libro_vecino_id, peso_vecino in self.nodos[vecino_id].vecinos.items():
                        if (self.nodos[libro_vecino_id].tipo == 'libro' and 
                            libro_vecino_id not in libros_prestados):
                            libros_recomendados[libro_vecino_id] = libros_recomendados.get(libro_vecino_id, 0) + 1
                            
        # Ordenar por frecuencia y retornar las mejores recomendaciones
        libros_ordenados = sorted(libros_recomendados.items(), key=lambda x: x[1], reverse=True)
        return [self.nodos[libro_id].datos for libro_id, _ in libros_ordenados[:max_libros]] 