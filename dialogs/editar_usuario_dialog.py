from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

class EditarUsuarioDialog(QDialog):
    def __init__(self, usuario, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Usuario")
        self.usuario = usuario
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Campos de entrada
        self.nombre_input = QLineEdit(self.usuario.nombre)
        self.id_input = QLineEdit(self.usuario.id_usuario)
        self.email_input = QLineEdit(self.usuario.email)
        
        # Etiquetas y campos
        layout.addWidget(QLabel("Nombre:"))
        layout.addWidget(self.nombre_input)
        layout.addWidget(QLabel("ID:"))
        layout.addWidget(self.id_input)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)
        
        # Botones
        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(self.accept)
        layout.addWidget(btn_guardar)
        
        self.setLayout(layout) 