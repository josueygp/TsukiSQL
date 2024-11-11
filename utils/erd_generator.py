import sqlite3
from graphviz import Digraph
from tkinter import filedialog

def generate_erd_dialog(db_connection, generate_erd_func):
    """
    Muestra un cuadro de diálogo para seleccionar el lugar donde guardar el diagrama de relaciones de entidades (ERD).
    
    Parameters:
    - db_connection: Conexión a la base de datos SQLite.
    - generate_erd_func: Función para generar el diagrama ERD.

    Esta función solicita al usuario una ruta para guardar el archivo generado, y si el usuario selecciona un archivo,
    llama a la función `generate_erd_func` para crear y guardar el diagrama.
    """
    # Abrir un cuadro de diálogo para seleccionar dónde guardar el ERD
    save_path = filedialog.asksaveasfilename(
        title="Guardar ERD",
        defaultextension=".png",
        filetypes=[("PNG Files", "*.png"), ("PDF Files", "*.pdf")]
    )

    if save_path:
        file_format = 'png' if save_path.endswith('.png') else 'pdf'  # Establece el formato del archivo
        generate_erd_func(db_connection, save_path, file_format)  # Genera y guarda el ERD

def generate_erd(db_connection, save_path, file_format='png'):
    """
    Genera un diagrama de relaciones de entidades (ERD) a partir de la base de datos y lo guarda en un archivo.
    
    Parameters:
    - db_connection: Conexión a la base de datos SQLite.
    - save_path: Ruta donde se guardará el diagrama generado.
    - file_format: Formato del archivo de salida (por defecto 'png').

    La función genera un diagrama utilizando Graphviz, incluyendo tablas, columnas y claves foráneas,
    y lo guarda en el archivo especificado en el formato seleccionado (PNG o PDF).
    """
    cursor = db_connection.cursor()  # Crea un cursor para ejecutar las consultas
    
    # Crear el gráfico de ERD
    dot = Digraph(comment='ERD Diagram')  # Inicializa un nuevo gráfico de tipo Digraph
    dot.attr(rankdir='BT')  # Cambia la dirección del diagrama para más claridad (de abajo hacia arriba)

    # Obtener todas las tablas en la base de datos
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Procesar cada tabla para crear nodos
    for (table_name,) in tables:
        cursor.execute(f"PRAGMA table_info({table_name});")  # Consulta las columnas de la tabla
        columns = cursor.fetchall()

        # Crear una etiqueta con el nombre de la tabla y sus columnas
        table_label = f"{table_name}|"
        for column in columns:
            column_name = column[1]
            column_type = column[2]
            is_primary = column[5]  # Verifica si la columna es clave primaria
            pk_label = "PK" if is_primary else ""  # Marca la columna como PK si es clave primaria
            table_label += f"{column_name} : {column_type} {pk_label}\\l"  # Agrega columna al texto de la tabla

        # Crear un nodo de la tabla con el nombre y columnas formateadas
        dot.node(table_name, label=f"{{{table_label}}}", shape='record')  # Define el nodo como un 'record' (tipo tabla)

    # Procesar claves foráneas para crear relaciones entre tablas
    for (table_name,) in tables:
        cursor.execute(f"PRAGMA foreign_key_list({table_name});")  # Consulta las claves foráneas de la tabla
        foreign_keys = cursor.fetchall()
        
        # Crear las conexiones de claves foráneas entre las tablas
        for fk in foreign_keys:
            from_table = table_name
            from_column = fk[3]  # Columna de la clave foránea
            to_table = fk[2]  # Tabla de la clave foránea
            to_column = fk[4]  # Columna referenciada por la clave foránea
            dot.edge(f"{from_table}:{from_column}", f"{to_table}:{to_column}", arrowhead='normal', color='blue', label='FK')  # Relación de FK

    # Guardar el diagrama generado en el archivo especificado
    dot.render(save_path, format=file_format, cleanup=True)  # Guarda el diagrama en el formato elegido

if __name__ == "__main__":
    db_path = "ruta/a/tu/base_de_datos.db"  # Cambia esta ruta a tu base de datos
    save_path = "erd_diagram"  # Ruta de salida predeterminada para guardar el diagrama
    
    # Conectar a la base de datos
    connection = sqlite3.connect(db_path)
    generate_erd(connection, save_path)  # Generar y guardar el ERD
    connection.close()  # Cierra la conexión a la base de datos
