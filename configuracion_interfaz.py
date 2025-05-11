from tkinter import Label, Frame, Button, ttk, messagebox, Entry
from configuracion import Configuracion
from exportar_db import listar_tablas, exportar_tabla_a_csv

def crear_seccion_exportar_base_datos(ventana, barra_lateral, ventana_principal):
    frame_principal = Frame(ventana, bg="#E6F0FA")
    frame_principal.pack(expand=True, fill="both")

    frame_centrado = Frame(frame_principal, bg="#E6F0FA")
    frame_centrado.pack(expand=True, fill="both", padx=10, pady=10)

    frame_derecho = Frame(frame_centrado, bg="#E6F0FA", width=150)
    frame_derecho.pack(side="right", fill="y", padx=10)

    frame_izquierdo = Frame(frame_centrado, bg="#E6F0FA")
    frame_izquierdo.pack(side="left", expand=True, fill="both")

    Label(frame_izquierdo, text="Exportar Base de Datos", font=("Arial", 16, "bold"), bg="#E6F0FA").pack(pady=10)

    frame_selector = Frame(frame_izquierdo, bg="#E6F0FA")
    frame_selector.pack(fill="x", pady=5)

    Label(frame_selector, text="Seleccionar tabla:", bg="#E6F0FA", font=("Arial", 12)).pack(side="left", padx=(10, 2))
    
    tablas = listar_tablas()
    combo_tablas = ttk.Combobox(frame_selector, values=tablas, font=("Arial", 12), state="readonly")
    combo_tablas.pack(side="left", padx=(0, 10))
    if tablas:
        combo_tablas.set(tablas[0])

    def exportar_seleccionada():
        tabla_seleccionada = combo_tablas.get()
        if not tabla_seleccionada:
            messagebox.showerror("Error", "Por favor, seleccione una tabla")
            return
        exportar_tabla_a_csv(tabla_seleccionada)

    Button(frame_derecho, text="Exportar a CSV", font=("Arial", 10), bg="#4CAF50", fg="white", width=15,
           command=exportar_seleccionada).pack(pady=5)

    return frame_principal

