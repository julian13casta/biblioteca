# Sistema de Gestión de Biblioteca

Una aplicación de escritorio para gestionar el inventario, usuarios y préstamos de una biblioteca, desarrollada en Python con PyQt5. Incluye estructuras de datos avanzadas (árboles binarios de búsqueda y grafos) para optimizar la eficiencia y funcionalidades como recomendaciones y análisis de relaciones.

## Características

- Gestión de libros (agregar, editar, eliminar)
- Gestión de usuarios (agregar, editar, eliminar)
- Sistema de préstamos y devoluciones
- Recomendaciones de libros personalizadas
- Visualización de libros relacionados
- Persistencia automática de datos en archivos JSON
- Interfaz gráfica intuitiva y moderna
- Validaciones para operaciones seguras

## Estructuras de Datos Utilizadas

- **Árbol Binario de Búsqueda (ABB):** Para almacenar y buscar libros y usuarios de manera eficiente.
- **Grafo:** Para modelar las relaciones de préstamo entre usuarios y libros, permitiendo recomendaciones y análisis de relaciones complejas.

## Requisitos del Sistema

- Python 3.6 o superior
- PyQt5

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/sistema-biblioteca.git
cd sistema-biblioteca
```

2. Instala las dependencias:
```bash
pip install PyQt5
```

## Estructura del Proyecto

```
├── main.py                  # Archivo principal de la aplicación
├── models/                  # Modelos de datos (Libro, Usuario)
├── estructuras/             # Implementaciones de árboles y grafos
├── dialogs/                 # Diálogos de la interfaz gráfica
├── data/                    # Archivos JSON para persistencia de datos
│   ├── libros.json
│   ├── usuarios.json
│   └── prestamos.json
├── tests/                   # Pruebas unitarias
├── requirements.txt         # Dependencias del proyecto
└── README.md                # Este archivo
```

## Uso

1. Ejecuta la aplicación:
```bash
python main.py
```
2. Gestiona libros, usuarios y préstamos desde la interfaz gráfica.
3. Utiliza las funciones de recomendaciones y libros relacionados para mejorar la experiencia del usuario.


