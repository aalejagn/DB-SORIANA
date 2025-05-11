from tkinter import Tk, Label, Frame, Entry, Button, ttk, messagebox
from clientes import crear_seccion_clientes
from proveedor import crear_seccion_proveedor
from unidades import crear_seccion_unidades
from categorias import crear_seccion_categorias
from metodo_de_pago import crear_seccion_metodo_de_pago
from empleados import crear_seccion_empleados
from configuracion_interfaz import crear_seccion_configuracion, crear_seccion_exportar_base_datos
from configuracion import Configuracion

"""
Funcion de creacion de ventana
"""
def creacion_ventana():
    ventana = Tk()
    ventana.title("Punto de venta - Soriana")
    ventana.geometry("800x600")
    ventana.configure(bg="#E6F0FA")
    return ventana

"""
Creacion de presentacion de usuarios registrados
"""
def ventana_login(ventana, actualizar=False):
    # Clear existing widgets
    if actualizar:
        for widget in ventana.winfo_children():
            widget.destroy()

    marco_sombra = Frame(ventana, bg="#80C4DE")
    marco_sombra.pack(expand=True, fill="both")

    marco_login = Frame(marco_sombra, bg="white", padx=40, pady=40, relief="raised", bd=2)
    marco_login.place(relx=0.5, rely=0.5, anchor="center")
    
    Label(marco_login, text="🛒 SORIANA", font=("Arial", 24, "bold"), fg="#1E90FF", bg="white")\
        .grid(row=0, column=0, columnspan=3, pady=(0,10))
    ttk.Separator(marco_login, orient='horizontal')\
        .grid(row=1, column=0, columnspan=3, sticky="ew", pady=10)
       
    info = "Dirección: LAS GRANJAS AQUI MATAN\nCelular: +52 9613765449\nEmail: ag0013155@gmail.com"
    Label(marco_login, text=info, font=("Arial", 12), bg="white", justify="center")\
        .grid(row=2, column=0, columnspan=3, pady=(10))
    
    # Obtener lista de usuarios para el combobox
    config = Configuracion("gerente")  # Usamos un usuario temporal para obtener la lista
    usuarios = list(config.obtener_usuarios().keys())
    
    Label(marco_login, text="Seleccione el usuario:", font=("Arial", 12), bg="white")\
        .grid(row=3, column=0, sticky="e", pady=5, padx=5)
    combo_usuario = ttk.Combobox(marco_login, values=usuarios, font=("Arial", 12), state="readonly")
    combo_usuario.grid(row=3, column=1, pady=0, padx=10, ipadx=10, ipady=2)
    if usuarios:
        combo_usuario.set(usuarios[0])  # Seleccionar el primer usuario por defecto
    
    # Botón para actualizar la lista de usuarios
    Button(marco_login, text="Actualizar", font=("Arial", 10), bg="#2196F3", fg="white",
           command=lambda: ventana_login(ventana, actualizar=True))\
        .grid(row=3, column=2, pady=5, padx=5)
    
    Label(marco_login, text="Ingrese la contraseña:", font=("Arial", 12), bg="white")\
        .grid(row=4, column=0, sticky="e", pady=5, padx=5)
    entry_contraseña = Entry(marco_login, font=("Arial", 12), show="*")
    entry_contraseña.grid(row=4, column=1, pady=0, padx=5, ipadx=18, ipady=2, columnspan=2)
    
    Button(marco_login, text="Ingresar", font=("Arial", 13), bg="#4CAF50", fg="white", width=15,
           command=lambda: validar_usuarios(combo_usuario.get(), entry_contraseña.get(), ventana, marco_sombra))\
        .grid(row=5, column=0, columnspan=3, pady=20)

"""
Creamos la funcion de validar datos para usuarios
"""
def validar_usuarios(usuario, contraseña, ventana, marco_sombra):
    if not usuario:
        messagebox.showerror("Error", "Por favor, seleccione un usuario")
        return
    config = Configuracion(usuario.lower())
    if config.verificar_credenciales(usuario.lower(), contraseña):
        marco_sombra.destroy()
        barra_lateral(ventana, usuario.lower())
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

