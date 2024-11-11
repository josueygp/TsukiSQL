import tkinter as tk
from tkinter import ttk
import webbrowser

class AboutWindow:
    """
    Clase que crea y gestiona la ventana 'Acerca de' de la aplicación TsukiSQL.
    Muestra información sobre la aplicación, el desarrollador y enlaces relevantes.
    """

    def __init__(self, parent):
        """
        Inicializa la ventana 'Acerca de'.

        Args:
            parent: Ventana padre de la aplicación
        """
        # Crear ventana de diálogo modal
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Acerca de TsukiSQL")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)  # Deshabilitar redimensionamiento
        
        # Configurar como ventana modal
        self.dialog.transient(parent)        # Hacer la ventana dependiente del padre
        self.dialog.grab_set()               # Hacer la ventana modal
        
        # Centrar la ventana en la pantalla
        self.center_window()
        
        # Crear los widgets de la ventana
        self.create_widgets()

    def center_window(self):
        """
        Centra la ventana en la pantalla.
        Calcula la posición adecuada basada en las dimensiones de la pantalla.
        """
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        """
        Crea y configura todos los widgets de la ventana 'Acerca de'.
        Incluye título, versión, información del desarrollador, propósito y enlaces.
        """
        # Frame principal con padding
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título de la aplicación
        title_label = ttk.Label(
            main_frame,
            text="TsukiSQL",
            font=('Helvetica', 16, 'bold')
        )
        title_label.pack(pady=(0, 10))

        # Etiqueta de versión
        version_label = ttk.Label(
            main_frame,
            text="Versión 1.0.0",
            font=('Helvetica', 10)
        )
        version_label.pack()

        # Línea separadora horizontal
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)

        # Información del desarrollador
        dev_label = ttk.Label(
            main_frame,
            text="Desarrollado por:\nJosue Yael Guerrero Priego",
            justify=tk.CENTER
        )
        dev_label.pack(pady=5)

        # Descripción del propósito de la aplicación
        purpose_label = ttk.Label(
            main_frame,
            text="Propósito:\nHerramienta de gestión y consulta de bases de datos SQLite\n"
                 "con interfaz gráfica intuitiva para facilitar el trabajo\n"
                 "con bases de datos relacionales.",
            justify=tk.CENTER,
            wraplength=350
        )
        purpose_label.pack(pady=10)

        # Enlace al repositorio de GitHub
        github_link = ttk.Label(
            main_frame,
            text="Visitar repositorio en GitHub",
            foreground='blue',
            cursor='hand2'  # Cambiar cursor al pasar sobre el enlace
        )
        github_link.pack(pady=5)
        # Vincular clic al enlace de GitHub
        github_link.bind(
            '<Button-1>',
            lambda e: webbrowser.open_new('https://github.com/josueygp/TsukiSQL')
        )

        # Botón para cerrar la ventana
        close_button = ttk.Button(
            main_frame,
            text="Cerrar",
            command=self.dialog.destroy
        )
        close_button.pack(pady=(20, 0))