def crear_seccion_configuracion(ventana, barra_lateral, ventana_principal):
    frame_principal = Frame(ventana, bg="#E6F0FA")
    frame_principal.pack(expand=True, fill="both")

    frame_centrado = Frame(frame_principal, bg="#E6F0FA")
    frame_centrado.pack(expand=True, fill="both", padx=10, pady=10)

    frame_derecho = Frame(frame_centrado, bg="#E6F0FA", width=150)
    frame_derecho.pack(side="right", fill="y", padx=10)

    frame_izquierdo = Frame(frame_centrado, bg="#E6F0FA")
    frame_izquierdo.pack(side="left", expand=True, fill="both")

    Label(frame_izquierdo, text="Gestión de Usuarios", font=("Arial", 16, "bold"), bg="#E6F0FA").pack(pady=10)

    frame_search = Frame(frame_izquierdo, bg="#E6F0FA")
    frame_search.pack(fill="x", pady=5)
    Label(frame_search, text="Buscar por usuario:", bg="#E6F0FA", font=("Arial", 12)).pack(side="left", padx=(10, 2))
    entry_busqueda = Entry(frame_search, font=("Arial", 12), width=20)
    entry_busqueda.pack(side="left", padx=(0, 10))

    frame_entradas = Frame(frame_izquierdo, bg="#E6F0FA")
    frame_entradas.pack(fill="x", pady=5)

    campos = ["Usuario:", "Contraseña:"]
    entradas = {}
    for i, campo in enumerate(campos):
        Label(frame_entradas, text=campo, bg="#E6F0FA", font=("Arial", 12)).grid(row=i, column=0, padx=(10, 2), pady=5, sticky="e")
        entrada = Entry(frame_entradas, font=("Arial", 12))
        entrada.grid(row=i, column=1, padx=(0, 10), pady=5, sticky="w")
        entradas[campo] = entrada

    tabla = ttk.Treeview(frame_izquierdo, columns=campos, show="headings", height=15)
    for col in campos:
        tabla.heading(col, text=col)
        tabla.column(col, width=150)
    tabla.pack(pady=10, fill="both", expand=True)

    usuario_original_var = [None]

    def on_select(event):
        select_item = tabla.selection()
        if select_item:
            values = tabla.item(select_item)['values']
            for i, campo in enumerate(campos):
                entradas[campo].delete(0, 'end')
                entradas[campo].insert(0, values[i])
            usuario_original_var[0] = values[0]

    tabla.bind('<<TreeviewSelect>>', on_select)

    def ver_usuarios():
        config = Configuracion("gerente")
        usuarios = config.obtener_usuarios()
        for row in tabla.get_children():
            tabla.delete(row)
        for usuario, contraseña in usuarios.items():
            tabla.insert("", "end", values=(usuario, contraseña))

    def buscar_y_mostrar():
        usuario = entry_busqueda.get().strip().lower()
        if not usuario:
            ver_usuarios()
            for entrada in entradas.values():
                entrada.delete(0, 'end')
            usuario_original_var[0] = None
            return

        config = Configuracion("gerente")
        usuarios = config.obtener_usuarios()
        for row in tabla.get_children():
            tabla.delete(row)
        for entrada in entradas.values():
            entrada.delete(0, 'end')
        usuario_original_var[0] = None

        if usuario in usuarios:
            contraseña = usuarios[usuario]
            tabla.insert("", "end", values=(usuario, contraseña))
            entradas["Usuario:"].insert(0, usuario)
            entradas["Contraseña:"].insert(0, contraseña)
            usuario_original_var[0] = usuario
        else:
            messagebox.showwarning("No encontrado", f"No se encontró el usuario {usuario}")

    def agregar():
        usuario = entradas["Usuario:"].get().strip()
        contraseña = entradas["Contraseña:"].get().strip()

        if not all([usuario, contraseña]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        if usuario.lower() == "gerente":
            messagebox.showerror("Error", "No se puede agregar un usuario con el nombre 'gerente'")
            return

        config = Configuracion("gerente")
        if config.agregar_usuario(usuario, contraseña):
            ver_usuarios()
            limpiar_campos()
            messagebox.showinfo("Éxito", f"Usuario {usuario} agregado correctamente")

    def eliminar():
        usuario = entradas["Usuario:"].get().strip()
        if not usuario:
            messagebox.showerror("Error", "El campo Usuario es obligatorio")
            return

        if usuario.lower() == "gerente":
            messagebox.showerror("Error", "No se puede eliminar el usuario 'gerente'")
            return

        config = Configuracion("gerente")
        if config.eliminar_usuario(usuario):
            ver_usuarios()
            limpiar_campos()
            messagebox.showinfo("Éxito", f"Usuario {usuario} eliminado correctamente")

    def actualizar_datos():
        usuario = entradas["Usuario:"].get().strip()
        contraseña = entradas["Contraseña:"].get().strip()

        if not all([usuario, contraseña]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        if not usuario_original_var[0]:
            messagebox.showerror("Error", "Seleccione un usuario para actualizar")
            return

        if usuario_original_var[0].lower() == "gerente":
            messagebox.showerror("Error", "No se puede modificar el usuario 'gerente'")
            return

        config = Configuracion("gerente")
        if config.modificar_contraseña(usuario_original_var[0], contraseña):
            ver_usuarios()
            limpiar_campos()
            messagebox.showinfo("Éxito", f"Usuario {usuario_original_var[0]} actualizado correctamente")

    def limpiar_campos():
        for entrada in entradas.values():
            entrada.delete(0, 'end')
        entry_busqueda.delete(0, 'end')
        usuario_original_var[0] = None

    Button(frame_search, text="Buscar", font=("Arial", 10), bg="#2196F3", fg="white",
           command=buscar_y_mostrar).pack(side="left", pady=5, padx=5)

    btn_agregar = Button(frame_derecho, text="Agregar", font=("Arial", 10), bg="#4CAF50", fg="white", width=15,
                         command=agregar)
    btn_agregar.pack(pady=5)
    btn_eliminar = Button(frame_derecho, text="Eliminar", font=("Arial", 10), bg="#F44336", fg="white", width=15,
                          command=eliminar)
    btn_eliminar.pack(pady=5)
    btn_actualizar = Button(frame_derecho, text="Actualizar", font=("Arial", 10), bg="#2196F3", fg="white", width=15,
                            command=actualizar_datos)
    btn_actualizar.pack(pady=5)
    Button(frame_derecho, text="Limpiar", font=("Arial", 10), bg="#FFC107", fg="black", width=15,
           command=limpiar_campos).pack(pady=5)

    ver_usuarios()

    return frame_principal