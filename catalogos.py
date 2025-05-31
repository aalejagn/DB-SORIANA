from tkinter import Tk, Label, Frame, Entry, Button, ttk, messagebox
from clientes import crear_seccion_clientes
from proveedor import crear_seccion_proveedor
from unidades import crear_seccion_unidades
from categorias import crear_seccion_categorias
from metodo_de_pago import crear_seccion_metodo_de_pago
from empleados import crear_seccion_empleados
from articulos import crear_seccion_articulos
from ventas import crear_seccion_ventas
from configuracion_interfaz import crear_seccion_configuracion
from corte_caja import crear_seccion_corte_de_caja
from historia_venta import crear_seccion_historia_venta
from historial_compras import crear_seccion_historia_compra
from compras import crear_seccion_compras
from configuracion import Configuracion
from PIL import Image, ImageTk

"""
Función de creación de ventana
"""
def creacion_ventana():
    ventana = Tk()
    ventana.title("Punto de venta - Soriana")
    ventana.geometry("1000x700")
    ventana.configure(bg="#E6F0FA")
    return ventana

"""
Creación de presentación de usuarios registrados
"""
def ventana_login(ventana, actualizar=False):
    if actualizar:
        for widget in ventana.winfo_children():
            widget.destroy()

    marco_sombra = Frame(ventana, bg="#87CEEB")
    marco_sombra.pack(expand=True, fill="both")

    # Usamos PIL para cargar la imagen de fondo en formato PNG
    try:
        img = Image.open("logos/Soriana.png")
        img = img.resize((1300, 800), Image.Resampling.LANCZOS)
        background_image = ImageTk.PhotoImage(img)
        background_label = Label(marco_sombra, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        marco_sombra.background_image = background_image
    except Exception as e:
        Label(marco_sombra, text="No se pudo cargar la imagen de fondo", font=("Helvetica", 12), bg="#87CEEB", fg="#F44336").place(relx=0.5, rely=0.1, anchor="center")

    marco_login = Frame(marco_sombra, bg="white", padx=50, pady=50, relief="raised", bd=5, highlightbackground="#ADD8E6", highlightthickness=2)
    marco_login.place(relx=0.5, rely=0.5, anchor="center")
    
    Label(marco_login, text="🛒 SORIANA", font=("Helvetica", 28, "bold"), fg="#1E90FF", bg="white")\
        .grid(row=0, column=0, columnspan=3, pady=(0, 15))
    ttk.Separator(marco_login, orient='horizontal')\
        .grid(row=1, column=0, columnspan=3, sticky="ew", pady=15)
       
    info = "Dirección: LAS GRANJAS AQUI MATAN\nCelular: +52 9613765449\nEmail: ag0013155@gmail.com"
    Label(marco_login, text=info, font=("Helvetica", 12, "italic"), bg="white", justify="center", fg="#555")\
        .grid(row=2, column=0, columnspan=3, pady=(10, 20))
    
    config = Configuracion("gerente")
    usuarios = list(config.obtener_usuarios().keys())
    
    Label(marco_login, text="Seleccione el usuario:", font=("Helvetica", 12, "bold"), bg="white")\
        .grid(row=3, column=0, sticky="e", pady=5, padx=5)
    combo_usuario = ttk.Combobox(marco_login, values=usuarios, font=("Helvetica", 12), state="readonly")
    combo_usuario.grid(row=3, column=1, pady=0, padx=10, ipadx=10, ipady=2)
    if usuarios:
        combo_usuario.set(usuarios[0])
    
    Button(marco_login, text="🔄 Actualizar", font=("Helvetica", 10), bg="#1565C0", fg="white",
           command=lambda: ventana_login(ventana, actualizar=True), relief="flat", activebackground="#0D47A1")\
        .grid(row=3, column=2, pady=5, padx=5)
    
    Label(marco_login, text="Ingrese la contraseña:", font=("Helvetica", 12, "bold"), bg="white")\
        .grid(row=4, column=0, sticky="e", pady=5, padx=0)
    entry_contraseña = Entry(marco_login, font=("Helvetica", 12), show="*")
    entry_contraseña.grid(row=4, column=1, pady=0, padx=10, ipadx=10, ipady=2)
    
    Button(marco_login, text="🚀 Ingresar", font=("Helvetica", 13, "bold"), bg="#4CAF50", fg="white", width=15,
           command=lambda: validar_usuarios(combo_usuario.get(), entry_contraseña.get(), ventana, marco_sombra),
           relief="flat", activebackground="#388E3C")\
        .grid(row=5, column=0, columnspan=3, pady=25)

"""
Creamos la función de validar datos para usuarios
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
Creación de lado lateral para los botones
"""
"""
Creación de lado lateral para los botones
"""
def barra_lateral(ventana, usuario):
    barra_lateral = Frame(ventana, bg="#1E88E5", width=250)
    barra_lateral.pack(side="left", fill="y")

    frame_superior = Frame(barra_lateral, bg="#1E88E5")
    frame_superior.pack(fill="x", pady=15, padx=15)
    
    # Determinar el tipo de usuario
    usuario = usuario.lower()
    if usuario == "gerente":
        tipo_usuario = "Gerente"
    elif usuario.startswith("supervisor"):
        tipo_usuario = "Supervisor"
    else:
        tipo_usuario = "Trabajador"
    
    Label(frame_superior, text=f"👤 {tipo_usuario}", font=("Helvetica", 16, "bold"), bg="#1E88E5", fg="white").pack()

    # Definimos opciones según el tipo de usuario
    if tipo_usuario == "Trabajador":
        opciones = ["Ventas", "Historial de Ventas"]
    elif tipo_usuario == "Supervisor":
        opciones = ["Ventas", "Historial de Ventas", "Compras", "Historial de Compras", "Corte de Caja"]
    else:  # Gerente
        opciones = ["Ventas", "Compras", "Clientes", "Proveedor", "Unidades", "Categorias", "Metodo de pago", "Articulos", "Historial de Ventas", "Historial de Compras", "Corte de Caja", "Empleado", "Configuración"]

    funciones = {
        "Ventas": lambda: crear_seccion_ventas(ventana, barra_lateral, usuario),
        "Compras": lambda: manejo_compras(ventana, tipo_usuario, barra_lateral, usuario),
        "Clientes": lambda: manejo_clientes(ventana, tipo_usuario, barra_lateral),
        "Proveedor": lambda: crear_seccion_proveedor(ventana, barra_lateral),
        "Unidades": lambda: crear_seccion_unidades(ventana, barra_lateral),
        "Categorias": lambda: crear_seccion_categorias(ventana, barra_lateral),
        "Metodo de pago": lambda: crear_seccion_metodo_de_pago(ventana, barra_lateral),
        "Articulos": lambda: crear_seccion_articulos(ventana, barra_lateral),
        "Historial de Ventas": lambda: manejo_historia_venta(ventana, tipo_usuario, barra_lateral),
        "Historial de Compras": lambda: manejo_historia_compra(ventana, tipo_usuario, barra_lateral),
        "Corte de Caja": lambda: crear_seccion_corte_de_caja(ventana, barra_lateral),
        "Empleado": lambda: manejo_empleados(ventana, tipo_usuario, barra_lateral),
        "Configuración": lambda: manejo_configuracion(ventana, tipo_usuario, barra_lateral)
    }
    
    for opcion in opciones:
        Button(barra_lateral, text=f"📋 {opcion}", bg="#1565C0", fg="white", width=20,
               font=("Helvetica", 12), command=funciones.get(opcion, lambda: None),
               relief="flat", activebackground="#0D47A1", activeforeground="white")\
            .pack(pady=5, padx=20)

    Button(barra_lateral, text="🚪 Cerrar Sesión", bg="#F44336", fg="white", width=20,
           font=("Helvetica", 12), command=lambda: cerrar_sesion(ventana),
           relief="flat", activebackground="#D32F2F", activeforeground="white")\
        .pack(pady=10, padx=20, side="bottom")

    main_frame = Frame(ventana, bg="#E6F0FA")
    main_frame.pack(expand=True, fill="both")

    title_frame = Frame(main_frame, bg="#E6F0FA")
    title_frame.pack(pady=20)

    try:
        logo_img = Image.open("logos/log.png")
        logo_img = logo_img.resize((200, 100), Image.Resampling.LANCZOS)
        logo_image = ImageTk.PhotoImage(logo_img)
        Label(title_frame, image=logo_image, bg="#E6F0FA").pack(pady=10)
        title_frame.logo_image = logo_image
    except Exception as e:
        Label(title_frame, text="No se pudo cargar la imagen", font=("Helvetica", 12), bg="#E6F0FA", fg="#F44336").pack(pady=10)

    separator = ttk.Separator(title_frame, orient='horizontal')
    separator.pack(fill="x", expand=True, pady=10)
    style = ttk.Style()
    style.configure("TSeparator", background="black", thickness=2)

    Label(title_frame, text="DB_SORIANA", font=("Helvetica", 28, "bold"), bg="#E6F0FA", fg="#D4A017", justify="center")\
        .pack()
    Label(title_frame, text="Sistema Moderno y Eficiente", font=("Helvetica", 14, "italic"), bg="#E6F0FA", fg="#555", justify="center")\
        .pack()

    caracteristicas = [
        ("⏱️ Rápido y fácil de usar", "#32CD32"),
        ("📊 Control de articulos en tiempo real", "#32CD32"),
        ("📈 Reportes detallados de ventas", "#32CD32"),
        ("👥 Gestión de clientes y proveedores", "#32CD32")
    ]

    for texto, color in caracteristicas:
        frame_caracteristica = Frame(main_frame, bg="#E6F0FA")
        frame_caracteristica.pack(fill="x", padx=40)
        Label(frame_caracteristica, text=texto[0], font=("Helvetica", 12), fg=color, bg="#E6F0FA").pack(side="left", padx=5)
        Label(frame_caracteristica, text=texto[1:], font=("Helvetica", 12), fg="black", bg="#E6F0FA", justify="center").pack()

    Button(main_frame, text="🚀 ¡COMENZAR AHORA!", font=("Helvetica", 16, "bold"), bg="#1565C0", fg="white", width=25,
           command=lambda: manejo_clientes(ventana, tipo_usuario, barra_lateral),
           relief="flat", activebackground="#0D47A1", activeforeground="white", bd=0, padx=10, pady=5)\
        .pack(pady=40)
    


"""
Función para cerrar sesión y volver al login
"""
def cerrar_sesion(ventana):
    for widget in ventana.winfo_children():
        widget.destroy()
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

    Label(main_frame, text="DB_SORIANA", font=("Helvetica", 24, "bold"), bg="#E6F0FA", fg="#D4A017").pack(pady=10)
    Label(main_frame, text=f"Tipo de usuario: {tipo_usuario}", font=("Helvetica", 12), bg="#E6F0FA", fg="#555").pack()

    frame_clientes = crear_seccion_clientes(main_frame, barra_lateral)
    frame_clientes.pack(pady=10, fill="both", expand=True)

"""
Manejo de la sección de historial de ventas (accesible para todos)
"""
def manejo_historia_venta(ventana, tipo_usuario, barra_lateral):
    for widget in ventana.winfo_children():
        if widget != barra_lateral:
            widget.destroy()

    main_frame = Frame(ventana, bg="#E6F0FA")
    main_frame.pack(expand=True, fill="both")

    Label(main_frame, text="DB_SORIANA", font=("Helvetica", 24, "bold"), bg="#E6F0FA", fg="#D4A017").pack(pady=10)
    Label(main_frame, text=f"Tipo de usuario: {tipo_usuario}", font=("Helvetica", 12), bg="#E6F0FA", fg="#555").pack()

    frame_historia = crear_seccion_historia_venta(ventana, barra_lateral)
    frame_historia.pack(pady=10, fill="both", expand=True)

"""
Manejo de la sección de historial de compras (accesible para Gerente)
"""
def manejo_historia_compra(ventana, tipo_usuario, barra_lateral):
    for widget in ventana.winfo_children():
        if widget != barra_lateral:
            widget.destroy()

    main_frame = Frame(ventana, bg="#E6F0FA")
    main_frame.pack(expand=True, fill="both")

    Label(main_frame, text="DB_SORIANA", font=("Helvetica", 24, "bold"), bg="#E6F0FA", fg="#D4A017").pack(pady=10)
    Label(main_frame, text=f"Tipo de usuario: {tipo_usuario}", font=("Helvetica", 12), bg="#E6F0FA", fg="#555").pack()

    if tipo_usuario in ["Gerente", "Supervisor"]:
        frame_historia = crear_seccion_historia_compra(ventana, barra_lateral)
        frame_historia.pack(pady=10, fill="both", expand=True)
    else:
        Label(main_frame, text="Acceso restringido: Solo Gerentes y Supervisores pueden ver el historial de compras.",
              font=("Helvetica", 12), bg="#E6F0FA", fg="#F44336").pack(pady=10)

"""
Manejo de acceso restringido para empleados
"""
def manejo_empleados(ventana, tipo_usuario, barra_lateral):
    for widget in ventana.winfo_children():
        if widget != barra_lateral:
            widget.destroy()

    main_frame = Frame(ventana, bg="#E6F0FA")
    main_frame.pack(expand=True, fill="both")

    Label(main_frame, text="DB_SORIANA", font=("Helvetica", 24, "bold"), bg="#E6F0FA", fg="#D4A017").pack(pady=10)
    Label(main_frame, text=f"Tipo de usuario: {tipo_usuario}", font=("Helvetica", 12), bg="#E6F0FA", fg="#555").pack()

    if tipo_usuario == "Gerente":
        frame_empleados = crear_seccion_empleados(main_frame, barra_lateral)
        frame_empleados.pack(pady=10, fill="both", expand=True)
    else:
        Label(main_frame, text="Acceso restringido: Solo Gerentes pueden gestionar empleados.",
              font=("Helvetica", 12), bg="#E6F0FA", fg="#F44336").pack(pady=10)


"""Manejo de la seccion de compras"""
"""
Manejo de la sección de compras (accesible para Gerente)
"""
def manejo_compras(ventana, tipo_usuario, barra_lateral, usuario):
    for widget in ventana.winfo_children():
        if widget != barra_lateral:
            widget.destroy()

    main_frame = Frame(ventana, bg="#E6F0FA")
    main_frame.pack(expand=True, fill="both")

    Label(main_frame, text="DB_SORIANA", font=("Helvetica", 24, "bold"), bg="#E6F0FA", fg="#D4A017").pack(pady=10)
    Label(main_frame, text=f"Tipo de usuario: {tipo_usuario}", font=("Helvetica", 12), bg="#E6F0FA", fg="#555").pack()

    if tipo_usuario in ["Gerente", "Supervisor"]:
        frame_compras = crear_seccion_compras(ventana, barra_lateral, usuario)
        frame_compras.pack(pady=10, fill="both", expand=True)
    else:
        Label(main_frame, text="Acceso restringido: Solo Gerentes y Supervisores pueden gestionar compras.",
              font=("Helvetica", 12), bg="#E6F0FA", fg="#F44336").pack(pady=10)



"""
Manejo de la sección de configuración (solo para Gerente)
"""
def manejo_configuracion(ventana, tipo_usuario, barra_lateral):
    for widget in ventana.winfo_children():
        if widget != barra_lateral:
            widget.destroy()

    main_frame = Frame(ventana, bg="#E6F0FA")
    main_frame.pack(expand=True, fill="both")

    Label(main_frame, text="DB_SORIANA", font=("Helvetica", 24, "bold"), bg="#E6F0FA", fg="#D4A017").pack(pady=10)
    Label(main_frame, text=f"Tipo de usuario: {tipo_usuario}", font=("Helvetica", 12), bg="#E6F0FA", fg="#555").pack()

    if tipo_usuario == "Gerente":
        frame_titulo_submenu = Frame(main_frame, bg="#E6F0FA")
        frame_titulo_submenu.pack(fill="x", pady=10)

        Label(frame_titulo_submenu, text="⚙️ Configuración", font=("Helvetica", 18, "bold"), bg="#E6F0FA", fg="#2E86C1").pack()

        frame_submenu = Frame(frame_titulo_submenu, bg="#E6F0FA")
        frame_submenu.pack(pady=10)

        frame_contenido = Frame(main_frame, bg="#E6F0FA")
        frame_contenido.pack(expand=True, fill="both", padx=20, pady=10)

        def cargar_interfaz(interfaz_func):
            for widget in frame_contenido.winfo_children():
                widget.destroy()
            interfaz_func(frame_contenido, barra_lateral, ventana)

        Button(frame_submenu, text="👤 Configuración Usuarios", font=("Helvetica", 12), bg="#1565C0", fg="white", width=20,
               command=lambda: cargar_interfaz(crear_seccion_configuracion),
               relief="flat", activebackground="#0D47A1", activeforeground="white")\
            .pack(side="left", padx=10)
    else:
        Label(main_frame, text="Acceso restringido: Solo Gerentes pueden acceder a la configuración.",
              font=("Helvetica", 12), bg="#E6F0FA", fg="#F44336").pack(pady=10)

ventana = creacion_ventana()
ventana_login(ventana)
ventana.mainloop()