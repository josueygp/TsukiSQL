import sqlite3
from tkinter import filedialog, messagebox

def export_database(db_connection):
    """
    Exporta una base de datos SQLite a un archivo SQL, que contiene la definición de las tablas y los datos.
    
    Parameters:
    - db_connection: Conexión a la base de datos SQLite.
    """
    sql_file_path = filedialog.asksaveasfilename(
        title="Exportar Base de Datos",
        defaultextension=".sql",
        filetypes=[("Archivos SQL", "*.sql")]
    )
    
    if sql_file_path:  # Si se seleccionó una ruta para guardar el archivo
        try:
            with db_connection:
                cursor = db_connection.cursor()
                
                # Configura la conexión para manejar caracteres UTF-8
                cursor.execute("PRAGMA encoding='UTF-8';")
                
                # Consulta las tablas excluyendo sqlite_sequence
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';")
                tables = [row[0] for row in cursor.fetchall()]
                
                # Abre el archivo en modo escritura con codificación UTF-8
                with open(sql_file_path, "w", encoding='utf-8') as f:
                    # Escribe un encabezado para establecer la codificación
                    f.write("-- coding: utf-8\n")
                    f.write("PRAGMA encoding='UTF-8';\n\n")
                    
                    for table in tables:
                        # Obtiene y escribe la definición de la tabla
                        cursor.execute(f"SELECT sql FROM sqlite_master WHERE name = ?", (table,))
                        ddl = cursor.fetchone()[0]
                        f.write(f"{ddl};\n\n") 
                        
                        # Obtiene y escribe los datos
                        cursor.execute(f"SELECT * FROM {table}")
                        rows = cursor.fetchall()
                        
                        if rows:
                            columns = [description[0] for description in cursor.description]
                            
                            for row in rows:
                                # Maneja valores especiales y escapa caracteres
                                values = []
                                for value in row:
                                    if value is None:
                                        values.append("NULL")
                                    elif isinstance(value, (int, float)):
                                        values.append(str(value))
                                    else:
                                        # Escapa comillas simples y caracteres especiales
                                        escaped_value = str(value).replace("'", "''")
                                        values.append(f"'{escaped_value}'")
                                
                                insert_statement = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(values)});"
                                f.write(f"{insert_statement}\n")
                            
                            f.write("\n")  # Línea en blanco entre tablas
                
                messagebox.showinfo(
                    "Exportación Exitosa",
                    f"La base de datos se ha exportado correctamente a:\n{sql_file_path}"
                )
                
        except Exception as e:
            messagebox.showerror(
                "Error de Exportación",
                f"Error al exportar la base de datos:\n{str(e)}"
            )