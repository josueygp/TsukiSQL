import sqlite3
from tkinter import filedialog, messagebox

def export_database(db_connection):
    """
    Exporta una base de datos SQLite a un archivo SQL, que contiene la definición de las tablas y los datos.

    Parameters:
    - db_connection: Conexión a la base de datos SQLite.

    Esta función muestra un cuadro de diálogo para que el usuario seleccione la ubicación donde guardar el archivo SQL.
    El archivo contendrá las instrucciones SQL necesarias para recrear las tablas y los datos de la base de datos.
    """
    # Abrir un cuadro de diálogo para seleccionar la ubicación y el nombre del archivo SQL de exportación
    sql_file_path = filedialog.asksaveasfilename(
        title="Exportar Base de Datos",
        defaultextension=".sql",
        filetypes=[("Archivos SQL", "*.sql")]
    )
    
    if sql_file_path:  # Si se seleccionó una ruta para guardar el archivo
        try:
            with db_connection:  # Asegura que la conexión esté activa
                cursor = db_connection.cursor()  # Crea un cursor para ejecutar consultas
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';")  # Consulta las tablas
                tables = [row[0] for row in cursor.fetchall()]  # Extrae los nombres de las tablas

                # Abre el archivo SQL en modo escritura
                with open(sql_file_path, "w") as f:
                    for table in tables:
                        # Escribe la definición de la tabla (DDL) en el archivo SQL
                        cursor.execute(f"SELECT sql FROM sqlite_master WHERE name = '{table}'")
                        ddl = cursor.fetchone()[0]
                        f.write(f"{ddl};\n\n")  # Escribe la instrucción de creación de la tabla
                        
                        # Escribe los datos de la tabla en el archivo SQL
                        cursor.execute(f"SELECT * FROM {table}")
                        rows = cursor.fetchall()
                        if rows:  # Si hay filas en la tabla
                            columns = [description[0] for description in cursor.description]  # Obtiene los nombres de las columnas
                            for row in rows:
                                # Formatea los valores de las filas y genera las sentencias INSERT
                                values = ", ".join(f"'{str(value)}'" if value is not None else "NULL" for value in row)
                                insert_statement = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({values});"
                                f.write(f"{insert_statement}\n")  # Escribe la sentencia INSERT en el archivo
                            f.write("\n")  # Agrega una línea en blanco al final de cada tabla

            # Muestra un mensaje de éxito al usuario
            messagebox.showinfo("Exportación Exitosa", f"La base de datos se ha exportado a: {sql_file_path}")
        
        except Exception as e:
            # Si ocurre un error, muestra un mensaje de error
            messagebox.showerror("Error de Exportación", str(e))
