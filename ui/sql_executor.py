import sqlite3
import tkinter as tk
from tkinter import messagebox

def on_table_select(event, tables_listbox, sql_text, execute_sql, ui_builder):
    """
    Maneja la selección de una tabla desde la lista de tablas para ejecutar una consulta SELECT *.

    Parameters:
    - event: El evento de selección de la tabla.
    - tables_listbox: Lista de tablas disponibles.
    - sql_text: Área de texto para la consulta SQL.
    - execute_sql: Función para ejecutar la consulta SQL.
    - ui_builder: Objeto encargado de la interfaz de usuario para mostrar mensajes.

    Modifica la consulta SQL para obtener todos los registros de la tabla seleccionada.
    Utiliza la consola para mostrar la consulta que se está ejecutando.
    """
    selected_index = tables_listbox.curselection()  # Obtiene la tabla seleccionada
    if selected_index:
        table_name = tables_listbox.get(selected_index)  # Nombre de la tabla seleccionada
        sql_command = f"SELECT * FROM {table_name}"  # Comando SQL para seleccionar todos los registros de la tabla
        ui_builder.append_to_console(f"Executing: {sql_command}", 'info')  # Muestra el comando en la consola
        execute_sql(sql_command)  # Ejecuta la consulta SQL

def execute_sql(db_connection, sql_text, results_table, update_tables_list, ui_builder, custom_sql=None):
    """
    Ejecuta una consulta SQL en la base de datos y maneja el resultado.

    Parameters:
    - db_connection: Conexión a la base de datos SQLite.
    - sql_text: Área de texto donde se encuentra la consulta SQL.
    - results_table: Tabla en la interfaz para mostrar los resultados.
    - update_tables_list: Función para actualizar la lista de tablas disponibles.
    - ui_builder: Objeto para mostrar mensajes en la consola de la interfaz.
    - custom_sql (opcional): Consulta SQL personalizada para ejecutar.

    Esta función ejecuta el SQL ingresado, maneja la ejecución de múltiples comandos SQL,
    muestra los resultados si es una consulta SELECT, o un mensaje de éxito si no lo es.
    """
    sql_command = custom_sql if custom_sql else sql_text.get("1.0", tk.END).strip()  # Obtiene el SQL, o usa el proporcionado
    
    # Verifica que el SQL no esté vacío y que haya conexión a la base de datos
    if not sql_command or not db_connection:
        error_msg = "Please connect to a database and enter an SQL command."
        ui_builder.append_to_console(error_msg, 'error')  # Muestra mensaje de error en la consola
        messagebox.showwarning("Warning", error_msg)  # Muestra advertencia al usuario
        return
        
    try:
        cursor = db_connection.cursor()  # Crea un cursor para ejecutar la consulta
        
        # Si hay múltiples comandos SQL, usa executescript()
        if ";" in sql_command:
            cursor.executescript(sql_command)
        else:
            cursor.execute(sql_command)  # Ejecuta el comando SQL
        
        db_connection.commit()  # Confirma los cambios en la base de datos
        
        if sql_command.lower().startswith("select"):  # Si es una consulta SELECT
            rows = cursor.fetchall()  # Obtiene todas las filas del resultado
            display_results(rows, cursor.description, results_table)  # Muestra los resultados en la interfaz
            ui_builder.append_to_console(f" {sql_command}. Query executed successfully. {len(rows)} rows returned.", 'success')
        else:
            success_msg = "SQL command executed successfully."
            ui_builder.append_to_console(success_msg, 'success')  # Muestra el mensaje de éxito
            messagebox.showinfo("Success", success_msg)  # Muestra información de éxito al usuario
            update_tables_list(db_connection)  # Actualiza la lista de tablas disponibles
            
    except sqlite3.Error as e:
        error_msg = str(e)  # En caso de error en SQL, se captura y muestra el mensaje
        ui_builder.append_to_console(f"Error: {error_msg}", 'error')  # Muestra el error en la consola
        messagebox.showerror("SQL Error", error_msg)  # Muestra el mensaje de error al usuario

def display_results(rows, description, results_table):
    """
    Muestra los resultados de una consulta SELECT en la interfaz gráfica.

    Parameters:
    - rows: Filas obtenidas de la consulta SQL.
    - description: Descripción de las columnas de la tabla.
    - results_table: Tabla en la interfaz donde se mostrarán los resultados.

    Esta función configura las columnas de la tabla de resultados y luego inserta
    los datos de las filas obtenidas.
    """
    for row in results_table.get_children():  # Elimina cualquier dato previo en la tabla
        results_table.delete(row)
    columns = [desc[0] for desc in description]  # Extrae los nombres de las columnas
    results_table.config(columns=columns)  # Configura las columnas en la tabla
    for col in columns:
        results_table.heading(col, text=col)  # Define los encabezados de las columnas
    for row in rows:
        results_table.insert("", tk.END, values=row)  # Inserta las filas de resultados
