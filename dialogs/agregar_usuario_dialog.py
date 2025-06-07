from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from models.usuario import Usuario

class AgregarUsuarioDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Nuevo Usuario")
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Campos de entrada
        self.nombre_input = QLineEdit()
        self.id_input = QLineEdit()
        self.email_input = QLineEdit()
        
        # Etiquetas y campos
        layout.addWidget(QLabel("Nombre:"))
        layout.addWidget(self.nombre_input)
        layout.addWidget(QLabel("ID:"))
        layout.addWidget(self.id_input)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)
        
        # Botón de guardar
        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(self.accept)
        layout.addWidget(btn_guardar)
        
        self.setLayout(layout)

    def obtener_usuario(self) -> Usuario:
        """Retorna un nuevo objeto Usuario con los datos ingresados."""
        return Usuario(
            nombre=self.nombre_input.text(),
            id_usuario=self.id_input.text(),
            email=self.email_input.text()
        ) 