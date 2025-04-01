from PyQt5.QtWidgets import (
    QDialog, 
    QVBoxLayout, 
    QLabel, 
    QComboBox, 
    QPushButton,
    QMessageBox
)

class PrestarLibroDialog(QDialog):
    def __init__(self, libros, usuarios, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Prestar Libro")
        self.libros = libros
        self.usuarios = usuarios
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
        actual = self.libros.cabeza
        while actual:
            libro = actual.dato
            if libro.cantidad_disponible > 0:
                self.combo_libros.addItem(str(libro), libro)
            actual = actual.siguiente
    
    def actualizar_combo_usuarios(self):
        self.combo_usuarios.clear()
        actual = self.usuarios.cabeza
        while actual:
            usuario = actual.dato
            self.combo_usuarios.addItem(str(usuario), usuario)
            actual = actual.siguiente
            
    def validar_prestamo(self):
        if self.combo_libros.count() == 0:
            QMessageBox.warning(self, "Error", "No hay libros disponibles")
            return
        if self.combo_usuarios.count() == 0:
            QMessageBox.warning(self, "Error", "No hay usuarios registrados")
            return
            
        self.libro_seleccionado = self.combo_libros.currentData()
        self.usuario_seleccionado = self.combo_usuarios.currentData()
        self.accept() 