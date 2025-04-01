from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

class EditarLibroDialog(QDialog):
    def __init__(self, libro, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Libro")
        self.libro = libro
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Campos de entrada
        self.titulo_input = QLineEdit(self.libro.titulo)
        self.autor_input = QLineEdit(self.libro.autor)
        self.isbn_input = QLineEdit(self.libro.isbn)
        self.cantidad_input = QLineEdit(str(self.libro.cantidad_disponible))
        
        # Etiquetas y campos
        layout.addWidget(QLabel("Título:"))
        layout.addWidget(self.titulo_input)
        layout.addWidget(QLabel("Autor:"))
        layout.addWidget(self.autor_input)
        layout.addWidget(QLabel("ISBN:"))
        layout.addWidget(self.isbn_input)
        layout.addWidget(QLabel("Cantidad:"))
        layout.addWidget(self.cantidad_input)
        
        # Botones
        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(self.accept)
        layout.addWidget(btn_guardar)
        
        self.setLayout(layout) 