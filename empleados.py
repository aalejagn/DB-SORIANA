from tkinter import Tk, Label, Frame, Entry, Button, ttk, messagebox, Scrollbar, StringVar
from db_soriana import agregar_empleado, eliminar_empleado, actualizar_empleado, ver_empleado, buscar_trabajador

def interfaz_empleados():
    ventana = Tk()
    ventana.title("Empleados")
    ventana.geometry("800x600")
    crear_seccion_empleados(ventana, None).pack(expand=True, fill="both")
    ventana.mainloop()

def crear_seccion_empleados(ventana, barra_lateral):
    campos = ["ID Empleado:", "Nombre:", "Apellidos:", "Teléfono:", "Edad:", "Puesto:", "Sueldo:", "Fecha Contratación:", "RFC:"]

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

    Label(frame_izquierdo, text="Empleados", font=("Arial", 16, "bold"), bg="#E6F0FA").pack(pady=10)

    frame_search = Frame(frame_izquierdo, bg="#E6F0FA")
    frame_search.pack(fill="x", pady=5)
    Label(frame_search, text="Buscar por:", bg="#E6F0FA", font=("Arial", 12)).pack(side="left", padx=(10, 2))
    criterio_var = StringVar(value="ID Empleado")
    combo_busqueda = ttk.Combobox(frame_search, textvariable=criterio_var, values=["ID Empleado", "Nombre", "Teléfono"], font=("Arial", 12), state="readonly", width=12)
    combo_busqueda.pack(side="left", padx=(0, 5))
    entry_busqueda = Entry(frame_search, font=("Arial", 12), width=20)
    entry_busqueda.pack(side="left", padx=(0, 10))

    # Frame para entradas, dividido en dos columnas
    frame_entradas = Frame(frame_izquierdo, bg="#E6F0FA")
    frame_entradas.pack(fill="x", pady=5)

    # Subframe para la columna izquierda (5 campos)
    frame_entradas_izq = Frame(frame_entradas, bg="#E6F0FA")
    frame_entradas_izq.pack(side="left", padx=10)

    # Subframe para la columna derecha (4 campos)
    frame_entradas_der = Frame(frame_entradas, bg="#E6F0FA")
    frame_entradas_der.pack(side="left", padx=10)

    entradas = {}
    # Campos en la columna izquierda (índices 0 a 4)
    for i, campo in enumerate(campos[:5]):
        Label(frame_entradas_izq, text=campo, bg="#E6F0FA", font=("Arial", 12)).grid(row=i, column=0, padx=(10, 2), pady=5, sticky="e")
        entrada = Entry(frame_entradas_izq, font=("Arial", 12))
        entrada.grid(row=i, column=1, padx=(0, 10), pady=5, sticky="w")
        entradas[campo] = entrada

    # Campos en la columna derecha (índices 5 a 8)
    for i, campo in enumerate(campos[5:]):
        Label(frame_entradas_der, text=campo, bg="#E6F0FA", font=("Arial", 12)).grid(row=i, column=0, padx=(10, 2), pady=5, sticky="e")
        entrada = Entry(frame_entradas_der, font=("Arial", 12))
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
    
    id_empleado_original_var = [None]

    def on_select(event):
        select_item = tabla.selection()
        if select_item:
            values = tabla.item(select_item)['values']
            for i, campo in enumerate(campos):
                entradas[campo].delete(0, 'end')
                entradas[campo].insert(0, values[i])
            id_empleado_original_var[0] = values[0]

    tabla.bind('<<TreeviewSelect>>', on_select)

    def buscar_y_mostrar():
        criterio = criterio_var.get().lower()
        valor = entry_busqueda.get().strip()
        if not valor:
            ver_empleado(tabla)
            for entrada in entradas.values():
                entrada.delete(0, 'end')
            id_empleado_original_var[0] = None
            entry_busqueda.focus_set()
            return

        criterio_map = {"id empleado": "id_empleado", "nombre": "nombre", "teléfono": "telefono"}
        resultados = buscar_trabajador(criterio_map[criterio], valor)

        for row in tabla.get_children():
            tabla.delete(row)
        for entrada in entradas.values():
            entrada.delete(0, 'end')
        id_empleado_original_var[0] = None

        if not resultados:
            messagebox.showwarning("No encontrado", f"No se encontró un empleado con {criterio.replace('id empleado', 'ID Empleado')} '{valor}'")
            entry_busqueda.focus_set()
            return

        resultado = resultados[0]  # Toma el primer resultado
        tabla.insert("", "end", values=resultado)
        for i, campo in enumerate(campos):
            entradas[campo].insert(0, resultado[i])
        id_empleado_original_var[0] = resultado[0]  # ID Empleado está en índice 0
        entry_busqueda.focus_set()

    entry_busqueda.bind('<Return>', lambda event: buscar_y_mostrar())

    Button(frame_search, text="Buscar", font=("Arial", 10), bg="#2196F3", fg="white",
           command=buscar_y_mostrar).pack(side="left", pady=5, padx=5)

    def agregar():
        nombre = entradas["Nombre:"].get().strip()
        apellidos = entradas["Apellidos:"].get().strip()
        telefono = entradas["Teléfono:"].get().strip()
        edad = entradas["Edad:"].get().strip()
        puesto = entradas["Puesto:"].get().strip()
        sueldo = entradas["Sueldo:"].get().strip()
        fecha_contratacion = entradas["Fecha Contratación:"].get().strip()
        rfc = entradas["RFC:"].get().strip()

        if not all([nombre, apellidos, telefono, edad, puesto, sueldo, fecha_contratacion, rfc]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        agregar_empleado(nombre, apellidos, telefono, edad, puesto, sueldo, fecha_contratacion, rfc)
        ver_empleado(tabla)
        limpiar_campos()

    def eliminar():
        id_empleado = entradas["ID Empleado:"].get().strip()
        if not id_empleado:
            messagebox.showerror("Error", "El campo ID Empleado es obligatorio")
            return
        eliminar_empleado(id_empleado)
        ver_empleado(tabla)
        limpiar_campos()

    def actualizar_datos():
        nombre = entradas["Nombre:"].get().strip()
        apellidos = entradas["Apellidos:"].get().strip()
        telefono = entradas["Teléfono:"].get().strip()
        edad = entradas["Edad:"].get().strip()
        puesto = entradas["Puesto:"].get().strip()
        sueldo = entradas["Sueldo:"].get().strip()
        fecha_contratacion = entradas["Fecha Contratación:"].get().strip()
        rfc = entradas["RFC:"].get().strip()

        if not all([nombre, apellidos, telefono, edad, puesto, sueldo, fecha_contratacion, rfc]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        if not id_empleado_original_var[0]:
            messagebox.showerror("Error", "Seleccione un empleado para actualizar")
            return

        actualizar_empleado(id_empleado_original_var[0], nombre, apellidos, telefono, edad, puesto, sueldo, fecha_contratacion, rfc)
        ver_empleado(tabla)
        limpiar_campos()

    def limpiar_campos():
        for entrada in entradas.values():
            entrada.delete(0, 'end')
        entry_busqueda.delete(0, 'end')
        id_empleado_original_var[0] = None

    Button(frame_derecho, text="Agregar", font=("Arial", 10), bg="#4CAF50", fg="white", width=15,
           command=agregar).pack(pady=5)
    Button(frame_derecho, text="Eliminar", font=("Arial", 10), bg="#F44336", fg="white", width=15,
           command=eliminar).pack(pady=5)
    Button(frame_derecho, text="Actualizar", font=("Arial", 10), bg="#2196F3", fg="white", width=15,
           command=actualizar_datos).pack(pady=5)
    Button(frame_derecho, text="Limpiar", font=("Arial", 10), bg="#FFC107", fg="black", width=15,
           command=limpiar_campos).pack(pady=5)

    ver_empleado(tabla)

    return frame_principal

if __name__ == "__main__":
    interfaz_empleados()