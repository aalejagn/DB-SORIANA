from tkinter import Label, Frame, Button, ttk, messagebox, Entry, Scrollbar
from tkinter import StringVar
from configuracion import Configuracion

# tood: Función para crear la sección de configuración de usuarios
def crear_seccion_configuracion(ventana, barra_lateral, ventana_principal):
    frame_principal = Frame(ventana, bg="#E6F0FA")
    frame_principal.pack(expand=True, fill="both")

    frame_centrado = Frame(frame_principal, bg="#E6F0FA")
    frame_centrado.pack(expand=True, fill="both", padx=10, pady=10)

    frame_derecho = Frame(frame_centrado, bg="#E6F0FA", width=150)
    frame_derecho.pack(side="right", fill="y", padx=10)

    frame_izquierdo = Frame(frame_centrado, bg="#E6F0FA")
    frame_izquierdo.pack(side="left", expand=True, fill="both")

    # tood: Título de la sección
    Label(frame_izquierdo, text="Gestión de Usuarios", font=("Arial", 16, "bold"), bg="#E6F0FA").pack(pady=10)

    # tood: Frame para la búsqueda de usuarios
    frame_search = Frame(frame_izquierdo, bg="#E6F0FA")
    frame_search.pack(fill="x", pady=5)
    Label(frame_search, text="Buscar por usuario:", bg="#E6F0FA", font=("Arial", 12)).pack(side="left", padx=(10, 2))
    entry_busqueda = Entry(frame_search, font=("Arial", 12), width=20)
    entry_busqueda.pack(side="left", padx=(0, 10))

    # tood: Frame para los campos de entrada
    frame_entradas = Frame(frame_izquierdo, bg="#E6F0FA")
    frame_entradas.pack(fill="x", pady=5)

    # tood: Usar StringVar para controlar el rol seleccionado
    rol_var = StringVar(value="Cajero")  # Valor por defecto: Cajero
    campos = ["Rol:", "Contraseña:"]
    entradas = {}
    
    # tood: Crear Combobox para seleccionar el rol (Supervisor o Cajero)
    Label(frame_entradas, text="Rol:", bg="#E6F0FA", font=("Arial", 12)).grid(row=0, column=0, padx=(10, 2), pady=5, sticky="e")
    combo_rol = ttk.Combobox(frame_entradas, textvariable=rol_var, values=["Cajero", "Supervisor"], font=("Arial", 12), state="readonly")
    combo_rol.grid(row=0, column=1, padx=(0, 10), pady=5, sticky="w")
    entradas["Rol:"] = combo_rol

    # tood: Campo para la contraseña
    Label(frame_entradas, text="Contraseña:", bg="#E6F0FA", font=("Arial", 12)).grid(row=1, column=0, padx=(10, 2), pady=5, sticky="e")
    entrada_contraseña = Entry(frame_entradas, font=("Arial", 12), show="*")
    entrada_contraseña.grid(row=1, column=1, padx=(0, 10), pady=5, sticky="w")
    entradas["Contraseña:"] = entrada_contraseña

    # tood: Crear frame para la tabla y el scrollbar
    frame_tabla = Frame(frame_izquierdo, bg="#E6F0FA")
    frame_tabla.pack(padx=10, fill="both", expand=True)

    # tood: Crear el scrollbar vertical
    scrollbar = Scrollbar(frame_tabla, orient="vertical")
    scrollbar.pack(side="right", fill="y")

    # tood: Crear la tabla (Treeview) y asociarla al scrollbar
    tabla = ttk.Treeview(frame_tabla, columns=["Usuario", "Contraseña"], show="headings", height=15, 
                         yscrollcommand=scrollbar.set)
    tabla.heading("Usuario", text="Usuario")
    tabla.heading("Contraseña", text="Contraseña")
    tabla.column("Usuario", width=100)
    tabla.column("Contraseña", width=100)
    tabla.pack(pady=10, fill="both", expand=True)

    # tood: Configurar el scrollbar para controlar el desplazamiento vertical de la tabla
    scrollbar.config(command=tabla.yview)

    usuario_original_var = [None]

    # tood: Manejar la selección de un usuario en la tabla
    def on_select(event):
        select_item = tabla.selection()
        if select_item:
            values = tabla.item(select_item)['values']
            usuario = values[0]
            # Determinar el rol base (Cajero o Supervisor) a partir del nombre de usuario
            if usuario.lower().startswith("cajero"):
                rol_var.set("Cajero")
            elif usuario.lower().startswith("supervisor"):
                rol_var.set("Supervisor")
            else:
                rol_var.set("Cajero")  # Por defecto, si no coincide
            entradas["Contraseña:"].delete(0, 'end')
            entradas["Contraseña:"].insert(0, values[1])
            usuario_original_var[0] = usuario

    tabla.bind('<<TreeviewSelect>>', on_select)

    # tood: Mostrar todos los usuarios en la tabla
    def ver_usuarios():
        config = Configuracion("gerente")
        usuarios = config.obtener_usuarios()
        for row in tabla.get_children():
            tabla.delete(row)
        for usuario, contraseña in usuarios.items():
            if usuario != "gerente":  # Excluir el usuario gerente
                tabla.insert("", "end", values=(usuario, contraseña))

    # tood: Buscar y mostrar usuarios según el texto de búsqueda
    def buscar_y_mostrar():
        usuario = entry_busqueda.get().strip().lower()
        if not usuario:
            ver_usuarios()
            for entrada in entradas.values():
                if entrada != combo_rol:
                    entrada.delete(0, 'end')
            usuario_original_var[0] = None
            return

        config = Configuracion("gerente")
        usuarios = config.obtener_usuarios()
        for row in tabla.get_children():
            tabla.delete(row)
        for entrada in entradas.values():
            if entrada != combo_rol:
                entrada.delete(0, 'end')
        usuario_original_var[0] = None

        if usuario in usuarios and usuario != "gerente":
            contraseña = usuarios[usuario]
            tabla.insert("", "end", values=(usuario, contraseña))
            if usuario.lower().startswith("cajero"):
                rol_var.set("Cajero")
            elif usuario.lower().startswith("supervisor"):
                rol_var.set("Supervisor")
            entradas["Contraseña:"].insert(0, contraseña)
            usuario_original_var[0] = usuario
        else:
            messagebox.showwarning("No encontrado", f"No se encontró el usuario {usuario}")

    # tood: Agregar un nuevo usuario con rol Cajero o Supervisor
    def agregar():
        rol = rol_var.get().strip()
        contraseña = entradas["Contraseña:"].get().strip()

        if not all([rol, contraseña]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        config = Configuracion("gerente")
        usuarios = config.obtener_usuarios()
        
        # tood: Generar un nombre de usuario único (por ejemplo, cajero1, supervisor1)
        base_usuario = rol.lower()
        i = 1
        usuario = f"{base_usuario}{i}"
        while usuario in usuarios:
            i += 1
            usuario = f"{base_usuario}{i}"

        if config.agregar_usuario(usuario, contraseña):
            ver_usuarios()
            limpiar_campos()
            messagebox.showinfo("Éxito", f"Usuario {usuario} agregado correctamente")

    # tood: Eliminar un usuario seleccionado
    def eliminar():
        usuario = usuario_original_var[0]
        if not usuario:
            messagebox.showerror("Error", "Seleccione un usuario para eliminar")
            return

        if usuario.lower() == "gerente":
            messagebox.showerror("Error", "No se puede eliminar el usuario 'gerente'")
            return

        config = Configuracion("gerente")
        if config.eliminar_usuario(usuario):
            ver_usuarios()
            limpiar_campos()
            messagebox.showinfo("Éxito", f"Usuario {usuario} eliminado correctamente")

    # tood: Actualizar la contraseña de un usuario seleccionado
    def actualizar_datos():
        usuario = usuario_original_var[0]
        contraseña = entradas["Contraseña:"].get().strip()

        if not usuario:
            messagebox.showerror("Error", "Seleccione un usuario para actualizar")
            return

        if not contraseña:
            messagebox.showerror("Error", "La contraseña es obligatoria")
            return

        if usuario.lower() == "gerente":
            messagebox.showerror("Error", "No se puede modificar el usuario 'gerente'")
            return

        config = Configuracion("gerente")
        if config.modificar_contraseña(usuario, contraseña):
            ver_usuarios()
            limpiar_campos()
            messagebox.showinfo("Éxito", f"Usuario {usuario} actualizado correctamente")

    # tood: Limpiar todos los campos de entrada
    def limpiar_campos():
        for entrada in entradas.values():
            if entrada != combo_rol:
                entrada.delete(0, 'end')
        entry_busqueda.delete(0, 'end')
        rol_var.set("Cajero")
        usuario_original_var[0] = None

    # tood: Botón para buscar usuarios
    Button(frame_search, text="Buscar", font=("Arial", 10), bg="#2196F3", fg="white",
           command=buscar_y_mostrar).pack(side="left", pady=5, padx=5)

    # tood: Botones para las acciones de agregar, eliminar, actualizar y limpiar
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

    # tood: Cargar los usuarios iniciales en la tabla
    ver_usuarios()

    return frame_principal