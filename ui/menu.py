import tkinter as tk

class Menu:
    """
    Clase que maneja la creación y gestión de la barra de menú principal de la aplicación.
    Proporciona acceso a todas las funcionalidades principales a través de menús desplegables.
    """

    def __init__(self, root, connect_db, create_new_db, disconnect_db, generate_erd, export_database):
        """
        Inicializa la barra de menú con las funciones de callback necesarias.

        Args:
            root: Ventana principal de la aplicación
            connect_db: Función para conectar base de datos
            create_new_db: Función para crear nueva base de datos
            disconnect_db: Función para desconectar base de datos
            generate_erd: Función para generar diagrama ERD
            export_database: Función para exportar base de datos
        """
        self.root = root
        self.connect_db = connect_db
        self.create_new_db = create_new_db
        self.disconnect_db = disconnect_db
        self.generate_erd = generate_erd
        self.export_database = export_database
        # Comandos del editor que se configurarán más tarde
        self.new_editor_command = None
        self.open_sql_command = None
        self.save_sql_command = None

    def create_menu(self):
        """
        Crea la estructura básica de la barra de menú.
        Incluye los menús de Archivo, Base de Datos, Herramientas y Editor.
        """
        # Crear barra de menú principal
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Configurar menú Archivo (las opciones se añadirán después)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Archivo", menu=self.file_menu)

        # Configurar menú Base de Datos
        db_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Base de Datos", menu=db_menu)
        db_menu.add_command(label="Conectar Base de Datos", command=self.connect_db)
        db_menu.add_command(label="Crear Nueva Base de Datos", command=self.create_new_db)
        db_menu.add_command(label="Desconectar Base de Datos", command=self.disconnect_db) 
        db_menu.add_separator()
        db_menu.add_command(label="Salir", command=self.root.quit)

        # Configurar menú Herramientas
        self.tools_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Herramientas", menu=self.tools_menu)
        self.tools_menu.add_command(label="Generar ERD", command=self.generate_erd, state="disabled")
        self.tools_menu.add_command(label="Exportar Base de Datos", command=self.export_database, state="disabled")

        # Configurar menú Editor
        self.editor_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Editor", menu=self.editor_menu)

    def add_editor_menu(self, new_editor_command, open_sql_command, save_sql_command):
        """
        Añade las opciones específicas del editor y completa el menú Archivo.

        Args:
            new_editor_command: Función para crear nuevo editor
            open_sql_command: Función para abrir archivo SQL
            save_sql_command: Función para guardar archivo SQL
        """
        self.new_editor_command = new_editor_command
        self.open_sql_command = open_sql_command
        self.save_sql_command = save_sql_command

        # Configurar opciones del menú Archivo
        self.file_menu.add_command(
            label="Abrir SQL...",
            command=self.open_sql_command,
            accelerator="Ctrl+O"
        )
        self.file_menu.add_command(
            label="Guardar SQL...",
            command=self.save_sql_command,
            accelerator="Ctrl+S"
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Salir", command=self.root.quit)

        # Configurar opciones del menú Editor
        self.editor_menu.add_command(
            label="Nuevo Editor SQL",
            command=self.new_editor_command,
            accelerator="Ctrl+N"
        )
        self.editor_menu.add_separator()
        self.editor_menu.add_command(
            label="Ejecutar SQL",
            command=lambda: self.root.event_generate('<<ExecuteSQL>>'),
            accelerator="Ctrl+Enter"
        )
        self.editor_menu.add_command(
            label="Cerrar Editor Actual",
            command=lambda: self.root.event_generate('<<CloseEditor>>'),
            accelerator="Ctrl+W"
        )

        # Configurar menú de Ayuda
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Acerca de", command=self.show_about)

    def show_about(self):
        """
        Muestra la ventana 'Acerca de' con información sobre la aplicación.
        Crea una instancia de AboutWindow para mostrar los detalles.
        """
        from ui.about_window import AboutWindow
        AboutWindow(self.root)