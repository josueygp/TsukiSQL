import sqlite3
from tkinter import filedialog, messagebox

class DatabaseManager:
    def __init__(self):
        self.db_connection = None
        self.db_path = None

    def connect_db(self):
        """Conecta la aplicación a una base de datos SQLite seleccionada por el usuario."""
        db_path = filedialog.askopenfilename(
            title="Selecciona una base de datos existente",
            filetypes=[("SQLite DB", "*.db *.sqlite3")]
        )

        if db_path:
            try:
                self.db_connection = sqlite3.connect(db_path)
                self.db_path = db_path
                messagebox.showinfo("Conexión Exitosa", f"Conectado a la base de datos: {db_path}")
                return True, self.db_connection, db_path
            except Exception as e:
                messagebox.showerror("Error de Conexión", str(e))
                return False, None, None
        return False, None, None

    def disconnect_db(self):
        """Desconecta la aplicación de la base de datos actualmente conectada."""
        if self.db_connection:
            self.db_connection.close()
            self.db_connection = None
            self.db_path = None
            messagebox.showinfo("Desconexión Exitosa", "Se ha desconectado de la base de datos.")
            return True
        return False

    def create_new_db(self):
        """Crea una nueva base de datos SQLite y la conecta."""
        db_path = filedialog.asksaveasfilename(
            title="Crea una nueva base de datos",
            defaultextension=".db",
            filetypes=[("SQLite DB", "*.db")]
        )
        if db_path:
            try:
                self.db_connection = sqlite3.connect(db_path)
                self.db_path = db_path
                messagebox.showinfo("Base de Datos Creada", f"Nueva base de datos creada: {db_path}")
                return True, self.db_connection, db_path
            except Exception as e:
                messagebox.showerror("Error al Crear Base de Datos", str(e))
                return False, None, None
        return False, None, None
