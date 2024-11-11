import tkinter as tk

def update_tools_menu_state(menu, connected):
    """
    Actualiza el estado de los elementos del menú 'Herramientas' dependiendo de la conexión a la base de datos.

    Parameters:
    - menu: Menú que contiene las opciones a actualizar.
    - connected: Estado de la conexión a la base de datos (True si está conectado, False si no lo está).

    Esta función habilita o deshabilita las opciones del menú "Generar ERD" y "Exportar Base de Datos"
    dependiendo de si la conexión a la base de datos está activa o no.
    """
    state = "normal" if connected else "disabled"  # Determina el estado basado en la conexión
    menu.tools_menu.entryconfig("Generar ERD", state=state)  # Actualiza el estado de "Generar ERD"
    menu.tools_menu.entryconfig("Exportar Base de Datos", state=state)  # Actualiza el estado de "Exportar Base de Datos"

def update_db_label(db_label, db_path):
    """
    Actualiza la etiqueta que muestra el estado de la conexión a la base de datos.

    Parameters:
    - db_label: Etiqueta de la interfaz gráfica que muestra el estado.
    - db_path: Ruta de la base de datos conectada (vacío si no hay base de datos conectada).

    Si hay una base de datos conectada, la etiqueta mostrará la ruta; si no, mostrará "No hay base de datos conectada".
    """
    if db_path:
        db_label.config(text=f"Conectado a: {db_path}")  # Muestra la ruta de la base de datos conectada
    else:
        db_label.config(text="No hay base de datos conectada")  # Muestra mensaje si no hay base de datos

def update_tables_list(db_connection, tables_listbox):
    """
    Actualiza la lista de tablas en la interfaz gráfica.

    Parameters:
    - db_connection: Conexión a la base de datos SQLite.
    - tables_listbox: Lista de tablas en la interfaz gráfica.

    Obtiene la lista de tablas de la base de datos y las muestra en el `tables_listbox`.
    Si no hay conexión a la base de datos, no hace nada.
    """
    if not db_connection:
        return  # Si no hay conexión, no se actualiza la lista
    cursor = db_connection.cursor()  # Crea un cursor para interactuar con la base de datos
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")  # Consulta las tablas en la base de datos
    tables = cursor.fetchall()  # Obtiene todas las tablas
    tables_listbox.delete(0, tk.END)  # Borra cualquier elemento previo en la lista de tablas
    for table in tables:
        tables_listbox.insert(tk.END, table[0])  # Inserta cada tabla en la lista
