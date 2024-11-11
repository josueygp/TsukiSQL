import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

class UIBuilder:
    """
    Clase responsable de construir y gestionar la interfaz de usuario de la aplicación.
    Maneja la creación de editores SQL, paneles de resultados y estructura de la base de datos.
    """

    def __init__(self, root, on_table_select_callback):
        """
        Inicializa el constructor de la interfaz de usuario.

        Args:
            root: Ventana principal de Tkinter
            on_table_select_callback: Función callback para manejar la selección de tablas
        """
        self.root = root
        self.on_table_select_callback = on_table_select_callback
        self.editors = {}              # Diccionario para almacenar los editores
        self.editor_count = 0          # Contador de editores creados
        self.results_frame = None      # Frame para resultados
        self.results_table = None      # Tabla de resultados
        self.tables_listbox = None     # Lista de tablas
        self.notebook = None           # Notebook para editores
        self.console = None            # Consola de mensajes
        self.setup_main_layout()

    def setup_main_layout(self):
        """
        Crea el diseño principal de la aplicación con paneles redimensionables.
        Configura la estructura básica de la interfaz dividida en secciones.
        """
        # Crear PanedWindow horizontal principal
        self.main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True)

        # Panel izquierdo para estructura de base de datos
        self.left_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(self.left_frame, weight=1)

        # Crear panel de filtro y estructura de base de datos
        self.create_tables_list()

        # Contenedor del panel derecho
        self.right_paned = ttk.PanedWindow(self.main_paned, orient=tk.VERTICAL)
        self.main_paned.add(self.right_paned, weight=3)

        # Crear notebook para editores SQL
        self.notebook = ttk.Notebook(self.right_paned)
        self.right_paned.add(self.notebook, weight=2)

        # Panel de resultados y consola
        self.results_frame = ttk.Frame(self.right_paned)
        self.right_paned.add(self.results_frame, weight=1)

        # Crear consola y resultados en disposición vertical
        self.create_console_and_results()
    
    def create_console_and_results(self):
        """
        Crea el área de consola y resultados con pestañas separadas.
        Configura la visualización de resultados y mensajes del sistema.
        """
        # Crear notebook para resultados y consola
        results_notebook = ttk.Notebook(self.results_frame)
        results_notebook.pack(fill=tk.BOTH, expand=True)

        # Pestaña de resultados
        results_frame = ttk.Frame(results_notebook)
        results_notebook.add(results_frame, text="Results")

        # Crear tabla de resultados con barras de desplazamiento
        self.create_results_table(results_frame)

        # Pestaña de consola
        console_frame = ttk.Frame(results_notebook)
        results_notebook.add(console_frame, text="Console")
        
        # Configurar widget de consola
        self.console = scrolledtext.ScrolledText(
            console_frame,
            wrap=tk.WORD,
            height=5,
            background='black',
            foreground='white',
            font=('Courier', 10)
        )
        self.console.pack(fill=tk.BOTH, expand=True)
        
    def create_tables_list(self):
        """
        Crea el panel de estructura de base de datos con lista de tablas.
        Configura la vista de árbol para mostrar la estructura de la base de datos.
        """
        tables_frame = ttk.LabelFrame(self.left_frame, text="Database Structure")
        tables_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)

        # Crear tree view para estructura de base de datos
        self.db_tree = ttk.Treeview(tables_frame, show='tree')
        self.db_tree.pack(fill=tk.BOTH, expand=True)

        # Agregar barra de desplazamiento
        scrollbar = ttk.Scrollbar(tables_frame, orient="vertical", command=self.db_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.db_tree.configure(yscrollcommand=scrollbar.set)

        # Estructura de ejemplo
        db_node = self.db_tree.insert("", "end", text="Database", open=True)
        tables_node = self.db_tree.insert(db_node, "end", text="Tables", open=True)
        self.db_tree.insert(tables_node, "end", text="Sample Table")

    def append_to_console(self, text, type='info'):
        """
        Añade texto a la consola con estilo opcional.

        Args:
            text: Texto a mostrar en la consola
            type: Tipo de mensaje ('info', 'error', 'success')
        """
        self.console.config(state='normal')
        if type == 'error':
            tag = 'error'
            self.console.tag_config(tag, foreground='red')
        elif type == 'success':
            tag = 'success'
            self.console.tag_config(tag, foreground='green')
        else:
            tag = 'info'
            self.console.tag_config(tag, foreground='white')
            
        self.console.insert(tk.END, f"{text}\n", tag)
        self.console.see(tk.END)
        self.console.config(state='disabled')

    def create_sql_editor(self, name=None):
        """
        Crea una nueva pestaña de editor SQL.

        Args:
            name: Nombre opcional para el editor

        Returns:
            Widget del editor de texto creado
        """
        if name is None:
            self.editor_count += 1
            name = f"SQL Editor {self.editor_count}"
        
        editor_frame = ttk.Frame(self.notebook)
        
        # Crear frame contenedor para editor y botón de cierre
        header_frame = ttk.Frame(editor_frame)
        header_frame.pack(fill=tk.X)
        
        # Crear botón de cierre
        close_button = ttk.Button(
            header_frame,
            text="×",
            width=2,
            command=lambda: self.close_editor(name)
        )
        close_button.pack(side=tk.RIGHT, padx=(0, 5), pady=2)
        
        # Crear editor de texto SQL con barras de desplazamiento
        sql_frame = ttk.Frame(editor_frame)
        sql_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))

        sql_text = scrolledtext.ScrolledText(
            sql_frame,
            wrap=tk.WORD,
            width=50,
            height=10
        )
        sql_text.pack(fill=tk.BOTH, expand=True)

        # Almacenar información del editor
        self.editors[name] = {
            'frame': editor_frame,
            'text_widget': sql_text,
            'close_button': close_button
        }

        # Añadir nueva pestaña al notebook
        self.notebook.add(editor_frame, text=name)
        
        # Actualizar editor actual
        self.sql_text = sql_text
        
        # Seleccionar nueva pestaña
        self.notebook.select(editor_frame)
        
        return sql_text

    def close_editor(self, name):
        """
        Cierra la pestaña del editor especificado.

        Args:
            name: Nombre del editor a cerrar
        """
        if name in self.editors:
            frame = self.editors[name]['frame']
            tab_id = self.notebook.select()
            
            # Encontrar índice de la pestaña a cerrar
            tab_index = self.notebook.index(tab_id)
            
            # Eliminar pestaña
            self.notebook.forget(frame)
            del self.editors[name]
            
            # Si quedan editores, seleccionar uno adyacente
            if self.editors:
                new_index = max(0, tab_index - 1)
                if new_index < self.notebook.index('end'):
                    self.notebook.select(new_index)
                    remaining_name = list(self.editors.keys())[new_index]
                    self.sql_text = self.editors[remaining_name]['text_widget']
            else:
                # Si no quedan editores, crear uno nuevo
                self.create_sql_editor()

    def get_current_editor(self):
        """
        Obtiene el widget del editor actualmente activo.

        Returns:
            Widget del editor activo o None si no hay ninguno
        """
        current_tab = self.notebook.select()
        if current_tab:
            return self.sql_text
        return None

    def get_all_editors(self):
        """
        Obtiene una lista de todos los widgets de editores.

        Returns:
            Lista de widgets de editores
        """
        return [editor['text_widget'] for editor in self.editors.values()]

    def create_tables_list(self):
        """
        Crea el panel de estructura de base de datos con lista de tablas.
        Configura la lista y sus eventos de selección.
        """
        tables_frame = ttk.LabelFrame(self.left_frame, text="Database Structure")
        tables_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Crear listbox con barra de desplazamiento
        scrollbar = ttk.Scrollbar(tables_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tables_listbox = tk.Listbox(
            tables_frame,
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE
        )
        self.tables_listbox.pack(fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)
        
        scrollbar.config(command=self.tables_listbox.yview)
        self.tables_listbox.bind("<<ListboxSelect>>", self.on_table_select_callback)

    def create_results_area(self):
        """
        Crea el área de resultados con una vista de tabla.
        Configura la tabla y sus barras de desplazamiento.
        """
        results_label_frame = ttk.LabelFrame(self.results_frame, text="Results")
        results_label_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Crear barras de desplazamiento
        x_scrollbar = ttk.Scrollbar(results_label_frame, orient=tk.HORIZONTAL)
        y_scrollbar = ttk.Scrollbar(results_label_frame)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Crear treeview con barras de desplazamiento
        self.results_table = ttk.Treeview(
            results_label_frame,
            show='headings',
            xscrollcommand=x_scrollbar.set,
            yscrollcommand=y_scrollbar.set
        )
        self.results_table.pack(fill=tk.BOTH, expand=True)

        # Configurar barras de desplazamiento
        x_scrollbar.config(command=self.results_table.xview)
        y_scrollbar.config(command=self.results_table.yview)

    def create_results_table(self, parent):
        """
        Crea la tabla de resultados con barras de desplazamiento apropiadas.

        Args:
            parent: Widget padre donde se creará la tabla
        """
        # Crear frame contenedor para la tabla
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill=tk.BOTH, expand=True)

        # Crear barras de desplazamiento
        x_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        y_scrollbar = ttk.Scrollbar(table_frame)
        
        # Crear treeview
        self.results_table = ttk.Treeview(
            table_frame,
            show='headings',
            xscrollcommand=x_scrollbar.set,
            yscrollcommand=y_scrollbar.set
        )
        
        # Configurar comandos de barras de desplazamiento
        x_scrollbar.config(command=self.results_table.xview)
        y_scrollbar.config(command=self.results_table.yview)
        
        # Disposición de grid para comportamiento correcto de barras
        self.results_table.grid(row=0, column=0, sticky='nsew')
        y_scrollbar.grid(row=0, column=1, sticky='ns')
        x_scrollbar.grid(row=1, column=0, sticky='ew')
        
        # Configurar pesos de grid
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)