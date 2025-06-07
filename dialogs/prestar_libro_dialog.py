from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QMessageBox
)


class PrestarLibroDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Prestar Libro")
        self.libros = parent.libros
        self.usuarios = parent.usuarios
        self.libro_seleccionado = None
        self.usuario_seleccionado = None
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()

        # Selector de libro
        layout.addWidget(QLabel("Seleccionar Libro:"))
        self.combo_libros = QComboBox()
        self.actualizar_combo_libros()
        layout.addWidget(self.combo_libros)

        # Selector de usuario
        layout.addWidget(QLabel("Seleccionar Usuario:"))
        self.combo_usuarios = QComboBox()
        self.actualizar_combo_usuarios()
        layout.addWidget(self.combo_usuarios)

        # Botón de préstamo
        btn_prestar = QPushButton("Realizar Préstamo")
        btn_prestar.clicked.connect(self.validar_prestamo)
        layout.addWidget(btn_prestar)

        self.setLayout(layout)

    def actualizar_combo_libros(self):
        self.combo_libros.clear()
        self._recorrer_arbol_libros(self.libros.raiz)

    def _recorrer_arbol_libros(self, nodo):
        if nodo is not None:
            self._recorrer_arbol_libros(nodo.izquierda)
            libro = nodo.dato
            if libro.cantidad_disponible > 0:
                self.combo_libros.addItem(f"{libro.titulo} - {libro.autor}", libro)
            self._recorrer_arbol_libros(nodo.derecha)

    def actualizar_combo_usuarios(self):
        self.combo_usuarios.clear()
        self._recorrer_arbol_usuarios(self.usuarios.raiz)

    def _recorrer_arbol_usuarios(self, nodo):
        if nodo is not None:
            self._recorrer_arbol_usuarios(nodo.izquierda)
            usuario = nodo.dato
            self.combo_usuarios.addItem(f"{usuario.nombre} ({usuario.id_usuario})", usuario)
            self._recorrer_arbol_usuarios(nodo.derecha)

    def validar_prestamo(self):
        if self.combo_libros.count() == 0:
            QMessageBox.warning(self, "Error", "No hay libros disponibles")
            return
        if self.combo_usuarios.count() == 0:
            QMessageBox.warning(self, "Error", "No hay usuarios registrados")
            return

        self.libro_seleccionado = self.combo_libros.currentData()
        self.usuario_seleccionado = self.combo_usuarios.currentData()

        if self.libro_seleccionado is None or self.usuario_seleccionado is None:
            QMessageBox.warning(self, "Error", "Por favor seleccione un libro y un usuario")
            return

        if self.libro_seleccionado.cantidad_disponible <= 0:
            QMessageBox.warning(self, "Error", "No hay ejemplares disponibles de este libro")
            return

        self.accept()

    def obtener_prestamo(self):
        """Retorna el usuario y libro seleccionados para el préstamo."""
        return self.usuario_seleccionado, self.libro_seleccionado 