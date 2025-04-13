from tkinter import Tk, Label, Frame, Entry, Button, ttk, messagebox

"""
Interfaz para la gestión de clientes
"""
def interfaz_clientes():
    ventana = Tk()
    ventana.title("Clientes")
    ventana.geometry("800x600")
    crear_seccion_clientes(ventana, None).pack(expand=True, fill="both")
    ventana.mainloop()

"""
Creación de la sección de clientes
"""
def crear_seccion_clientes(ventana, barra_lateral):
    campos = ["Telefono:", "Nombre:", "Dirección:", "RFC:", "Correo:"]

    # Limpiamos los widgets existentes, excepto la barra lateral
    if barra_lateral:
        for widget in ventana.winfo_children():
            if widget != barra_lateral:
                widget.destroy()

    frame_principal = Frame(ventana, bg="#E6F0FA")
    frame_principal.pack(expand=True, fill="both")

    # Frame intermedio para dividir en dos: izquierda (entradas y tabla) y derecha (botones)
    frame_centrado = Frame(frame_principal, bg="#E6F0FA")
    frame_centrado.pack(expand=True, fill="both", padx=10, pady=10)

    # Frame lateral derecho para botones
    frame_derecho = Frame(frame_centrado, bg="#E6F0FA", width=150)
    frame_derecho.pack(side="right", fill="y", padx=10)

    # Frame izquierdo para entradas y tabla
    frame_izquierdo = Frame(frame_centrado, bg="#E6F0FA")
    frame_izquierdo.pack(side="left", expand=True, fill="both")

    # Título de la sección
    Label(frame_izquierdo, text="Clientes", font=("Arial", 16, "bold"), bg="#E6F0FA").pack(pady=10)

    # Frame para los campos de entrada
    frame_entradas = Frame(frame_izquierdo, bg="#E6F0FA")
    frame_entradas.pack(fill="x", pady=5)

    # Creamos las entradas
    entradas = {}
    for i, campo in enumerate(campos):
        Label(frame_entradas, text=campo, bg="#E6F0FA", font=("Arial", 12)).grid(row=i, column=0, padx=(10, 2), pady=5, sticky="e")
        entrada = Entry(frame_entradas, font=("Arial", 12))
        entrada.grid(row=i, column=1, padx=(0, 10), pady=5, sticky="w")
        entradas[campo] = entrada

    # Creación de tabla (más grande)
    tabla = ttk.Treeview(frame_izquierdo, columns=campos, show="headings", height=15)  # Aumentamos altura
    for col in campos:
        tabla.heading(col, text=col)
        tabla.column(col, width=150)  # Aumentamos el ancho de las columnas
    tabla.pack(pady=10, fill="both", expand=True)

    # Botones (en el frame derecho, apilados verticalmente)
    Button(frame_derecho, text="Agregar", font=("Arial", 10), bg="#4CAF50", fg="white", width=15,
           command=lambda: messagebox.showwarning("Advertencia", "Función no implementada")).pack(pady=5)
    Button(frame_derecho, text="Eliminar", font=("Arial", 10), bg="#F44336", fg="white", width=15,
           command=lambda: messagebox.showwarning("Advertencia", "Función no implementada")).pack(pady=5)
    Button(frame_derecho, text="Actualizar", font=("Arial", 10), bg="#2196F3", fg="white", width=15,
           command=lambda: messagebox.showwarning("Advertencia", "Función no implementada")).pack(pady=5)
    Button(frame_derecho, text="Limpiar", font=("Arial", 10), bg="#FFC107", fg="black", width=15).pack(pady=5)

    return frame_principal

if __name__ == "__main__":
    interfaz_clientes()