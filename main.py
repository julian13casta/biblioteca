import sys
from PyQt5.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget, 
    QVBoxLayout,
    QHBoxLayout, 
    QPushButton, 
    QLabel, 
    QLineEdit, 
    QMessageBox,
    QDialog,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMenu,
    QAction
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont
from models.libro import Libro
from models.usuario import Usuario
from estructuras.lista_enlazada import ListaEnlazada
from dialogs.agregar_libro_dialog import AgregarLibroDialog
from dialogs.agregar_usuario_dialog import AgregarUsuarioDialog
from dialogs.prestar_libro_dialog import PrestarLibroDialog
from dialogs.editar_libro_dialog import EditarLibroDialog
from dialogs.editar_usuario_dialog import EditarUsuarioDialog

class BibliotecaGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión de Biblioteca")
        self.setGeometry(100, 100, 1200, 800)
        
        # Configurar estilo y colores
        self.configurar_estilo()
        
        # Inicializar estructuras de datos
        self.libros = ListaEnlazada()
        self.usuarios = ListaEnlazada()
        
        # Configurar la interfaz
        self.configurar_ui()
        
    def configurar_estilo(self):
        # Establecer la paleta de colores
        paleta = QPalette()
        paleta.setColor(QPalette.Window, QColor(240, 240, 245))  # Fondo principal
        paleta.setColor(QPalette.WindowText, QColor(50, 50, 50))  # Texto
        paleta.setColor(QPalette.Button, QColor(70, 130, 180))   # Botones
        paleta.setColor(QPalette.ButtonText, QColor(255, 255, 255))  # Texto de botones
        self.setPalette(paleta)
        
        # Establecer estilo global
        self.setStyleSheet("""
            QPushButton {
                background-color: #4682B4;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                font-size: 14px;
                margin: 2px;
            }
            QPushButton:hover {
                background-color: #5793C5;
            }
            /* Estilo específico para botones en tablas */
            QTableWidget QPushButton {
                min-height: 30px;
                max-height: 30px;
                padding: 5px;
            }
            QLabel {
                font-size: 14px;
                color: #333;
                margin: 5px;
            }
            QTableWidget {
                background-color: white;
                alternate-background-color: #F5F5F5;
                border: 1px solid #DDD;
                border-radius: 4px;
                padding: 2px;
            }
            QTableWidget::item {
                padding: 5px;
                min-height: 40px;  /* Altura mínima para las celdas */
            }
            QHeaderView::section {
                background-color: #4682B4;
                color: white;
                padding: 5px;
                border: 1px solid #3571A3;
                height: 35px;  /* Altura para el encabezado */
            }
        """)
        
    def configurar_ui(self):
        # Widget central
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        
        # Layout principal
        layout = QHBoxLayout()
        
        # Panel izquierdo para botones
        panel_botones = QVBoxLayout()
        
        # Título principal
        titulo = QLabel("Sistema de Gestión de Biblioteca")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        titulo.setStyleSheet("color: #2C3E50; margin: 10px;")
        panel_botones.addWidget(titulo)
        
        # Sección de Libros
        panel_botones.addWidget(QLabel("\nGestión de Libros"))
        btn_agregar_libro = QPushButton("➕ Agregar Libro")
        btn_agregar_libro.clicked.connect(self.mostrar_agregar_libro)
        panel_botones.addWidget(btn_agregar_libro)
        
        # Sección de Usuarios
        panel_botones.addWidget(QLabel("\nGestión de Usuarios"))
        btn_agregar_usuario = QPushButton("➕ Agregar Usuario")
        btn_agregar_usuario.clicked.connect(self.mostrar_agregar_usuario)
        panel_botones.addWidget(btn_agregar_usuario)
        
        # Sección de Préstamos
        panel_botones.addWidget(QLabel("\nGestión de Préstamos"))
        btn_prestar_libro = QPushButton("📚 Prestar Libro")
        btn_prestar_libro.clicked.connect(self.mostrar_prestar_libro)
        panel_botones.addWidget(btn_prestar_libro)
        
        panel_botones.addStretch()
        
        # Panel derecho para tablas
        panel_tablas = QVBoxLayout()
        
        # Tabla de Libros con botones de acción
        panel_libros = QVBoxLayout()
        panel_libros.addWidget(QLabel("Libros:"))
        
        self.tabla_libros = QTableWidget()
        self.tabla_libros.setColumnCount(6)
        self.tabla_libros.setHorizontalHeaderLabels(['Título', 'Autor', 'ISBN', 'Disponibles', 'Editar', 'Eliminar'])
        self.tabla_libros.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tabla_libros.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tabla_libros.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.tabla_libros.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.tabla_libros.horizontalHeader().setSectionResizeMode(4, QHeaderView.Fixed)
        self.tabla_libros.horizontalHeader().setSectionResizeMode(5, QHeaderView.Fixed)
        self.tabla_libros.setColumnWidth(4, 100)
        self.tabla_libros.setColumnWidth(5, 100)
        panel_libros.addWidget(self.tabla_libros)
        
        # Tabla de Usuarios con botones de acción
        panel_usuarios = QVBoxLayout()
        panel_usuarios.addWidget(QLabel("Usuarios:"))
        
        self.tabla_usuarios = QTableWidget()
        self.tabla_usuarios.setColumnCount(5)
        self.tabla_usuarios.setHorizontalHeaderLabels(['Nombre', 'ID', 'Email', 'Editar', 'Eliminar'])
        self.tabla_usuarios.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tabla_usuarios.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tabla_usuarios.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.tabla_usuarios.horizontalHeader().setSectionResizeMode(3, QHeaderView.Fixed)
        self.tabla_usuarios.horizontalHeader().setSectionResizeMode(4, QHeaderView.Fixed)
        self.tabla_usuarios.setColumnWidth(3, 100)
        self.tabla_usuarios.setColumnWidth(4, 100)
        panel_usuarios.addWidget(self.tabla_usuarios)
        
        # Tabla de Préstamos con botón de devolución
        panel_prestamos = QVBoxLayout()
        panel_prestamos.addWidget(QLabel("Préstamos Activos:"))
        
        self.tabla_prestamos = QTableWidget()
        self.tabla_prestamos.setColumnCount(4)
        self.tabla_prestamos.setHorizontalHeaderLabels(['Usuario', 'Libro', 'ISBN', 'Devolver'])
        self.tabla_prestamos.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tabla_prestamos.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tabla_prestamos.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.tabla_prestamos.horizontalHeader().setSectionResizeMode(3, QHeaderView.Fixed)
        self.tabla_prestamos.setColumnWidth(3, 100)
        panel_prestamos.addWidget(self.tabla_prestamos)
        
        # Agregar todos los paneles al panel de tablas
        panel_tablas.addLayout(panel_libros)
        panel_tablas.addLayout(panel_usuarios)
        panel_tablas.addLayout(panel_prestamos)
        
        # Agregar paneles al layout principal
        layout.addLayout(panel_botones, 1)
        layout.addLayout(panel_tablas, 3)
        
        widget_central.setLayout(layout)
        
        # Configuración adicional para la tabla de libros
        self.tabla_libros.verticalHeader().setDefaultSectionSize(50)  # Altura de las filas
        
        # Configuración adicional para la tabla de usuarios
        self.tabla_usuarios.verticalHeader().setDefaultSectionSize(50)  # Altura de las filas
        
        # Configuración adicional para la tabla de préstamos
        self.tabla_prestamos.verticalHeader().setDefaultSectionSize(50)  # Altura de las filas
        
    def actualizar_tabla_libros(self):
        self.tabla_libros.setRowCount(0)
        actual = self.libros.cabeza
        row = 0
        while actual:
            libro = actual.dato
            self.tabla_libros.insertRow(row)
            self.tabla_libros.setRowHeight(row, 50)  # Establecer altura de la fila
            self.tabla_libros.setItem(row, 0, QTableWidgetItem(libro.titulo))
            self.tabla_libros.setItem(row, 1, QTableWidgetItem(libro.autor))
            self.tabla_libros.setItem(row, 2, QTableWidgetItem(libro.isbn))
            self.tabla_libros.setItem(row, 3, QTableWidgetItem(str(libro.cantidad_disponible)))
            
            # Botón Editar
            btn_editar = QPushButton("✏️ Editar")
            btn_editar.clicked.connect(lambda checked, l=libro: self.editar_libro(l))
            self.tabla_libros.setCellWidget(row, 4, btn_editar)
            
            # Botón Eliminar
            btn_eliminar = QPushButton("❌ Eliminar")
            btn_eliminar.clicked.connect(lambda checked, l=libro: self.eliminar_libro(l))
            self.tabla_libros.setCellWidget(row, 5, btn_eliminar)
            
            row += 1
            actual = actual.siguiente
            
    def actualizar_tabla_usuarios(self):
        self.tabla_usuarios.setRowCount(0)
        actual = self.usuarios.cabeza
        row = 0
        while actual:
            usuario = actual.dato
            self.tabla_usuarios.insertRow(row)
            self.tabla_usuarios.setRowHeight(row, 50)  # Establecer altura de la fila
            self.tabla_usuarios.setItem(row, 0, QTableWidgetItem(usuario.nombre))
            self.tabla_usuarios.setItem(row, 1, QTableWidgetItem(usuario.id_usuario))
            self.tabla_usuarios.setItem(row, 2, QTableWidgetItem(usuario.email))
            
            # Botón Editar
            btn_editar = QPushButton("✏️ Editar")
            btn_editar.clicked.connect(lambda checked, u=usuario: self.editar_usuario(u))
            self.tabla_usuarios.setCellWidget(row, 3, btn_editar)
            
            # Botón Eliminar
            btn_eliminar = QPushButton("❌ Eliminar")
            btn_eliminar.clicked.connect(lambda checked, u=usuario: self.eliminar_usuario(u))
            self.tabla_usuarios.setCellWidget(row, 4, btn_eliminar)
            
            row += 1
            actual = actual.siguiente
            
    def actualizar_tabla_prestamos(self):
        self.tabla_prestamos.setRowCount(0)
        row = 0
        actual_usuario = self.usuarios.cabeza
        while actual_usuario:
            usuario = actual_usuario.dato
            for libro in usuario.libros_prestados:
                self.tabla_prestamos.insertRow(row)
                self.tabla_prestamos.setRowHeight(row, 50)  # Establecer altura de la fila
                self.tabla_prestamos.setItem(row, 0, QTableWidgetItem(usuario.nombre))
                self.tabla_prestamos.setItem(row, 1, QTableWidgetItem(libro.titulo))
                self.tabla_prestamos.setItem(row, 2, QTableWidgetItem(libro.isbn))
                
                # Botón Devolver
                btn_devolver = QPushButton("📚 Devolver")
                btn_devolver.clicked.connect(lambda checked, u=usuario, l=libro: self.devolver_libro(u, l))
                self.tabla_prestamos.setCellWidget(row, 3, btn_devolver)
                
                row += 1
            actual_usuario = actual_usuario.siguiente
    
    def mostrar_agregar_libro(self):
        dialog = AgregarLibroDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                nuevo_libro = Libro(
                    titulo=dialog.titulo_input.text(),
                    autor=dialog.autor_input.text(),
                    isbn=dialog.isbn_input.text(),
                    cantidad_disponible=int(dialog.cantidad_input.text())
                )
                self.libros.agregar(nuevo_libro)
                self.actualizar_tabla_libros()
                QMessageBox.information(self, "Éxito", "Libro agregado correctamente")
            except ValueError:
                QMessageBox.warning(self, "Error", "Por favor, ingrese datos válidos")
        
    def mostrar_agregar_usuario(self):
        dialog = AgregarUsuarioDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                nuevo_usuario = Usuario(
                    nombre=dialog.nombre_input.text(),
                    id_usuario=dialog.id_input.text(),
                    email=dialog.email_input.text()
                )
                self.usuarios.agregar(nuevo_usuario)
                self.actualizar_tabla_usuarios()
                QMessageBox.information(self, "Éxito", "Usuario agregado correctamente")
            except ValueError:
                QMessageBox.warning(self, "Error", "Por favor, ingrese datos válidos")
        
    def mostrar_prestar_libro(self):
        if self.libros.esta_vacia():
            QMessageBox.warning(self, "Error", "No hay libros registrados")
            return
        if self.usuarios.esta_vacia():
            QMessageBox.warning(self, "Error", "No hay usuarios registrados")
            return
        
        dialog = PrestarLibroDialog(self.libros, self.usuarios, self)
        if dialog.exec_() == QDialog.Accepted:
            usuario = dialog.usuario_seleccionado
            libro = dialog.libro_seleccionado
            
            if usuario.tomar_prestado(libro):
                self.actualizar_tabla_libros()
                self.actualizar_tabla_prestamos()
                QMessageBox.information(
                    self, 
                    "Éxito", 
                    f"Libro '{libro.titulo}' prestado a {usuario.nombre}"
                )
            else:
                QMessageBox.warning(
                    self, 
                    "Error", 
                    "No se pudo realizar el préstamo"
                )

    def mostrar_menu_libro(self, position):
        menu = QMenu()
        editar_action = QAction("Editar", self)
        eliminar_action = QAction("Eliminar", self)
        
        menu.addAction(editar_action)
        menu.addAction(eliminar_action)
        
        item = self.tabla_libros.itemAt(position)
        if item:
            row = item.row()
            libro = self.obtener_libro_por_isbn(self.tabla_libros.item(row, 2).text())
            
            editar_action.triggered.connect(lambda: self.editar_libro(libro))
            eliminar_action.triggered.connect(lambda: self.eliminar_libro(libro))
            
            menu.exec_(self.tabla_libros.viewport().mapToGlobal(position))
    
    def mostrar_menu_usuario(self, position):
        menu = QMenu()
        editar_action = QAction("Editar", self)
        eliminar_action = QAction("Eliminar", self)
        
        menu.addAction(editar_action)
        menu.addAction(eliminar_action)
        
        item = self.tabla_usuarios.itemAt(position)
        if item:
            row = item.row()
            usuario = self.obtener_usuario_por_id(self.tabla_usuarios.item(row, 1).text())
            
            editar_action.triggered.connect(lambda: self.editar_usuario(usuario))
            eliminar_action.triggered.connect(lambda: self.eliminar_usuario(usuario))
            
            menu.exec_(self.tabla_usuarios.viewport().mapToGlobal(position))
    
    def mostrar_menu_prestamo(self, position):
        menu = QMenu()
        devolver_action = QAction("Devolver Libro", self)
        menu.addAction(devolver_action)
        
        item = self.tabla_prestamos.itemAt(position)
        if item:
            row = item.row()
            usuario = self.obtener_usuario_por_nombre(self.tabla_prestamos.item(row, 0).text())
            libro = self.obtener_libro_por_isbn(self.tabla_prestamos.item(row, 2).text())
            
            devolver_action.triggered.connect(lambda: self.devolver_libro(usuario, libro))
            
            menu.exec_(self.tabla_prestamos.viewport().mapToGlobal(position))
    
    def editar_libro(self, libro):
        dialog = EditarLibroDialog(libro, self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                libro.titulo = dialog.titulo_input.text()
                libro.autor = dialog.autor_input.text()
                libro.isbn = dialog.isbn_input.text()
                libro.cantidad_disponible = int(dialog.cantidad_input.text())
                self.actualizar_tabla_libros()
                QMessageBox.information(self, "Éxito", "Libro actualizado correctamente")
            except ValueError:
                QMessageBox.warning(self, "Error", "Por favor, ingrese datos válidos")
    
    def editar_usuario(self, usuario):
        dialog = EditarUsuarioDialog(usuario, self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                usuario.nombre = dialog.nombre_input.text()
                usuario.id_usuario = dialog.id_input.text()
                usuario.email = dialog.email_input.text()
                self.actualizar_tabla_usuarios()
                self.actualizar_tabla_prestamos()  # Por si cambió el nombre
                QMessageBox.information(self, "Éxito", "Usuario actualizado correctamente")
            except ValueError:
                QMessageBox.warning(self, "Error", "Por favor, ingrese datos válidos")
    
    def eliminar_libro(self, libro):
        if libro.prestamos:
            QMessageBox.warning(self, "Error", "No se puede eliminar un libro que está prestado")
            return
            
        if self.libros.eliminar(libro):
            self.actualizar_tabla_libros()
            QMessageBox.information(self, "Éxito", "Libro eliminado correctamente")
        else:
            QMessageBox.warning(self, "Error", "No se pudo eliminar el libro")
    
    def eliminar_usuario(self, usuario):
        if usuario.libros_prestados:
            QMessageBox.warning(self, "Error", "No se puede eliminar un usuario con libros prestados")
            return
            
        if self.usuarios.eliminar(usuario):
            self.actualizar_tabla_usuarios()
            QMessageBox.information(self, "Éxito", "Usuario eliminado correctamente")
        else:
            QMessageBox.warning(self, "Error", "No se pudo eliminar el usuario")
    
    def devolver_libro(self, usuario, libro):
        if usuario.devolver_libro(libro):
            self.actualizar_tabla_libros()
            self.actualizar_tabla_prestamos()
            QMessageBox.information(self, "Éxito", "Libro devuelto correctamente")
        else:
            QMessageBox.warning(self, "Error", "No se pudo devolver el libro")
    
    def obtener_libro_por_isbn(self, isbn):
        return self.libros.buscar(lambda l: l.isbn == isbn)
    
    def obtener_usuario_por_id(self, id_usuario):
        return self.usuarios.buscar(lambda u: u.id_usuario == id_usuario)
    
    def obtener_usuario_por_nombre(self, nombre):
        return self.usuarios.buscar(lambda u: u.nombre == nombre)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = BibliotecaGUI()
    ventana.show()
    sys.exit(app.exec_()) 