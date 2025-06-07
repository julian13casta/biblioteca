import sys
import os
import json
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
from estructuras.arbol_binario_busqueda import ArbolBinarioBusqueda
from estructuras.grafo import Grafo
from dialogs.agregar_libro_dialog import AgregarLibroDialog
from dialogs.agregar_usuario_dialog import AgregarUsuarioDialog
from dialogs.prestar_libro_dialog import PrestarLibroDialog
from dialogs.editar_libro_dialog import EditarLibroDialog
from dialogs.editar_usuario_dialog import EditarUsuarioDialog
import logging

# Configurar logging
logging.basicConfig(
    filename='biblioteca.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class BibliotecaGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión de Biblioteca")
        self.setGeometry(100, 100, 1200, 800)
        
        # Configurar estilo y colores
        self.configurar_estilo()
        
        # Inicializar estructuras de datos
        self.libros = ArbolBinarioBusqueda()
        self.usuarios = ArbolBinarioBusqueda()
        self.grafo = Grafo()  # Nueva estructura de datos
        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')
        self.cargar_datos_archivos()
        self.configurar_ui()
        self.actualizar_tabla_libros()
        self.actualizar_tabla_usuarios()
        self.actualizar_tabla_prestamos()
                
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
        
        # Agregar botones para nuevas funcionalidades
        btn_libros_relacionados = QPushButton("📚 Libros Relacionados")
        btn_libros_relacionados.clicked.connect(lambda: self.mostrar_libros_relacionados(
            self.obtener_libro_seleccionado()))
        panel_botones.addWidget(btn_libros_relacionados)

        btn_recomendaciones = QPushButton("🎯 Recomendaciones")
        btn_recomendaciones.clicked.connect(lambda: self.mostrar_recomendaciones_usuario(
            self.obtener_usuario_seleccionado()))
        panel_botones.addWidget(btn_recomendaciones)
        
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
        self._recorrer_arbol_libros(self.libros.raiz, 0)
        
    def _recorrer_arbol_libros(self, nodo, row):
        if nodo is not None:
            row = self._recorrer_arbol_libros(nodo.izquierda, row)
            libro = nodo.dato
            self.tabla_libros.insertRow(row)
            self.tabla_libros.setRowHeight(row, 50)
            self.tabla_libros.setItem(row, 0, QTableWidgetItem(libro.titulo))
            self.tabla_libros.setItem(row, 1, QTableWidgetItem(libro.autor))
            self.tabla_libros.setItem(row, 2, QTableWidgetItem(libro.isbn))
            self.tabla_libros.setItem(row, 3, QTableWidgetItem(str(libro.cantidad_disponible)))
            btn_editar = QPushButton("✏️ Editar")
            btn_editar.clicked.connect(lambda checked, l=libro: self.editar_libro(l))
            self.tabla_libros.setCellWidget(row, 4, btn_editar)
            btn_eliminar = QPushButton("❌ Eliminar")
            btn_eliminar.clicked.connect(lambda checked, l=libro: self.eliminar_libro(l))
            self.tabla_libros.setCellWidget(row, 5, btn_eliminar)
            row += 1
            row = self._recorrer_arbol_libros(nodo.derecha, row)
        return row

    def actualizar_tabla_usuarios(self):
        self.tabla_usuarios.setRowCount(0)
        self._recorrer_arbol_usuarios(self.usuarios.raiz, 0)
    
    def _recorrer_arbol_usuarios(self, nodo, row):
        if nodo is not None:
            row = self._recorrer_arbol_usuarios(nodo.izquierda, row)
            usuario = nodo.dato
            self.tabla_usuarios.insertRow(row)
            self.tabla_usuarios.setRowHeight(row, 50)
            self.tabla_usuarios.setItem(row, 0, QTableWidgetItem(usuario.nombre))
            self.tabla_usuarios.setItem(row, 1, QTableWidgetItem(usuario.id_usuario))
            self.tabla_usuarios.setItem(row, 2, QTableWidgetItem(usuario.email))
            btn_editar = QPushButton("✏️ Editar")
            btn_editar.clicked.connect(lambda checked, u=usuario: self.editar_usuario(u))
            self.tabla_usuarios.setCellWidget(row, 3, btn_editar)
            btn_eliminar = QPushButton("❌ Eliminar")
            btn_eliminar.clicked.connect(lambda checked, u=usuario: self.eliminar_usuario(u))
            self.tabla_usuarios.setCellWidget(row, 4, btn_eliminar)
            row += 1
            row = self._recorrer_arbol_usuarios(nodo.derecha, row)
        return row

    def actualizar_tabla_prestamos(self):
        """Actualiza la tabla de préstamos activos usando el grafo."""
        self.tabla_prestamos.setRowCount(0)
        row = 0

        # Recorrer todos los nodos del grafo
        for nodo_id, nodo in self.grafo.nodos.items():
            if nodo.tipo == 'usuario':  # Si es un usuario
                usuario = nodo.datos
                # Buscar los libros prestados por este usuario
                for vecino_id, peso in nodo.vecinos.items():
                    if self.grafo.nodos[vecino_id].tipo == 'libro':
                        libro = self.grafo.nodos[vecino_id].datos
                        # Agregar el préstamo a la tabla
                        self.tabla_prestamos.insertRow(row)
                        self.tabla_prestamos.setItem(row, 0, QTableWidgetItem(usuario.nombre))
                        self.tabla_prestamos.setItem(row, 1, QTableWidgetItem(libro.titulo))
                        self.tabla_prestamos.setItem(row, 2, QTableWidgetItem(libro.isbn))
                        
                        # Botón de devolver
                        btn_devolver = QPushButton("Devolver")
                        btn_devolver.clicked.connect(lambda checked, u=usuario, l=libro: self.devolver_libro(u, l))
                        self.tabla_prestamos.setCellWidget(row, 3, btn_devolver)
                        
                        row += 1

    def closeEvent(self, event):
        self.guardar_datos_archivos()
        event.accept()

    # --- Persistencia ---
    def cargar_datos_archivos(self):
        # Cargar libros
        libros_path = os.path.join(self.data_dir, 'libros.json')
        usuarios_path = os.path.join(self.data_dir, 'usuarios.json')
        prestamos_path = os.path.join(self.data_dir, 'prestamos.json')
        if os.path.exists(libros_path):
            with open(libros_path, 'r', encoding='utf-8') as f:
                libros_data = json.load(f)
                for l in libros_data:
                    libro = Libro(**l)
                    self.libros.agregar(libro)
                    self.grafo.agregar_nodo(libro.isbn, 'libro', libro)
        if os.path.exists(usuarios_path):
            with open(usuarios_path, 'r', encoding='utf-8') as f:
                usuarios_data = json.load(f)
                for u in usuarios_data:
                    usuario = Usuario(**u)
                    self.usuarios.agregar(usuario)
                    self.grafo.agregar_nodo(usuario.id_usuario, 'usuario', usuario)
        if os.path.exists(prestamos_path):
            with open(prestamos_path, 'r', encoding='utf-8') as f:
                prestamos_data = json.load(f)
                for p in prestamos_data:
                    self.grafo.agregar_arista(p['usuario_id'], p['libro_isbn'])
                    libro = self.obtener_libro_por_isbn(p['libro_isbn'])
                    if libro:
                        libro.cantidad_disponible -= 1

    def guardar_datos_archivos(self):
        libros_path = os.path.join(self.data_dir, 'libros.json')
        usuarios_path = os.path.join(self.data_dir, 'usuarios.json')
        prestamos_path = os.path.join(self.data_dir, 'prestamos.json')
        # Serializar libros
        libros = []
        self._recorrer_arbol_serializar(self.libros.raiz, libros, tipo='libro')
        with open(libros_path, 'w', encoding='utf-8') as f:
            json.dump(libros, f, ensure_ascii=False, indent=2)
        # Serializar usuarios
        usuarios = []
        self._recorrer_arbol_serializar(self.usuarios.raiz, usuarios, tipo='usuario')
        with open(usuarios_path, 'w', encoding='utf-8') as f:
            json.dump(usuarios, f, ensure_ascii=False, indent=2)
        # Serializar préstamos (aristas del grafo)
        prestamos = []
        for nodo_id, nodo in self.grafo.nodos.items():
            if nodo.tipo == 'usuario':
                for vecino_id in nodo.vecinos:
                    if self.grafo.nodos[vecino_id].tipo == 'libro':
                        prestamos.append({'usuario_id': nodo_id, 'libro_isbn': vecino_id})
        with open(prestamos_path, 'w', encoding='utf-8') as f:
            json.dump(prestamos, f, ensure_ascii=False, indent=2)

    def _recorrer_arbol_serializar(self, nodo, lista, tipo):
        if nodo is not None:
            self._recorrer_arbol_serializar(nodo.izquierda, lista, tipo)
            if tipo == 'libro':
                lista.append({
                    'titulo': nodo.dato.titulo,
                    'autor': nodo.dato.autor,
                    'isbn': nodo.dato.isbn,
                    'cantidad_disponible': nodo.dato.cantidad_disponible
                })
            elif tipo == 'usuario':
                lista.append({
                    'nombre': nodo.dato.nombre,
                    'id_usuario': nodo.dato.id_usuario,
                    'email': nodo.dato.email
                })
            self._recorrer_arbol_serializar(nodo.derecha, lista, tipo)

    # --- Modificar métodos para guardar automáticamente ---
    def mostrar_agregar_libro(self):
        dialog = AgregarLibroDialog(self)
        if dialog.exec_():
            libro = dialog.obtener_libro()
            self.libros.agregar(libro)
            self.grafo.agregar_nodo(libro.isbn, 'libro', libro)
            self.guardar_datos_archivos()
            self.actualizar_tabla_libros()

    def mostrar_agregar_usuario(self):
        dialog = AgregarUsuarioDialog(self)
        if dialog.exec_():
            usuario = dialog.obtener_usuario()
            self.usuarios.agregar(usuario)
            self.grafo.agregar_nodo(usuario.id_usuario, 'usuario', usuario)
            self.guardar_datos_archivos()
            self.actualizar_tabla_usuarios()

    def mostrar_prestar_libro(self):
        if self.libros.esta_vacio():
            QMessageBox.warning(self, "Error", "No hay libros registrados")
            return
        if self.usuarios.esta_vacio():
            QMessageBox.warning(self, "Error", "No hay usuarios registrados")
            return
        dialog = PrestarLibroDialog(self)
        if dialog.exec_():
            usuario, libro = dialog.obtener_prestamo()
            if usuario and libro:
                if libro.cantidad_disponible > 0:
                    libro.cantidad_disponible -= 1
                    self.grafo.agregar_arista(usuario.id_usuario, libro.isbn)
                    self.guardar_datos_archivos()
                    self.actualizar_tabla_libros()
                    self.actualizar_tabla_prestamos()
                    QMessageBox.information(self, "Éxito", 
                        f"Libro '{libro.titulo}' prestado a {usuario.nombre}")
                else:
                    QMessageBox.warning(self, "Error", 
                        "No hay ejemplares disponibles de este libro.")

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
                self.guardar_datos_archivos()
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
                self.guardar_datos_archivos()
                QMessageBox.information(self, "Éxito", "Usuario actualizado correctamente")
            except ValueError:
                QMessageBox.warning(self, "Error", "Por favor, ingrese datos válidos")
    
    def eliminar_libro(self, libro):        
        if libro.prestamos:
            QMessageBox.warning(self, "Error", "No se puede eliminar un libro que está prestado")
            return            

        libro_a_eliminar = self.libros.buscar(libro.get_id())
        if libro_a_eliminar is None:
             QMessageBox.warning(self, "Error", "No se pudo eliminar el libro") 
             return
        
        self.libros.eliminar(libro.get_id())
        self.actualizar_tabla_libros()
        self.guardar_datos_archivos()
        QMessageBox.information(self, "Éxito", "Libro eliminado correctamente")
    
    def eliminar_usuario(self, usuario):
        if usuario.libros_prestados:
            QMessageBox.warning(self, "Error", "No se puede eliminar un usuario con libros prestados")
            return
            
        usuario_a_eliminar = self.usuarios.buscar(usuario.get_id())        
        if usuario_a_eliminar is None:
            QMessageBox.warning(self, "Error", "No se pudo eliminar el usuario")
            return
        
        self.usuarios.eliminar(usuario.get_id())
        self.actualizar_tabla_usuarios()
        self.guardar_datos_archivos()
        QMessageBox.information(self, "Éxito", "Usuario eliminado correctamente")
    
    def devolver_libro(self, usuario, libro):
        """Maneja la devolución de un libro."""
        if QMessageBox.question(self, "Confirmar", 
                              f"¿Desea devolver el libro {libro.titulo}?") == QMessageBox.Yes:
            # Actualizar cantidad disponible
            libro.cantidad_disponible += 1
            
            # Eliminar la arista del grafo
            self.grafo.eliminar_arista(usuario.id_usuario, libro.isbn)
            
            # Actualizar las tablas
            self.actualizar_tabla_libros()
            self.actualizar_tabla_prestamos()
            self.guardar_datos_archivos()
            
            QMessageBox.information(self, "Éxito", 
                                  f"Libro '{libro.titulo}' devuelto correctamente")

    def obtener_libro_por_isbn(self, isbn): 
        return self.libros.buscar(isbn)
    
    def obtener_usuario_por_id(self, id_usuario): 
        return self.usuarios.buscar(id_usuario)
    
    def obtener_usuario_por_nombre(self, nombre_buscado):
        self.usuario_encontrado = None
        self._recorrer_arbol_usuarios_busqueda(self.usuarios.raiz, nombre_buscado)
        return self.usuario_encontrado
    
    def _recorrer_arbol_usuarios_busqueda(self, nodo, nombre_buscado):
        if nodo is not None:
            self._recorrer_arbol_usuarios_busqueda(nodo.izquierda, nombre_buscado)
            usuario = nodo.dato
            if usuario.nombre == nombre_buscado:
                self.usuario_encontrado = usuario
                return 
            self._recorrer_arbol_usuarios_busqueda(nodo.derecha, nombre_buscado)

    def mostrar_libros_relacionados(self, libro):
        """Muestra los libros relacionados con el libro seleccionado."""
        if libro is None:
            QMessageBox.warning(self, "Error", "Por favor, seleccione un libro primero.")
            return
            
        libros_relacionados = self.grafo.obtener_libros_relacionados(libro.isbn)
        if libros_relacionados:
            mensaje = f"Libros relacionados con {libro.titulo}:\n\n"
            for libro_rel in libros_relacionados:
                mensaje += f"- {libro_rel.titulo} ({libro_rel.autor})\n"
            QMessageBox.information(self, "Libros Relacionados", mensaje)
        else:
            QMessageBox.information(self, "Libros Relacionados", 
                                  f"No se encontraron libros relacionados con {libro.titulo}.")

    def mostrar_recomendaciones_usuario(self, usuario):
        """Muestra recomendaciones de libros para el usuario seleccionado."""
        if usuario is None:
            QMessageBox.warning(self, "Error", "Por favor, seleccione un usuario primero.")
            return
            
        recomendaciones = self.grafo.obtener_recomendaciones_usuario(usuario.id_usuario)
        if recomendaciones:
            mensaje = f"Recomendaciones para {usuario.nombre}:\n\n"
            for libro in recomendaciones:
                mensaje += f"- {libro.titulo} ({libro.autor})\n"
            QMessageBox.information(self, "Recomendaciones", mensaje)
        else:
            QMessageBox.information(self, "Recomendaciones", 
                                  f"No hay recomendaciones disponibles para {usuario.nombre}.")

    def obtener_libro_seleccionado(self):
        """Retorna el libro seleccionado en la tabla de libros."""
        fila = self.tabla_libros.currentRow()
        if fila >= 0:
            isbn = self.tabla_libros.item(fila, 2).text()
            return self.obtener_libro_por_isbn(isbn)
        return None

    def obtener_usuario_seleccionado(self):
        """Retorna el usuario seleccionado en la tabla de usuarios."""
        fila = self.tabla_usuarios.currentRow()
        if fila >= 0:
            id_usuario = self.tabla_usuarios.item(fila, 1).text()
            return self.obtener_usuario_por_id(id_usuario)
        return None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = BibliotecaGUI()
    ventana.show()
    sys.exit(app.exec_()) 