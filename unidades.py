from tkinter import Tk, Label, Frame, Entry, Button, ttk, messagebox,Scrollbar
from db_soriana import agregar_unidad, eliminar_unidad, actualizar_unidad, ver_unidad, buscar_unidad

def interfaz_unidades():
    ventana = Tk()
    ventana.title("Unidades")
    ventana.geometry("800x600")
    crear_seccion_unidades(ventana, None).pack(expand=True, fill="both")
    ventana.mainloop()

def crear_seccion_unidades(ventana, barra_lateral):
    campos = ["ID Unidad:", "Nombre:", "Descripción:"]

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

    Label(frame_izquierdo, text="Unidades", font=("Arial", 16, "bold"), bg="#E6F0FA").pack(pady=10)

    frame_search = Frame(frame_izquierdo, bg="#E6F0FA")
    frame_search.pack(fill="x", pady=5)
    Label(frame_search, text="Buscar por ID Unidad:", bg="#E6F0FA", font=("Arial", 12)).pack(side="left", padx=(10, 2))
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
    id_unidad_original_var = [None]

    def on_select(event):
        select_item = tabla.selection()
        if select_item:
            values = tabla.item(select_item)['values']
            for i, campo in enumerate(campos):
                entradas[campo].delete(0, 'end')
                entradas[campo].insert(0, values[i])
            id_unidad_original_var[0] = values[0]

    tabla.bind('<<TreeviewSelect>>', on_select)

    def buscar_y_mostrar():
        id_unidad = entry_busqueda.get().strip()
        if not id_unidad:
            ver_unidad(tabla)
            for entrada in entradas.values():
                entrada.delete(0, 'end')
            id_unidad_original_var[0] = None
            return

        resultado = buscar_unidad(id_unidad)
        for row in tabla.get_children():
            tabla.delete(row)
        for entrada in entradas.values():
            entrada.delete(0, 'end')
        id_unidad_original_var[0] = None

        if resultado:
            tabla.insert("", "end", values=resultado)
            for i, campo in enumerate(campos):
                entradas[campo].insert(0, resultado[i])
            id_unidad_original_var[0] = resultado[0]
        else:
            messagebox.showwarning("No encontrado", f"No se encontró una unidad con el ID {id_unidad}")

    Button(frame_search, text="Buscar", font=("Arial", 10), bg="#2196F3", fg="white",
           command=buscar_y_mostrar).pack(side="left", pady=5, padx=5)

    def agregar():
        id_unidad = entradas["ID Unidad:"].get().strip()
        nombre = entradas["Nombre:"].get().strip()
        descripcion = entradas["Descripción:"].get().strip()

        if not all([id_unidad, nombre, descripcion]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        agregar_unidad(id_unidad, nombre, descripcion)
        ver_unidad(tabla)
        limpiar_campos()

    def eliminar():
        id_unidad = entradas["ID Unidad:"].get().strip()
        if not id_unidad:
            messagebox.showerror("Error", "El campo ID Unidad es obligatorio")
            return
        eliminar_unidad(id_unidad)
        ver_unidad(tabla)
        limpiar_campos()

    def actualizar_datos():
        id_unidad = entradas["ID Unidad:"].get().strip()
        nombre = entradas["Nombre:"].get().strip()
        descripcion = entradas["Descripción:"].get().strip()

        if not all([id_unidad, nombre, descripcion]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        if not id_unidad_original_var[0]:
            messagebox.showerror("Error", "Seleccione una unidad para actualizar")
            return

        actualizar_unidad(id_unidad_original_var[0], id_unidad, nombre, descripcion)
        ver_unidad(tabla)
        limpiar_campos()

    def limpiar_campos():
        for entrada in entradas.values():
            entrada.delete(0, 'end')
        entry_busqueda.delete(0, 'end')
        id_unidad_original_var[0] = None

    Button(frame_derecho, text="Agregar", font=("Arial", 10), bg="#4CAF50", fg="white", width=15,
           command=agregar).pack(pady=5)
    Button(frame_derecho, text="Eliminar", font=("Arial", 10), bg="#F44336", fg="white", width=15,
           command=eliminar).pack(pady=5)
    Button(frame_derecho, text="Actualizar", font=("Arial", 10), bg="#2196F3", fg="white", width=15,
           command=actualizar_datos).pack(pady=5)
    Button(frame_derecho, text="Limpiar", font=("Arial", 10), bg="#FFC107", fg="black", width=15,
           command=limpiar_campos).pack(pady=5)

    ver_unidad(tabla)

    return frame_principal

if __name__ == "__main__":
    interfaz_unidades()