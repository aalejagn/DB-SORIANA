from tkinter import Tk, Label, Frame, Entry, Button, ttk, messagebox, Toplevel, Scrollbar, StringVar
from db_soriana import agregar_catalogo, eliminar_catalogo, actualizar_catalogo, ver_catalogo, buscar_catalogo

def interfaz_categorias():
    ventana = Tk()
    ventana.title("Categorías")
    ventana.geometry("800x600")
    crear_seccion_categorias(ventana, None).pack(expand=True, fill="both")
    ventana.mainloop()

def crear_seccion_categorias(ventana, barra_lateral):
    campos = ["Código:", "Nombre:", "Descripción:"]

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

    Label(frame_izquierdo, text="Categorías", font=("Arial", 16, "bold"), bg="#E6F0FA").pack(pady=10)

    frame_search = Frame(frame_izquierdo, bg="#E6F0FA")
    frame_search.pack(fill="x", pady=5)
    Label(frame_search, text="Buscar por:", bg="#E6F0FA", font=("Arial", 12)).pack(side="left", padx=(10, 2))
    criterio_var = StringVar(value="Código")
    combo_busqueda = ttk.Combobox(frame_search, textvariable=criterio_var, values=["Código", "Nombre"], font=("Arial", 12), state="readonly", width=10)
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

    def buscar_y_mostrar():
        criterio = criterio_var.get().lower()
        valor = entry_busqueda.get().strip()
        if not valor:
            ver_catalogo(tabla)
            for entrada in entradas.values():
                entrada.delete(0, 'end')
            codigo_original_var[0] = None
            entry_busqueda.focus_set()
            return

        criterio_map = {"código": "codigo", "nombre": "nombre"}
        resultados = buscar_catalogo(criterio_map[criterio], valor)

        for row in tabla.get_children():
            tabla.delete(row)
        for entrada in entradas.values():
            entrada.delete(0, 'end')
        codigo_original_var[0] = None

        if not resultados:
            messagebox.showwarning("No encontrado", f"No se encontró una categoría con {criterio} '{valor}'")
            entry_busqueda.focus_set()
            return

        resultado = resultados[0]  # Toma el primer resultado
        tabla.insert("", "end", values=resultado)
        for i, campo in enumerate(campos):
            entradas[campo].insert(0, resultado[i])
        codigo_original_var[0] = resultado[0]
        entry_busqueda.focus_set()

    entry_busqueda.bind('<Return>', lambda event: buscar_y_mostrar())

    Button(frame_search, text="Buscar", font=("Arial", 10), bg="#2196F3", fg="white",
           command=buscar_y_mostrar).pack(side="left", pady=5, padx=5)

    def agregar():
        codigo = entradas["Código:"].get().strip()
        nombre = entradas["Nombre:"].get().strip()
        descripcion = entradas["Descripción:"].get().strip()

        if not all([codigo, nombre, descripcion]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        agregar_catalogo(codigo, nombre, descripcion)
        ver_catalogo(tabla)
        limpiar_campos()

    def eliminar():
        codigo = entradas["Código:"].get().strip()
        if not codigo:
            messagebox.showerror("Error", "El campo Código es obligatorio")
            return
        eliminar_catalogo(codigo)
        ver_catalogo(tabla)
        limpiar_campos()

    def actualizar_datos():
        codigo = entradas["Código:"].get().strip()
        nombre = entradas["Nombre:"].get().strip()
        descripcion = entradas["Descripción:"].get().strip()

        if not all([codigo, nombre, descripcion]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        if not codigo_original_var[0]:
            messagebox.showerror("Error", "Seleccione una categoría para actualizar")
            return

        actualizar_catalogo(codigo_original_var[0], codigo, nombre, descripcion)
        ver_catalogo(tabla)
        limpiar_campos()

    def limpiar_campos():
        for entrada in entradas.values():
            entrada.delete(0, 'end')
        entry_busqueda.delete(0, 'end')
        codigo_original_var[0] = None

    Button(frame_derecho, text="Agregar", font=("Arial", 10), bg="#4CAF50", fg="white", width=15,
           command=agregar).pack(pady=5)
    Button(frame_derecho, text="Eliminar", font=("Arial", 10), bg="#F44336", fg="white", width=15,
           command=eliminar).pack(pady=5)
    Button(frame_derecho, text="Actualizar", font=("Arial", 10), bg="#2196F3", fg="white", width=15,
           command=actualizar_datos).pack(pady=5)
    Button(frame_derecho, text="Limpiar", font=("Arial", 10), bg="#FFC107", fg="black", width=15,
           command=limpiar_campos).pack(pady=5)

    ver_catalogo(tabla)

    return frame_principal

if __name__ == "__main__":
    interfaz_categorias()