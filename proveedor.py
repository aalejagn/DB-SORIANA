from tkinter import Tk, Label, Frame, Entry, Button, ttk, messagebox, Scrollbar, StringVar
from db_soriana import agregar_proveedor, eliminar_proveedor, actualizar_proveedor, ver_proveedor, buscar_proveedor

def interfaz_proveedor():
    ventana = Tk()
    ventana.title("Proveedores")
    ventana.geometry("800x600")
    crear_seccion_proveedor(ventana, None).pack(expand=True, fill="both")
    ventana.mainloop()

def crear_seccion_proveedor(ventana, barra_lateral):
    campos = ["ID Proveedor:", "Nombre:", "Teléfono:", "Empresa:", "Descripción:"]

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

    Label(frame_izquierdo, text="Proveedores", font=("Arial", 16, "bold"), bg="#E6F0FA").pack(pady=10)

    frame_search = Frame(frame_izquierdo, bg="#E6F0FA")
    frame_search.pack(fill="x", pady=5)
    Label(frame_search, text="Buscar por:", bg="#E6F0FA", font=("Arial", 12)).pack(side="left", padx=(10, 2))
    criterio_var = StringVar(value="ID Proveedor")
    combo_busqueda = ttk.Combobox(frame_search, textvariable=criterio_var, values=["ID Proveedor", "Nombre", "Teléfono"], font=("Arial", 12), state="readonly", width=12)
    combo_busqueda.pack(side="left", padx=(0, 5))
    entry_busqueda = Entry(frame_search, font=("Arial", 12), width=20)
    entry_busqueda.pack(side="left", padx=(0, 10))

    frame_entradas = Frame(frame_izquierdo, bg="#E6F0FA")
    frame_entradas.pack(fill="x", pady=5)

    entradas = {}
    for i, campo in enumerate(campos):
        Label(frame_entradas, text=campo, bg="#E6F0FA", font=("Arial", 12)).grid(row=i, column=0, padx=(10, 2), pady=5, sticky="e")
        entrada = Entry(frame_entradas, font=("Arial", 12))
        entrada.grid(row=i, column=1, padx=(0, 10), pady=5, sticky="w")
        entradas[campo] = entrada

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

    id_proveedor_original_var = [None]

    def on_select(event):
        select_item = tabla.selection()
        if select_item:
            values = tabla.item(select_item)['values']
            for i, campo in enumerate(campos):
                entradas[campo].delete(0, 'end')
                entradas[campo].insert(0, values[i])
            id_proveedor_original_var[0] = values[0]

    tabla.bind('<<TreeviewSelect>>', on_select)

    def buscar_y_mostrar():
        criterio = criterio_var.get().lower()
        valor = entry_busqueda.get().strip()
        if not valor:
            ver_proveedor(tabla)
            for entrada in entradas.values():
                entrada.delete(0, 'end')
            id_proveedor_original_var[0] = None
            entry_busqueda.focus_set()
            return

        criterio_map = {"id proveedor": "id_proveedor", "nombre": "nombre", "teléfono": "telefono"}
        resultados = buscar_proveedor(criterio_map[criterio], valor)

        for row in tabla.get_children():
            tabla.delete(row)
        for entrada in entradas.values():
            entrada.delete(0, 'end')
        id_proveedor_original_var[0] = None

        if not resultados:
            messagebox.showwarning("No encontrado", f"No se encontró un proveedor con {criterio.replace('id proveedor', 'ID Proveedor')} '{valor}'")
            entry_busqueda.focus_set()
            return

        resultado = resultados[0]  # Toma el primer resultado
        tabla.insert("", "end", values=resultado)
        for i, campo in enumerate(campos):
            entradas[campo].insert(0, resultado[i])
        id_proveedor_original_var[0] = resultado[0]  # ID Proveedor está en índice 0
        entry_busqueda.focus_set()

    entry_busqueda.bind('<Return>', lambda event: buscar_y_mostrar())

    Button(frame_search, text="Buscar", font=("Arial", 10), bg="#2196F3", fg="white",
           command=buscar_y_mostrar).pack(side="left", pady=5, padx=5)

    def agregar():
        id_proveedor = entradas["ID Proveedor:"].get().strip()
        nombre = entradas["Nombre:"].get().strip()
        telefono = entradas["Teléfono:"].get().strip()
        empresa = entradas["Empresa:"].get().strip()
        descripcion = entradas["Descripción:"].get().strip()

        if not all([id_proveedor, nombre, telefono, empresa, descripcion]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        agregar_proveedor(id_proveedor, nombre, telefono, empresa, descripcion)
        ver_proveedor(tabla)
        limpiar_campos()

    def eliminar():
        id_proveedor = entradas["ID Proveedor:"].get().strip()
        if not id_proveedor:
            messagebox.showerror("Error", "El campo ID Proveedor es obligatorio")
            return
        eliminar_proveedor(id_proveedor)
        ver_proveedor(tabla)
        limpiar_campos()

    def actualizar_datos():
        id_proveedor = entradas["ID Proveedor:"].get().strip()
        nombre = entradas["Nombre:"].get().strip()
        telefono = entradas["Teléfono:"].get().strip()
        empresa = entradas["Empresa:"].get().strip()
        descripcion = entradas["Descripción:"].get().strip()

        if not all([id_proveedor, nombre, telefono, empresa, descripcion]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        if not id_proveedor_original_var[0]:
            messagebox.showerror("Error", "Seleccione un proveedor para actualizar")
            return

        actualizar_proveedor(id_proveedor_original_var[0], id_proveedor, nombre, telefono, empresa, descripcion)
        ver_proveedor(tabla)
        limpiar_campos()

    def limpiar_campos():
        for entrada in entradas.values():
            entrada.delete(0, 'end')
        entry_busqueda.delete(0, 'end')
        id_proveedor_original_var[0] = None

    Button(frame_derecho, text="Agregar", font=("Arial", 10), bg="#4CAF50", fg="white", width=15,
           command=agregar).pack(pady=5)
    Button(frame_derecho, text="Eliminar", font=("Arial", 10), bg="#F44336", fg="white", width=15,
           command=eliminar).pack(pady=5)
    Button(frame_derecho, text="Actualizar", font=("Arial", 10), bg="#2196F3", fg="white", width=15,
           command=actualizar_datos).pack(pady=5)
    Button(frame_derecho, text="Limpiar", font=("Arial", 10), bg="#FFC107", fg="black", width=15,
           command=limpiar_campos).pack(pady=5)

    ver_proveedor(tabla)

    return frame_principal

if __name__ == "__main__":
    interfaz_proveedor()