"""
Creacion de lado lateral para los botones
"""
def barra_lateral(ventana, usuario):
    barra_lateral = Frame(ventana, bg="#D3D3D3", width=200)
    barra_lateral.pack(side="left", fill="y")

    """Frame para el rol y el boton de salir"""
    frame_superior = Frame(barra_lateral, bg="#D3D3D3")
    frame_superior.pack(fill="x", pady=10, padx=10)
    
    # Rol
    tipo_usuario = "Gerente" if usuario.lower() == "gerente" else "Trabajador"
    Label(frame_superior, text=f"{tipo_usuario}", font=("Arial", 14, "bold"), bg="#DEDEDE").pack()

    # Opciones base disponibles para todos
    opciones = ["Clientes", "Proveedor", "Unidades", "Categorias", "Metodo de pago"]
    
    # Agregar "Empleado" y "Configuración" solo si el usuario es Gerente
    if tipo_usuario == "Gerente":
        opciones.extend(["Empleado", "Configuración"])

    funciones = {
        "Clientes": lambda: manejo_clientes(ventana, tipo_usuario, barra_lateral),
        "Proveedor": lambda: crear_seccion_proveedor(ventana, barra_lateral),
        "Unidades": lambda: crear_seccion_unidades(ventana, barra_lateral),
        "Categorias": lambda: crear_seccion_categorias(ventana, barra_lateral),
        "Metodo de pago": lambda: crear_seccion_metodo_de_pago(ventana, barra_lateral),
        "Empleado": lambda: manejo_empleados(ventana, tipo_usuario, barra_lateral),
        "Configuración": lambda: manejo_configuracion(ventana, tipo_usuario, barra_lateral)
    }
    
    for opcion in opciones:
        Button(barra_lateral, text=opcion, bg="#4682B4", fg="white", width=20,
               font=("Arial", 12), command=funciones.get(opcion, lambda: None)).pack(pady=5, padx=10)

    # Botón para cerrar sesión
    Button(barra_lateral, text="Cerrar Sesión", bg="#F44336", fg="white", width=20,
           font=("Arial", 12), command=lambda: cerrar_sesion(ventana))\
        .pack(pady=5, padx=10, side="bottom")

    main_frame = Frame(ventana, bg="#E6F0FA")
    main_frame.pack(expand=True, fill="both")
    Label(main_frame, text="PUNTO DE VENTA", font=("Arial", 20, "bold"), bg="#E6F0FA").pack(pady=20)
    Label(main_frame, text="Sistema Moderno y Eficiente", font=("Arial", 14), bg="#E6F0FA").pack(pady=10)

    caracteristicas = [
        "Rápido y fácil de usar",
        "Control de inventario en tiempo real",
        "Reportes detallados de ventas",
        "Gestión de clientes y proveedores"
    ]

    for texto in caracteristicas:
        frame_caracteristica = Frame(main_frame, bg="#E6F0FA")
        frame_caracteristica.pack(fill="x", padx=20)
        Label(frame_caracteristica, text="●", font=("Arial", 12), fg="#32CD32", bg="#E6F0FA").pack(side="left")
        Label(frame_caracteristica, text=texto, font=("Arial", 12), fg="black", bg="#E6F0FA").pack(side="left")

    Button(main_frame, text="¡COMENZAR AHORA!", font=("Arial", 14, "bold"), bg="#FFA500", fg="white", width=20,
           command=lambda: manejo_clientes(ventana, tipo_usuario, barra_lateral)).pack(pady=30)

"""
Función para cerrar sesión y volver al login
"""
def cerrar_sesion(ventana):
    # Destroy all widgets in the window
    for widget in ventana.winfo_children():
        widget.destroy()
    # Reload the login screen with updated user list
    ventana_login(ventana, actualizar=True)

