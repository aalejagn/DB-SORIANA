from tkinter import Tk, Label, Frame, Entry, Button, ttk, messagebox, Scrollbar
from db_soriana import agregar_articulo, ver_articulos, actualizar_articulo, buscar_articulo, eliminar_articulos, buscar_catalogo, buscar_proveedor, buscar_unidad, buscar_articulo_por_nombre
from datetime import datetime

def interfaz_articulos():
    ventana = Tk()
    ventana.title("Gestión de Artículos")
    ventana.geometry("1000x600")
    crear_seccion_articulos(ventana, None).pack(expand=True, fill="both")
    ventana.mainloop()

def crear_seccion_articulos(ventana, barra_lateral, codigo_prellenado=None):
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

    frame_search = Frame(frame_izquierdo, bg="#E6F0FA")
    frame_search.pack(fill="x", pady=5)
    Label(frame_search, text="Buscar por:", bg="#E6F0FA", font=("Arial", 12)).pack(side="left", padx=(10, 2))
    combo_busqueda = ttk.Combobox(frame_search, values=["Código", "Nombre"], font=("Arial", 12), state="readonly", width=10)
    combo_busqueda.pack(side="left", padx=(0, 5))
    combo_busqueda.set("Código")
    entry_busqueda = Entry(frame_search, font=("Arial", 12), width=20)
    entry_busqueda.pack(side="left", padx=(0, 10))

    frame_entradas = Frame(frame_izquierdo, bg="#E6F0FA")
    frame_entradas.pack(fill="x", pady=5)

    frame_entradas_izq = Frame(frame_entradas, bg="#E6F0FA")
    frame_entradas_izq.pack(side="left", padx=10)

    frame_entradas_der = Frame(frame_entradas, bg="#E6F0FA")
    frame_entradas_der.pack(side="left", padx=10)

    entradas = {}
    for i, campo in enumerate(campos[:5]):
        Label(frame_entradas_izq, text=campo, bg="#E6F0FA", font=("Arial", 12)).grid(row=i, column=0, padx=(10, 2), pady=5, sticky="e")
        entrada = Entry(frame_entradas_izq, font=("Arial", 12))
        entrada.grid(row=i, column=1, padx=(0, 10), pady=5, sticky="w")
        entradas[campo] = entrada

    for i, campo in enumerate(campos[5:]):
        Label(frame_entradas_der, text=campo, bg="#E6F0FA", font=("Arial", 12)).grid(row=i, column=0, padx=(10, 2), pady=5, sticky="e")
        entrada = Entry(frame_entradas_der, font=("Arial", 12))
        entrada.grid(row=i, column=1, padx=(0, 10), pady=5, sticky="w")
        entradas[campo] = entrada

    if codigo_prellenado:
        entradas["Código:"].insert(0, codigo_prellenado)

    frame_tabla = Frame(frame_izquierdo, bg="#E6F0FA")
    frame_tabla.pack(padx=10, fill="both", expand=True)

    scrollbar = Scrollbar(frame_tabla, orient="vertical")
    scrollbar1 = Scrollbar(frame_tabla, orient="horizontal")
    scrollbar.pack(side="right", fill="y")
    scrollbar1.pack(side="bottom", fill="x")

    tabla = ttk.Treeview(frame_tabla, columns=campos, show="headings", height=15, 
                         yscrollcommand=scrollbar.set, xscrollcommand=scrollbar1.set)
    for col in campos:
        tabla.heading(col, text=col)
        tabla.column(col, width=100)
    tabla.pack(pady=10, fill="both", expand=True)

    scrollbar.config(command=tabla.yview)
    scrollbar1.config(command=tabla.xview)
    codigo_original_var = [None]

    def on_select(event):
        select_item = tabla.selection()
        if select_item:
            values = tabla.item(select_item)['values']
            for i, campo in enumerate(campos):
                entradas[campo].delete(0, 'end')
                entradas[campo].insert(0, values[i])
            codigo_original_var[0] = values[0]

    tabla.bind('<<TreeviewSelect>>', on_select)

    def validate_date(date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def buscar_y_mostrar(event=None, combo_busqueda=None):
        criterio = combo_busqueda.get() if combo_busqueda else "Código"
        valor = entry_busqueda.get().strip()
        if not valor:
            ver_articulos(tabla)
            for entrada in entradas.values():
                entrada.delete(0, 'end')
            codigo_original_var[0] = None
            entry_busqueda.focus_set()
            return

        for row in tabla.get_children():
            tabla.delete(row)
        for entrada in entradas.values():
            entrada.delete(0, 'end')
        codigo_original_var[0] = None

        # Mapear el criterio de la interfaz a los valores esperados por buscar_articulo
        criterio_db = "codigo" if criterio == "Código" else "nombre"

        if criterio == "Código":
            resultado = buscar_articulo(criterio_db, valor)  # Pasar ambos argumentos
            if resultado:
                tabla.insert("", "end", values=resultado[0])  # Usar resultado[0] para un solo registro
                for i, campo in enumerate(campos):
                    entradas[campo].insert(0, resultado[0][i])
                codigo_original_var[0] = resultado[0][0]
            else:
                response = messagebox.askyesno("No encontrado", f"No se encontró un artículo con el código {valor}. ¿Desea agregarlo?")
                if response:
                    entradas["Código:"].insert(0, valor)
                    entry_busqueda.delete(0, 'end')
        elif criterio == "Nombre":
            resultados = buscar_articulo(criterio_db, valor)  # Pasar ambos argumentos
            if resultados:
                for resultado in resultados:
                    tabla.insert("", "end", values=resultado)
                for i, campo in enumerate(campos):
                    entradas[campo].insert(0, resultados[0][i])
                codigo_original_var[0] = resultados[0][0]
            else:
                messagebox.showwarning("No encontrado", f"No se encontró un artículo con el nombre {valor}")
        entry_busqueda.focus_set()

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

        if not validate_date(fecha_caducidad):
            messagebox.showerror("Error", "Fecha de caducidad debe estar en formato YYYY-MM-DD")
            return

        try:
            precio = float(precio)
            costo = float(costo)
            existencia = int(existencia)
            id_proveedor = int(id_proveedor)
            id_unidad = int(id_unidad)
            if existencia < 0:
                messagebox.showerror("Error", "La existencia no puede ser negativa")
                return
            if not (buscar_catalogo(categoria_codigo) and buscar_proveedor(id_proveedor) and buscar_unidad(id_unidad)):
                messagebox.showerror("Error", "Código de categoría, ID de proveedor o ID de unidad no válidos")
                return
        except ValueError:
            messagebox.showerror("Error", "Precio, Costo, Existencia, ID Proveedor e ID Unidad deben ser valores numéricos")
            return

        agregar_articulo(codigo, nombre, precio, costo, existencia, descripcion, fecha_caducidad, categoria_codigo, id_proveedor, id_unidad)
        ver_articulos(tabla)
        limpiar_campos()
        if codigo_prellenado:
            from ventas import crear_seccion_ventas
            for widget in ventana.winfo_children():
                if widget != barra_lateral:
                    widget.destroy()
            crear_seccion_ventas(ventana, barra_lateral, None)

    def eliminar():
        codigo = entradas["Código:"].get().strip()
        if not codigo:
            messagebox.showerror("Error", "El campo Código es obligatorio")
            return
        response = messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar el artículo con código {codigo}? Esto también eliminará las ventas asociadas.")
        if response:
            try:
                eliminar_articulos(codigo)
                ver_articulos(tabla)
                limpiar_campos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el artículo: {e}")

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

        if not validate_date(fecha_caducidad):
            messagebox.showerror("Error", "Fecha de caducidad debe estar en formato YYYY-MM-DD")
            return

        try:
            precio = float(precio)
            costo = float(costo)
            existencia = int(existencia)
            id_proveedor = int(id_proveedor)
            id_unidad = int(id_unidad)
            if existencia < 0:
                messagebox.showerror("Error", "La existencia no puede ser negativa")
                return
            if not (buscar_catalogo(categoria_codigo) and buscar_proveedor(id_proveedor) and buscar_unidad(id_unidad)):
                messagebox.showerror("Error", "Código de categoría, ID de proveedor o ID de unidad no válidos")
                return
        except ValueError:
            messagebox.showerror("Error", "Precio, Costo, Existencia, ID Proveedor e ID Unidad deben ser valores numéricos")
            return

        actualizar_articulo(
            codigo_original_var[0],
            nombre, precio, costo, existencia, descripcion, fecha_caducidad, categoria_codigo, id_proveedor, id_unidad
        )
        ver_articulos(tabla)
        limpiar_campos()

    def limpiar_campos():
        for entrada in entradas.values():
            entrada.delete(0, 'end')
        entry_busqueda.delete(0, 'end')
        codigo_original_var[0] = None
        entry_busqueda.focus_set()

    Button(frame_derecho, text="Agregar", font=("Arial", 10), bg="#4CAF50", fg="white", width=15,
           command=agregar).pack(pady=5)
    Button(frame_derecho, text="Eliminar", font=("Arial", 10), bg="#F44336", fg="white", width=15,
           command=eliminar).pack(pady=5)
    Button(frame_derecho, text="Actualizar", font=("Arial", 10), bg="#2196F3", fg="white", width=15,
           command=actualizar_datos).pack(pady=5)
    Button(frame_derecho, text="Limpiar", font=("Arial", 10), bg="#FFC107", fg="black", width=15,
           command=limpiar_campos).pack(pady=5)
    Button(frame_search, text="Buscar", font=("Arial", 10), bg="#2196F3", fg="white",
       command=lambda: buscar_y_mostrar(None, combo_busqueda)).pack(side="left", pady=5, padx=5)

    ver_articulos(tabla)
    entry_busqueda.focus_set()

    return frame_principal

if __name__ == "__main__":
    interfaz_articulos()