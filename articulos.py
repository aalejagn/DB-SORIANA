from tkinter import Tk, Label, Frame, Entry, Button, ttk, messagebox,Scrollbar
from db_soriana import agregar_articulo, ver_articulos, actualizar_articulo, buscar_articulo, eliminar_articulos, buscar_catalogo, buscar_proveedor, buscar_unidad,registrar_venta
from datetime import datetime

def interfaz_articulos():
    ventana = Tk()
    ventana.title("Gestión de Artículos")
    ventana.geometry("1000x600")  # Increased width to accommodate more columns
    crear_seccion_articulos(ventana, None).pack(expand=True, fill="both")
    ventana.mainloop()

def crear_seccion_articulos(ventana, barra_lateral):
    # Define fields based on articulos table schema
    campos = ["Código:", "Nombre:", "Precio:", "Costo:", "Existencia:", "Descripción:", 
              "Fecha Caducidad:", "Código Categoría:", "ID Proveedor:", "ID Unidad:"]

    if barra_lateral:
        for widget in ventana.winfo_children():
            if widget != barra_lateral:
                widget.destroy()

    frame_principal = Frame(ventana, bg="#E6F0FA")
    frame_principal.pack(expand=True, fill="both")

    frame_centrado = Frame(frame_principal, bg="#E6F0FA")
    frame_centrado.pack(expand=True, fill="both", padx=10, pady=10)

    frame_derecho = Frame(frame_centrado, bg="#E6F0FA", width=150)
    frame_derecho.pack(side="right", fill="y", padx=10)

    frame_izquierdo = Frame(frame_centrado, bg="#E6F0FA")
    frame_izquierdo.pack(side="left", expand=True, fill="both")

    Label(frame_izquierdo, text="Artículos", font=("Arial", 16, "bold"), bg="#E6F0FA").pack(pady=10)

    # Search frame
    frame_search = Frame(frame_izquierdo, bg="#E6F0FA")
    frame_search.pack(fill="x", pady=5)
    Label(frame_search, text="Buscar por Código:", bg="#E6F0FA", font=("Arial", 12)).pack(side="left", padx=(10, 2))
    entry_busqueda = Entry(frame_search, font=("Arial", 12), width=20)
    entry_busqueda.pack(side="left", padx=(0, 10))

    # Entries frame, split into two columns
    frame_entradas = Frame(frame_izquierdo, bg="#E6F0FA")
    frame_entradas.pack(fill="x", pady=5)

    # Left column (first 5 fields)
    frame_entradas_izq = Frame(frame_entradas, bg="#E6F0FA")
    frame_entradas_izq.pack(side="left", padx=10)

    # Right column (remaining fields)
    frame_entradas_der = Frame(frame_entradas, bg="#E6F0FA")
    frame_entradas_der.pack(side="left", padx=10)

    entradas = {}
    # Left column entries
    for i, campo in enumerate(campos[:5]):
        Label(frame_entradas_izq, text=campo, bg="#E6F0FA", font=("Arial", 12)).grid(row=i, column=0, padx=(10, 2), pady=5, sticky="e")
        entrada = Entry(frame_entradas_izq, font=("Arial", 12))
        entrada.grid(row=i, column=1, padx=(0, 10), pady=5, sticky="w")
        entradas[campo] = entrada

    # Right column entries
    for i, campo in enumerate(campos[5:]):
        Label(frame_entradas_der, text=campo, bg="#E6F0FA", font=("Arial", 12)).grid(row=i, column=0, padx=(10, 2), pady=5, sticky="e")
        entrada = Entry(frame_entradas_der, font=("Arial", 12))
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
    codigo_original_var = [None]  # Store original codigo for updates

    def on_select(event):
        select_item = tabla.selection()
        if select_item:
            values = tabla.item(select_item)['values']
            for i, campo in enumerate(campos):
                entradas[campo].delete(0, 'end')
                entradas[campo].insert(0, values[i])
            codigo_original_var[0] = values[0]

    tabla.bind('<<TreeviewSelect>>', on_select)

    # TODO: Agregar validación de fecha para formato YYYY-MM-DD
    def validate_date(date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def buscar_y_mostrar(event=None):  # TODO: Añadir un event como NONE oara el binding
        codigo = entry_busqueda.get().strip()
        if not codigo:
            ver_articulos(tabla)
            for entrada in entradas.values():
                entrada.delete(0, 'end')
            codigo_original_var[0] = None
            return

        resultado = buscar_articulo(codigo)
        for row in tabla.get_children():
            tabla.delete(row)
        for entrada in entradas.values():
            entrada.delete(0, 'end')
        codigo_original_var[0] = None

        if resultado:
            tabla.insert("", "end", values=resultado)
            for i, campo in enumerate(campos):
                entradas[campo].insert(0, resultado[i])
            codigo_original_var[0] = resultado[0]
            # TODO: MAnejo de registros del articulo simula una venta
            if entradas["Existencia:"].get():
                try:
                    existencia = int(entradas["Existencia:"].get())
                    if existencia > 0:
                        entradas["Existencia:"].delete(0, 'end')
                        entradas["Existencia:"].insert(0, str(existencia - 1))
                        actualizar_articulo(
                            codigo_original_var[0],
                            entradas["Nombre:"].get(),  # Corregido espacio extra
                            float(entradas["Precio:"].get()),
                            float(entradas["Costo:"].get()),
                            existencia - 1,
                            entradas["Descripción:"].get(),  # Corregido "Descripcióo"
                            entradas["Fecha Caducidad:"].get(),
                            entradas["Código Categoría:"].get(),
                            int(entradas["ID Proveedor:"].get()),
                            int(entradas["ID Unidad:"].get())
                        )
                        registrar_venta(codigo)
                        messagebox.showinfo("Éxito", f"Artículo {codigo} registrado correctamente")  # Corregido "resigtrado"
                        # TODO: Agregar registro de venta en tabla ventas
                    else:
                        messagebox.showwarning("Sin stock", "No hay existencia del producto")  # Corregido "exitencia"
                except ValueError:
                    messagebox.showerror("Error", "Existencia debe ser numérica")  # Corregido "numerica"
        else:
            response = messagebox.askyesno("No encontrado", f"No se encontró un artículo con el código {codigo}. ¿Desea agregarlo?")
            if response:
                entradas["Código:"].insert(0, codigo)
                entry_busqueda.delete(0, 'end')
            # TODO: Agregar sonido para confirmar escaneo exitoso

    # TODO: Vincular ENTER al campo de busqueda
    entry_busqueda.bind('<Return>', buscar_y_mostrar)
    # TODO: Poner el foco en el campo de busqueda
    entry_busqueda.focus_set()

    Button(frame_search, text="Buscar", font=("Arial", 10), bg="#2196F3", fg="white",
           command=buscar_y_mostrar).pack(side="left", pady=5, padx=5)

    def agregar():
        codigo = entradas["Código:"].get().strip()
        nombre = entradas["Nombre:"].get().strip()
        precio = entradas["Precio:"].get().strip()
        costo = entradas["Costo:"].get().strip()
        existencia = entradas["Existencia:"].get().strip()
        descripcion = entradas["Descripción:"].get().strip()
        fecha_caducidad = entradas["Fecha Caducidad:"].get().strip()
        categoria_codigo = entradas["Código Categoría:"].get().strip()
        id_proveedor = entradas["ID Proveedor:"].get().strip()
        id_unidad = entradas["ID Unidad:"].get().strip()

        if not all([codigo, nombre, precio, costo, existencia, descripcion, fecha_caducidad, categoria_codigo, id_proveedor, id_unidad]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        # TODO: Validar formato de fecha antes de agregar
        if not validate_date(fecha_caducidad):
            messagebox.showerror("Error", "Fecha de caducidad debe estar en formato YYYY-MM-DD")
            return

        try:
            precio = float(precio)
            costo = float(costo)
            existencia = int(existencia)
            id_proveedor = int(id_proveedor)
            id_unidad = int(id_unidad)
            # TODO: Validar claaves foranesa
            if not (buscar_catalogo(categoria_codigo) and buscar_proveedor(id_proveedor) and buscar_unidad(id_unidad)):
                messagebox.showerror("Error", "Código de categoría, ID de proveedor o ID de unidad no válidos")  # Corregido mensaje
                return
        except ValueError:
            messagebox.showerror("Error", "Precio, Costo, Existencia, ID Proveedor e ID Unidad deben ser valores numéricos")
            return

        agregar_articulo(codigo, nombre, precio, costo, existencia, descripcion, fecha_caducidad, categoria_codigo, id_proveedor, id_unidad)
        ver_articulos(tabla)
        limpiar_campos()

    def eliminar():
        codigo = entradas["Código:"].get().strip()
        if not codigo:
            messagebox.showerror("Error", "El campo Código es obligatorio")
            return
        eliminar_articulos(codigo)
        ver_articulos(tabla)
        limpiar_campos()

    # TODO: Actualializar datos
    def actualizar_datos():
        codigo = entradas["Código:"].get().strip()
        nombre = entradas["Nombre:"].get().strip()
        precio = entradas["Precio:"].get().strip()
        costo = entradas["Costo:"].get().strip()
        existencia = entradas["Existencia:"].get().strip()
        descripcion = entradas["Descripción:"].get().strip()
        fecha_caducidad = entradas["Fecha Caducidad:"].get().strip()
        categoria_codigo = entradas["Código Categoría:"].get().strip()
        id_proveedor = entradas["ID Proveedor:"].get().strip()
        id_unidad = entradas["ID Unidad:"].get().strip()

        if not all([codigo, nombre, precio, costo, existencia, descripcion, fecha_caducidad, categoria_codigo, id_proveedor, id_unidad]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        if not codigo_original_var[0]:
            messagebox.showerror("Error", "Seleccione un artículo para actualizar")
            return

        # TODO: Validar formato de fecha antes de actualizar
        if not validate_date(fecha_caducidad):
            messagebox.showerror("Error", "Fecha de caducidad debe estar en formato YYYY-MM-DD")
            return

        try:
            precio = float(precio)
            costo = float(costo)
            existencia = int(existencia)
            id_proveedor = int(id_proveedor)
            id_unidad = int(id_unidad)
            # TODO: Validar claves foráneas antes de actualizar
            if not (buscar_catalogo(categoria_codigo) and buscar_proveedor(id_proveedor) and buscar_unidad(id_unidad)):
                messagebox.showerror("Error", "Código de categoría, ID de proveedor o ID de unidad no válidos")
                return
        except ValueError:
            messagebox.showerror("Error", "Precio, Costo, Existencia, ID Proveedor e ID Unidad deben ser valores numéricos")
            return

        actualizar_articulo(
            codigo_original_var[0],  # Usar código original para WHERE
            nombre, precio, costo, existencia, descripcion, fecha_caducidad, categoria_codigo, id_proveedor, id_unidad
        )
        ver_articulos(tabla)
        limpiar_campos()

    def limpiar_campos():
        for entrada in entradas.values():
            entrada.delete(0, 'end')
        entry_busqueda.delete(0, 'end')
        codigo_original_var[0] = None

    # Buttons for actions
    Button(frame_derecho, text="Agregar", font=("Arial", 10), bg="#4CAF50", fg="white", width=15,
           command=agregar).pack(pady=5)
    Button(frame_derecho, text="Eliminar", font=("Arial", 10), bg="#F44336", fg="white", width=15,
           command=eliminar).pack(pady=5)
    Button(frame_derecho, text="Actualizar", font=("Arial", 10), bg="#2196F3", fg="white", width=15,
           command=actualizar_datos).pack(pady=5)
    Button(frame_derecho, text="Limpiar", font=("Arial", 10), bg="#FFC107", fg="black", width=15,
           command=limpiar_campos).pack(pady=5)

    ver_articulos(tabla)
    # TODO: Poner el foco en el campo de busqueda
    entry_busqueda.focus_set()

    return frame_principal

if __name__ == "__main__":
    interfaz_articulos()