"""
Manejo de la sección de clientes (accesible para todos)
"""
def manejo_clientes(ventana, tipo_usuario, barra_lateral):
    for widget in ventana.winfo_children():
        if widget != barra_lateral:
            widget.destroy()

    main_frame = Frame(ventana, bg="#E6F0FA")
    main_frame.pack(expand=True, fill="both")

    Label(main_frame, text="PUNTO DE VENTA", font=("Arial", 20, "bold"), bg="#E6F0FA").pack(pady=10)
    Label(main_frame, text=f"Tipo de usuario: {tipo_usuario}", font=("Arial", 12), bg="#E6F0FA").pack()

    frame_clientes = crear_seccion_clientes(main_frame, barra_lateral)
    frame_clientes.pack(pady=10, fill="both", expand=True)

"""
Manejo de acceso restringido para empleados
"""
def manejo_empleados(ventana, tipo_usuario, barra_lateral):
    for widget in ventana.winfo_children():
        if widget != barra_lateral:
            widget.destroy()

    main_frame = Frame(ventana, bg="#E6F0FA")
    main_frame.pack(expand=True, fill="both")

    Label(main_frame, text="PUNTO DE VENTA", font=("Arial", 20, "bold"), bg="#E6F0FA").pack(pady=10)
    Label(main_frame, text=f"Tipo de usuario: {tipo_usuario}", font=("Arial", 12), bg="#E6F0FA").pack()

    if tipo_usuario == "Gerente":
        frame_empleados = crear_seccion_empleados(main_frame, barra_lateral)
        frame_empleados.pack(pady=10, fill="both", expand=True)
    else:
        Label(main_frame, text="Acceso restringido: Solo Gerentes pueden gestionar empleados.",
              font=("Arial", 12), bg="#E6F0FA").pack(pady=10)

"""
Manejo de la sección de configuración (solo para Gerente)
"""
def manejo_configuracion(ventana, tipo_usuario, barra_lateral):
    for widget in ventana.winfo_children():
        if widget != barra_lateral:
            widget.destroy()

    main_frame = Frame(ventana, bg="#E6F0FA")
    main_frame.pack(expand=True, fill="both")

    # Título principal
    Label(main_frame, text="PUNTO DE VENTA", font=("Arial", 20, "bold"), bg="#E6F0FA").pack(pady=10)
    Label(main_frame, text=f"Tipo de usuario: {tipo_usuario}", font=("Arial", 12), bg="#E6F0FA").pack()

    if tipo_usuario == "Gerente":
        # Frame para el título y el submenú
        frame_titulo_submenu = Frame(main_frame, bg="#E6F0FA")
        frame_titulo_submenu.pack(fill="x", pady=10)

        # Título "Configuración"
        Label(frame_titulo_submenu, text="Configuración", font=("Arial", 16, "bold"), bg="#E6F0FA").pack()

        # Frame para los botones del submenú (alineados horizontalmente)
        frame_submenu = Frame(frame_titulo_submenu, bg="#E6F0FA")
        frame_submenu.pack(pady=10)

        # Frame donde se cargarán las interfaces
        frame_contenido = Frame(main_frame, bg="#E6F0FA")
        frame_contenido.pack(expand=True, fill="both", padx=10, pady=10)

        # Función para limpiar el frame_contenido y cargar una nueva interfaz
        def cargar_interfaz(interfaz_func):
            for widget in frame_contenido.winfo_children():
                widget.destroy()
            interfaz_func(frame_contenido, barra_lateral, ventana)  # Pass the root window

        # Botones alineados horizontalmente
        Button(frame_submenu, text="Configuración Usuarios", font=("Arial", 12), bg="#2196F3", fg="white", width=20,
               command=lambda: cargar_interfaz(crear_seccion_configuracion)).pack(side="left", padx=5)
        Button(frame_submenu, text="Exportar Base de Datos", font=("Arial", 12), bg="#2196F3", fg="white", width=20,
               command=lambda: cargar_interfaz(crear_seccion_exportar_base_datos)).pack(side="left", padx=5)

    else:
        Label(main_frame, text="Acceso restringido: Solo Gerentes pueden acceder a la configuración.",
              font=("Arial", 12), bg="#E6F0FA").pack(pady=10)

ventana = creacion_ventana()
ventana_login(ventana)
ventana.mainloop()