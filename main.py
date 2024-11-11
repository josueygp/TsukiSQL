import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox, filedialog
from db.connection import DatabaseManager
from ui.menu import Menu
from ui.ui_builder import UIBuilder
from utils.erd_generator import generate_erd_dialog, generate_erd
from utils.exporter import export_database
from ui.sql_executor import on_table_select, execute_sql, display_results
from ui.ui_updater import update_tools_menu_state, update_db_label, update_tables_list


class TsukiSQLApp:
    """
    Clase principal que representa la aplicación TsukiSQL.
    Maneja la interfaz gráfica y la lógica principal de la aplicación.
    """
    
    def __init__(self, root):
        """
        Inicializa la aplicación TsukiSQL.
        
        Args:
            root: Ventana principal de Tkinter
        """
        self.root = root
        self.root.title("TsukiSQL")
        self.db_connection = None  # Conexión actual a la base de datos
        self.db_path = None       # Ruta de la base de datos actual
        self.db_manager = DatabaseManager()

        # Configuración del menú principal
        self.menu = Menu(
            self.root,
            self.connect_db,
            self.create_new_db,
            self.disconnect_db,
            self.generate_erd,
            self.export_database_wrapper
        )
        self.menu.create_menu()

        # Agregar menú de editor
        self.menu.add_editor_menu(
            self.create_new_editor,
            self.open_sql_file,
            self.save_sql_file
        )

        # Etiqueta para mostrar la base de datos conectada
        self.db_label = tk.Label(self.root, text="No hay base de datos conectada")
        self.db_label.pack(padx=10, pady=5)

        # Inicialización de componentes UI
        self.ui_builder = UIBuilder(self.root, self.on_table_select)
        
        # Frame para botones
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(pady=5)

        # Botón de ejecución SQL
        self.execute_button = ttk.Button(
            self.button_frame,
            text="Ejecutar SQL",
            command=self.execute_sql
        )
        self.execute_button.pack(side=tk.LEFT, padx=5)

        # Crear el primer editor por defecto
        self.ui_builder.create_sql_editor()

        # Configurar atajos de teclado
        self.root.bind('<Control-n>', lambda e: self.create_new_editor())
        self.root.bind('<Control-Return>', lambda e: self.execute_sql())
        self.root.bind('<Control-o>', lambda e: self.open_sql_file())
        self.root.bind('<Control-s>', lambda e: self.save_sql_file())
        self.root.bind('<Control-w>', lambda e: self.close_current_editor())

    def close_current_editor(self):
        """
        Cierra la pestaña del editor actualmente seleccionada.
        """
        current_tab = self.ui_builder.notebook.select()
        if current_tab:
            tab_text = self.ui_builder.notebook.tab(current_tab, "text")
            self.ui_builder.close_editor(tab_text)

    def open_sql_file(self):
        """
        Abre un archivo SQL y muestra su contenido en un nuevo editor.
        Maneja la selección de archivo mediante un diálogo y actualiza la interfaz.
        """
        file_path = filedialog.askopenfilename(
            defaultextension=".sql",
            filetypes=[("SQL files", "*.sql"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    new_editor = self.create_new_editor()
                    if new_editor:
                        new_editor.delete('1.0', tk.END)
                        new_editor.insert('1.0', content)
                        current_tab = self.ui_builder.notebook.select()
                        if current_tab:
                            file_name = file_path.split('/')[-1]
                            self.ui_builder.notebook.tab(current_tab, text=file_name)
                            new_editor.focus_set()
                            self.ui_builder.sql_text = new_editor
                            self.ui_builder.append_to_console(f"Archivo SQL abierto: {file_name}", 'info')
            except Exception as e:
                error_msg = f"Error al abrir el archivo: {str(e)}"
                self.ui_builder.append_to_console(error_msg, 'error')
                messagebox.showerror("Error", error_msg)

    def save_sql_file(self):
        """
        Guarda el contenido del editor actual en un archivo SQL.
        Maneja el diálogo de guardado y actualiza la interfaz.
        """
        current_editor = self.get_current_editor()
        if not current_editor:
            messagebox.showwarning("Advertencia", "No hay editor activo para guardar")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".sql",
            filetypes=[("SQL files", "*.sql"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                content = current_editor.get('1.0', tk.END)
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                
                current_tab = self.ui_builder.notebook.select()
                if current_tab:
                    file_name = file_path.split('/')[-1]
                    self.ui_builder.notebook.tab(current_tab, text=file_name)
                    
                messagebox.showinfo("Éxito", "Archivo guardado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar el archivo: {str(e)}")   

    def create_new_editor(self):
        """
        Crea una nueva pestaña de editor SQL.
        Returns:
            El nuevo editor creado
        """
        return self.ui_builder.create_sql_editor()

    def get_current_editor(self):
        """
        Obtiene el editor actualmente activo.
        Returns:
            El editor activo o None si no hay ninguno
        """
        return self.ui_builder.get_current_editor()

    def connect_db(self):
        """
        Establece conexión con una base de datos existente.
        Actualiza la interfaz según el resultado de la conexión.
        """
        success, db_connection, db_path = self.db_manager.connect_db()
        if success:
            self.db_connection = db_connection
            self.db_path = db_path
            update_db_label(self.db_label, self.db_path)
            update_tools_menu_state(self.menu, True)
            update_tables_list(self.db_connection, self.ui_builder.tables_listbox)
            self.ui_builder.append_to_console(f"Conectado a la base de datos: {db_path}", 'success')

    def disconnect_db(self):
        """
        Desconecta la base de datos actual y actualiza la interfaz.
        """
        if self.db_manager.disconnect_db():
            self.db_connection = None
            self.db_path = None
            update_db_label(self.db_label, self.db_path)
            update_tools_menu_state(self.menu, False)
            self.ui_builder.tables_listbox.delete(0, tk.END)
            self.ui_builder.append_to_console("Desconectado de la base de datos", 'info')

    def create_new_db(self):
        """
        Crea una nueva base de datos SQLite y establece conexión con ella.
        Actualiza la interfaz según el resultado de la creación.
        """
        success, db_connection, db_path = self.db_manager.create_new_db()
        if success:
            self.db_connection = db_connection
            self.db_path = db_path
            update_db_label(self.db_label, self.db_path)
            update_tools_menu_state(self.menu, True)
            update_tables_list(self.db_connection, self.ui_builder.tables_listbox)

    def generate_erd(self):
        """
        Inicia el proceso de generación del diagrama ERD.
        """
        generate_erd_dialog(self.db_connection, generate_erd)

    def export_database_wrapper(self):
        """
        Maneja la exportación de la base de datos actual.
        Muestra mensaje de advertencia si no hay base de datos conectada.
        """
        if self.db_connection:
            export_database(self.db_connection)
        else:
            messagebox.showwarning("Advertencia", "No hay base de datos conectada para exportar.")

    def execute_sql_in_console(self, sql_command):
        """
        Ejecuta comandos SQL directamente desde la consola.
        
        Args:
            sql_command: Comando SQL a ejecutar
        """
        if self.db_connection:
            execute_sql(
                self.db_connection,
                None,  # No editor needed
                self.ui_builder.results_table,
                lambda conn: update_tables_list(conn, self.ui_builder.tables_listbox),
                self.ui_builder,
                custom_sql=sql_command
            )

    def on_table_select(self, event):
        """
        Manejador de eventos para la selección de tablas.
        Ejecuta una consulta SELECT * cuando se selecciona una tabla.
        
        Args:
            event: Evento de selección
        """
        selected_index = self.ui_builder.tables_listbox.curselection()
        if selected_index:
            table_name = self.ui_builder.tables_listbox.get(selected_index)
            sql_command = f"SELECT * FROM {table_name}"
            self.execute_sql_in_console(sql_command)

    def execute_sql(self):
        """
        Ejecuta el SQL desde el editor activo.
        Muestra advertencia si no hay editor activo.
        """
        current_editor = self.get_current_editor()
        if current_editor:
            execute_sql(
                self.db_connection,
                current_editor,
                self.ui_builder.results_table,
                lambda conn: update_tables_list(conn, self.ui_builder.tables_listbox),
                self.ui_builder
            )
        else:
            messagebox.showwarning("Advertencia", "No hay editor activo")

    def display_results(self, rows, description):
        """
        Muestra los resultados de una consulta en la tabla de resultados.
        
        Args:
            rows: Filas de resultados
            description: Descripción de las columnas
        """
        display_results(rows, description, self.ui_builder.results_table)


if __name__ == "__main__":
    root = tk.Tk()
    app = TsukiSQLApp(root)
    root.geometry("800x600")
    root.mainloop()