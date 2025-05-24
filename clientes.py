from tkinter import Tk, Label, Frame, Entry, Button, ttk, messagebox, Scrollbar
from db_soriana import agregar_cliente, eliminar_cliente, actualizar_cliente, ver_clientes, buscar_cliente

def interfaz_clientes():
    ventana = Tk()
    ventana.title("Clientes")
    ventana.geometry("800x600")
    crear_seccion_clientes(ventana, None).pack(expand=True, fill="both")
    ventana.mainloop()

def crear_seccion_clientes(ventana, barra_lateral):
    # Campos alineados con la base de datos
    campos = ["Nombre:", "Apellidos:", "Teléfono:", "Dirección:", "RFC:", "Correo:"]

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

    # Frame para búsqueda
    frame_search = Frame(frame_izquierdo, bg="#E6F0FA")
    frame_search.pack(fill="x", pady=5)
    Label(frame_search, text="Buscar por Teléfono:", bg="#E6F0FA", font=("Arial", 12)).pack(side="left", padx=(10, 2))
    entry_busqueda = Entry(frame_search, font=("Arial", 12), width=20)
    entry_busqueda.pack(side="left", padx=(0, 10))

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

        #TODO: Creamos un frame para la tabla y el scrollbar
    frame_tabla = Frame(frame_izquierdo, bg="#E6F0FA")
    frame_tabla.pack(padx=10,fill="both", expand=True)

    #TODO: Creamos el scrollbar vertical
    scrollbar = Scrollbar(frame_tabla, orient="vertical")
    scrollbar1 = Scrollbar(frame_tabla,orient="horizontal")
    scrollbar.pack(side="right", fill="y")
    scrollbar1.pack(side="bottom", fill="x")
    # Treeview table
    # TODO: Creamos la tabla (Treeview) y la asociamos a los scrollbars     
    tabla = ttk.Treeview(frame_tabla, columns=campos, show="headings", height=15, 
                     yscrollcommand=scrollbar.set, xscrollcommand=scrollbar1.set)
    for col in campos:
        tabla.heading(col, text=col)
        tabla.column(col, width=100)
    tabla.pack(pady=10, fill="both", expand=True)

    #TODO: Configuramos el scrollbar para que controle el desplzamineot vertical de la tabla
    scrollbar.config(command=tabla.yview)
    scrollbar1.config(command=tabla.xview)

    # Variable para almacenar el teléfono original
    telefono_original_var = [None]  # Usamos una lista para que sea mutable

    # Función para cargar datos de la fila seleccionada
    def on_select(event):
        select_item = tabla.selection()
        if select_item:
            values = tabla.item(select_item)['values']
            for i, campo in enumerate(campos):
                entradas[campo].delete(0, 'end')
                entradas[campo].insert(0, values[i])
            telefono_original_var[0] = values[2]  # Guardar el teléfono original (índice 2 es Teléfono:)

    tabla.bind('<<TreeviewSelect>>', on_select)

    # Función para buscar y mostrar resultados
    def buscar_y_mostrar():
        telefono = entry_busqueda.get().strip()
        if not telefono:
            # Si el campo está vacío, mostramos todos los clientes
            ver_clientes(tabla)
            for entrada in entradas.values():
                entrada.delete(0, 'end')  # Limpiar campos
            telefono_original_var[0] = None
            return

        resultado = buscar_cliente(telefono)
        # Limpiar la tabla
        for row in tabla.get_children():
            tabla.delete(row)
        # Limpiar los campos de entrada
        for entrada in entradas.values():
            entrada.delete(0, 'end')
        telefono_original_var[0] = None

        if resultado:
            # Insertar el resultado en la tabla
            tabla.insert("", "end", values=resultado)
            # Llenar los campos de entrada con los datos encontrados
            for i, campo in enumerate(campos):
                entradas[campo].insert(0, resultado[i])
            telefono_original_var[0] = resultado[2]  # Guardar teléfono original
        else:
            messagebox.showwarning("No encontrado", f"No se encontró un cliente con el teléfono {telefono}")

    # Botón de búsqueda
    Button(frame_search, text="Buscar", font=("Arial", 10), bg="#2196F3", fg="white",
           command=buscar_y_mostrar).pack(side="left", pady=5, padx=5)

    def agregar():
        nombre = entradas["Nombre:"].get().strip()
        apellidos = entradas["Apellidos:"].get().strip()
        telefono = entradas["Teléfono:"].get().strip()
        direccion = entradas["Dirección:"].get().strip()
        rfc = entradas["RFC:"].get().strip()
        correo = entradas["Correo:"].get().strip()

        if not all([nombre, apellidos, telefono, direccion,correo]):
            messagebox.showerror("Error", "Todos los campos excepto rfc son obligatorios")
            return

        agregar_cliente(nombre, apellidos, telefono, direccion, rfc, correo)
        ver_clientes(tabla)
        limpiar_campos()

    def eliminar():
        telefono = entradas["Teléfono:"].get().strip()
        if not telefono:
            messagebox.showerror("Error", "El campo Teléfono es obligatorio")
            return
        eliminar_cliente(telefono)
        ver_clientes(tabla)
        limpiar_campos()

    def limpiar_campos():
        for entrada in entradas.values():
            entrada.delete(0, 'end')
        entry_busqueda.delete(0, 'end')  # Limpiar campo de búsqueda
        telefono_original_var[0] = None  # Resetear el teléfono original

    def actualizar_datos():
        nombre = entradas["Nombre:"].get().strip()
        apellidos = entradas["Apellidos:"].get().strip()
        telefono = entradas["Teléfono:"].get().strip()
        direccion = entradas["Dirección:"].get().strip()
        rfc = entradas["RFC:"].get().strip()
        correo = entradas["Correo:"].get().strip()

        if not all([nombre, apellidos, telefono, direccion, correo]):
            messagebox.showerror("Error", "Todos los campos excepto rfc son obligatorios")
            return

        if not telefono_original_var[0]:
            messagebox.showerror("Error", "Seleccione un cliente para actualizar")
            return

        actualizar_cliente(telefono_original_var[0], nombre, apellidos, telefono, direccion, rfc, correo)
        ver_clientes(tabla)
        limpiar_campos()

    # Botones
    Button(frame_derecho, text="Agregar", font=("Arial", 10), bg="#4CAF50", fg="white", width=15,
           command=agregar).pack(pady=5)
    Button(frame_derecho, text="Eliminar", font=("Arial", 10), bg="#F44336", fg="white", width=15,
           command=eliminar).pack(pady=5)
    Button(frame_derecho, text="Actualizar", font=("Arial", 10), bg="#2196F3", fg="white", width=15,
           command=actualizar_datos).pack(pady=5)
    Button(frame_derecho, text="Limpiar", font=("Arial", 10), bg="#FFC107", fg="black", width=15,
           command=limpiar_campos).pack(pady=5)

    # Cargar todos los clientes al iniciar
    ver_clientes(tabla)

    return frame_principal

if __name__ == "__main__":
    interfaz_clientes()