from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

class AgregarLibroDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Nuevo Libro")
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Campos de entrada
        self.titulo_input = QLineEdit()
        self.autor_input = QLineEdit()
        self.isbn_input = QLineEdit()
        self.cantidad_input = QLineEdit()
        
        # Etiquetas y campos
        layout.addWidget(QLabel("Título:"))
        layout.addWidget(self.titulo_input)
        layout.addWidget(QLabel("Autor:"))
        layout.addWidget(self.autor_input)
        layout.addWidget(QLabel("ISBN:"))
        layout.addWidget(self.isbn_input)
        layout.addWidget(QLabel("Cantidad:"))
        layout.addWidget(self.cantidad_input)
        
        # Botón de guardar
        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(self.accept)
        layout.addWidget(btn_guardar)
        
        self.setLayout(layout) 