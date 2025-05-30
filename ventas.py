from tkinter import Tk, Label, Frame, Entry, Button, ttk, messagebox, StringVar, Toplevel
from db_soriana import buscar_articulo, agregar_venta, buscar_metodo_de_pago, obtener_conexion, buscar_cliente, agregar_cliente
import mysql.connector
from datetime import datetime

# Clase para manejar el estado de la venta
class VentaEstado:
    def __init__(self):
        self.articulos = []
        self.total = "0.00"
        self.usuario = "cajero1"
        self.ultima_venta = None  # Almacena los datos de la última venta

# Instancia global del estado de la venta
venta_estado = VentaEstado()

# Declarar variables globales para la interfaz
entry_codigo = None
entry_cantidad = None
metodo_pago_var = None
combo_metodo_pago = None
entry_usuario = None
entry_telefono = None
tabla = None
total_var = None
pago_con = None
cambio = None
btn_ticket = None
cliente_info_label = None  # Label para mostrar info del cliente

def hay_corte_de_caja():
    conexion = obtener_conexion()
    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos para verificar el corte de caja.")
        return True
    try:
        cursor = conexion.cursor()
        query = "SELECT COUNT(*) FROM cortes_de_caja WHERE DATE(fecha) = %s"
        today = datetime.now().date()
        cursor.execute(query, (today,))
        count = cursor.fetchone()[0]
        return count > 0
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error al verificar el corte de caja: {e}")
        return True
    finally:
        cursor.close()
        conexion.close()

def generar_ticket():
    global venta_estado
    
    # Verificar si hay datos de la última venta
    if not venta_estado.ultima_venta or not venta_estado.ultima_venta["articulos"]:
        messagebox.showerror("Error", "No hay datos de venta para generar el ticket. Confirme una venta primero.")
        return
    
    # Crear ventana emergente para el ticket
    ventana_ticket = Toplevel()
    ventana_ticket.title("Ticket de Venta - Soriana")
    ventana_ticket.geometry("350x600")
    ventana_ticket.resizable(False, False)
    
    # Frame para el contenido del ticket
    frame_ticket = Frame(ventana_ticket, bg="#FFFFFF")
    frame_ticket.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Fuentes para el ticket
    font_titulo = ("Arial", 14, "bold")
    font_normal = ("Arial", 10)
    font_destacado = ("Arial", 12, "bold")
    
    # Encabezado del ticket con dirección, teléfono y emoji
    Label(frame_ticket, text="SORIANA 🛒", font=font_titulo, bg="#FFFFFF").pack(pady=5)
    Label(frame_ticket, text="Blvd. Ángel Albino Corzo y Blvd.Andrés#250", font=font_normal, bg="#FFFFFF").pack()
    Label(frame_ticket, text="Tel: 961 3765449", font=font_normal, bg="#FFFFFF").pack()
    Label(frame_ticket, text=f"Folio: T-{datetime.now().strftime('%Y%m%d%H%M%S')}", font=font_normal, bg="#FFFFFF").pack()
    Label(frame_ticket, text=f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", font=font_normal, bg="#FFFFFF").pack()
    
    # Información del cliente
    telefono = venta_estado.ultima_venta["telefono"]
    print(f"Debug: Telefono en ultima_venta: {telefono}")  # Debug
    if telefono:
        cliente = buscar_cliente("telefono", telefono)
        print(f"Debug: Resultado de buscar_cliente: {cliente}")  # Debug
        if cliente:  # Expecting a tuple like ('José', 'García Torres', ...)
            cliente_info = f"{cliente[0]} {cliente[1]}"  # Nombre y apellidos
            Label(frame_ticket, text=f"Cliente: {cliente_info}", font=font_normal, bg="#FFFFFF").pack()
            Label(frame_ticket, text=f"Teléfono: {telefono}", font=font_normal, bg="#FFFFFF").pack()
        else:
            Label(frame_ticket, text="Cliente: No encontrado", font=font_normal, bg="#FFFFFF").pack()
            Label(frame_ticket, text=f"Teléfono: {telefono}", font=font_normal, bg="#FFFFFF").pack()
    
    # Separador
    Label(frame_ticket, text="=" * 40, font=font_normal, bg="#FFFFFF").pack(pady=5)
    Label(frame_ticket, text="ARTÍCULOS", font=font_titulo, bg="#FFFFFF").pack()
    
    # Lista de productos: Nombre, Costo, Cantidad, Importe
    for item in venta_estado.ultima_venta["articulos"]:
        nombre = item[1]  # Nombre del producto
        costo = float(item[2])  # Precio unitario
        cantidad = int(item[3])  # Cantidad
        importe = float(item[4])  # Subtotal
        Label(frame_ticket, text=f"{nombre}", font=font_normal, bg="#FFFFFF").pack(anchor="w")
        Label(frame_ticket, text=f"{cantidad} x ${costo:.2f} = ${importe:.2f}", font=font_normal, bg="#FFFFFF").pack(anchor="w")
    
    # Separador
    Label(frame_ticket, text="=" * 40, font=font_normal, bg="#FFFFFF").pack(pady=5)
    
    # Totales
    Label(frame_ticket, text=f"TOTAL: ${venta_estado.ultima_venta['total']}", font=font_destacado, bg="#FFFFFF").pack()
    Label(frame_ticket, text=f"PAGO CON: ${venta_estado.ultima_venta['pago_con']:.2f}", font=font_destacado, bg="#FFFFFF").pack()
    Label(frame_ticket, text=f"CAMBIO: ${venta_estado.ultima_venta['cambio']:.2f}", font=font_destacado, bg="#FFFFFF").pack()
    
    # Pie del ticket
    Label(frame_ticket, text="¡GRACIAS POR SU COMPRA!", font=font_titulo, bg="#FFFFFF").pack(pady=10)
    Label(frame_ticket, text="Vuelva pronto", font=font_normal, bg="#FFFFFF").pack()
    
    # Botón para cerrar la ventana del ticket
    Button(frame_ticket, text="Cerrar", font=font_normal, bg="#F44336", fg="white", command=ventana_ticket.destroy).pack(pady=10)
    
    ventana_ticket.grab_set()

def crear_seccion_ventas(ventana, barra_lateral, usuario):
    global entry_codigo, entry_cantidad, metodo_pago_var, combo_metodo_pago, entry_usuario, entry_telefono, tabla, total_var, pago_con, cambio, btn_ticket, cliente_info_label

    campos = ["Código", "Nombre", "Precio", "Cantidad", "Subtotal", "Método de Pago"]

    if barra_lateral:
        for widget in ventana.winfo_children():
            if widget != barra_lateral:
                widget.destroy()

    frame_principal = Frame(ventana, bg="#E6F0FA")
    frame_principal.pack(expand=True, fill="both")

    frame_centrado = Frame(frame_principal, bg="#E6F0FA")
    frame_centrado.pack(expand=True, fill="both", padx=10, pady=10)

    frame_izquierdo = Frame(frame_centrado, bg="#E6F0FA")
    frame_izquierdo.pack(side="left", expand=True, fill="both")

    frame_derecho = Frame(frame_centrado, bg="#E6F0FA", width=150)
    frame_derecho.pack(side="right", fill="y", padx=10)

    Label(frame_izquierdo, text="Ventas", font=("Arial", 16, "bold"), bg="#E6F0FA").pack(pady=10)

    frame_search = Frame(frame_izquierdo, bg="#E6F0FA")
    frame_search.pack(fill="x", pady=5)
    Label(frame_search, text="Código:", bg="#E6F0FA", font=("Arial", 12)).pack(side="left", padx=(10, 2))
    entry_codigo = Entry(frame_search, font=("Arial", 12), width=20)
    entry_codigo.pack(side="left", padx=(0, 10))
    Label(frame_search, text="Cantidad:", bg="#E6F0FA", font=("Arial", 12)).pack(side="left", padx=(10, 2))
    entry_cantidad = Entry(frame_search, font=("Arial", 12), width=5)
    entry_cantidad.pack(side="left", padx=(0, 10))
    entry_cantidad.insert(0, "1")
    btn_agregar = Button(frame_search, text="Agregar", font=("Arial", 10), bg="#2196F3", fg="white",
                         command=lambda: buscar_y_mostrar())
    btn_agregar.pack(side="left", padx=5)

    frame_pago = Frame(frame_izquierdo, bg="#E6F0FA")
    frame_pago.pack(fill="x", pady=5)
    Label(frame_pago, text="Método de Pago:", bg="#E6F0FA", font=("Arial", 12)).pack(side="left", padx=(10, 2))
    metodo_pago_var = StringVar()
    combo_metodo_pago = ttk.Combobox(frame_pago, textvariable=metodo_pago_var, font=("Arial", 12), state="readonly", width=15)
    combo_metodo_pago.pack(side="left", padx=(0, 10))
    Label(frame_pago, text="Usuario:", bg="#E6F0FA", font=("Arial", 12)).pack(side="left", padx=(10, 2))
    entry_usuario = Entry(frame_pago, font=("Arial", 12), width=15)
    entry_usuario.pack(side="left", padx=(0, 10))
    entry_usuario.insert(0, venta_estado.usuario)
    Label(frame_pago, text="Teléfono:", bg="#E6F0FA", font=("Arial", 12)).pack(side="left", padx=(10, 2))
    entry_telefono = Entry(frame_pago, font=("Arial", 12), width=15)
    entry_telefono.pack(side="left", padx=(0, 10))
    cliente_info_label = Label(frame_pago, text="", bg="#E6F0FA", font=("Arial", 12))
    cliente_info_label.pack(side="left", padx=(10, 2))

    # Define buscar_cliente_por_telefono before using it
    def buscar_cliente_por_telefono(event=None):
        print(f"Debug: Evento disparado: {event}")  # Debug to confirm event
        telefono = entry_telefono.get().strip()
        print(f"Debug: Iniciar búsqueda de cliente con teléfono: {telefono}")  # Debug
        if not telefono:
            cliente_info_label.config(text="")
            print("Debug: Teléfono vacío, limpiando etiqueta")
            return
        cliente = buscar_cliente("telefono", telefono)
        print(f"Debug: Buscar cliente por teléfono {telefono}: {cliente}")  # Debug
        if cliente:  # Expecting a tuple like ('José', 'García Torres', ...)
            cliente_info = f"{cliente[0]} {cliente[1]} - {cliente[2]}"  # Nombre, Apellidos, Teléfono
            cliente_info_label.config(text=cliente_info)
            print(f"Debug: Cliente encontrado, actualizando etiqueta a: {cliente_info}")
        else:
            cliente_info_label.config(text="Cliente no encontrado")
            print(f"Debug: Cliente no encontrado para teléfono {telefono}")

    # Now create the button and bindings
    btn_buscar_cliente = Button(frame_pago, text="Buscar Cliente", font=("Arial", 10), bg="#4CAF50", fg="white",
                                command=buscar_cliente_por_telefono)
    btn_buscar_cliente.pack(side="left", padx=(5, 10))
    entry_telefono.bind("<FocusOut>", buscar_cliente_por_telefono)
    entry_telefono.bind("<Return>", buscar_cliente_por_telefono)

    def toggle_pago_con_entry(*args):
        """Habilita o deshabilita el campo 'Pago con' según el método de pago seleccionado."""
        metodo_seleccionado = metodo_pago_var.get()
        if not metodo_seleccionado:
            pago_con.config(state="normal")
            return
        metodo_nombre = metodo_seleccionado.split(" - ")[1].strip()
        if metodo_nombre in ["Tarjeta de Crédito", "Tarjeta de Débito"]:
            pago_con.config(state="disabled")
            pago_con.delete(0, "end")
            cambio.config(state="normal")
            cambio.delete(0, "end")
            cambio.insert(0, "0.00")
            cambio.config(state="readonly")
        else:
            pago_con.config(state="normal")

    def cargar_metodos_pago():
        conexion = obtener_conexion()
        if not conexion:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos para cargar los métodos de pago.")
            return
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id_metodo, tipo FROM metodo_de_pago")
            metodos = cursor.fetchall()
            if not metodos:
                messagebox.showwarning("Advertencia", "No hay métodos de pago registrados.")
                combo_metodo_pago['values'] = []
                metodo_pago_var.set("")
                return
            opciones = [f"{metodo[0]} - {metodo[1]}" for metodo in metodos]
            combo_metodo_pago['values'] = opciones
            metodo_pago_var.set(opciones[0] if opciones else "")
            # Vincular la función toggle_pago_con_entry al cambio de método de pago
            metodo_pago_var.trace("w", toggle_pago_con_entry)
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al cargar los métodos de pago: {e}")
        finally:
            cursor.close()
            conexion.close()

    cargar_metodos_pago()
    entry_codigo.focus_set()

    frame_tabla = Frame(frame_izquierdo, bg="#E6F0FA")
    frame_tabla.pack(padx=10, fill="both", expand=True)
    tabla = ttk.Treeview(frame_tabla, columns=campos, show="headings", height=12)
    for col in campos:
        tabla.heading(col, text=col)
        tabla.column(col, width=100)
    tabla.pack(pady=10, fill="both", expand=True)

    for articulo in venta_estado.articulos:
        tabla.insert("", "end", values=articulo)

    def on_select(event):
        selected_item = tabla.selection()
        if selected_item:
            values = tabla.item(selected_item)['values']
            entry_codigo.delete(0, 'end')
            entry_codigo.insert(0, values[0])
            entry_cantidad.delete(0, 'end')
            entry_cantidad.insert(0, str(int(values[3])))
        else:
            entry_codigo.delete(0, 'end')
            entry_cantidad.delete(0, 'end')
            entry_cantidad.insert(0, "1")

    tabla.bind('<<TreeviewSelect>>', on_select)

    frame_total = Frame(frame_izquierdo, bg="#E6F0FA")
    frame_total.pack(fill="x", pady=5)
    Label(frame_total, text="Total:", bg="#E6F0FA", font=("Arial", 12, "bold")).pack(side="left", padx=(10, 2))
    total_var = StringVar(value=venta_estado.total)
    Label(frame_total, textvariable=total_var, bg="#E6F0FA", font=("Arial", 12)).pack(side="left")
    Label(frame_total, text="Pago con:", bg="#E6F0FA", font=("Arial", 12, "bold")).pack(side="left", padx=(10, 2))
    pago_con = Entry(frame_total, font=("Arial", 12), width=15)
    pago_con.pack(side="left", padx=(10, 2))
    Label(frame_total, text="Cambio:", bg="#E6F0FA", font=("Arial", 12, "bold")).pack(side="left", padx=(10, 2))
    cambio = Entry(frame_total, font=("Arial", 12), width=15, state="readonly")
    cambio.pack(side="left", padx=(10, 2))
    cambio.insert(0, "0.00")
    btn_ticket = Button(frame_total, text="Generar Ticket", font=("Arial", 10), bg="#2196F3", fg="white", width=15,
                        command=generar_ticket, state="disabled")
    btn_ticket.pack(side="left", padx=(10, 2))

    def calcular_cambio(event=None):
        try:
            total = float(total_var.get())
            pago = pago_con.get().strip()
            if not pago:
                cambio.config(state="normal")
                cambio.delete(0, 'end')
                cambio.insert(0, "0.00")
                cambio.config(state="readonly")
                return 0.0
            pago = float(pago)
            cambio_calculado = pago - total
            cambio.config(state="normal")
            cambio.delete(0, 'end')
            cambio.insert(0, f"{cambio_calculado:.2f}")
            cambio.config(state="readonly")
            return cambio_calculado
        except ValueError:
            cambio.config(state="normal")
            cambio.delete(0, 'end')
            cambio.insert(0, "0.00")
            cambio.config(state="readonly")
            return 0.0

    pago_con.bind("<Return>", calcular_cambio)
    pago_con.bind("<FocusOut>", calcular_cambio)

    def buscar_y_mostrar():
        if hay_corte_de_caja():
            messagebox.showerror("Error", "No se pueden realizar ventas: ya se ha realizado un corte de caja.")
            return
        codigo = entry_codigo.get().strip()
        if not codigo:
            messagebox.showerror("Error", "Ingrese un código")
            return
        try:
            cantidad = int(entry_cantidad.get().strip()) if entry_cantidad.get().strip() else 1
            if cantidad <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
                return
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero")
            return
        metodo_seleccionado = metodo_pago_var.get()
        if not metodo_seleccionado:
            messagebox.showerror("Error", "Seleccione un método de pago")
            return
        id_metodo = metodo_seleccionado.split(" - ")[0]
        resultado = buscar_articulo("codigo", codigo)
        if resultado:
            resultado = resultado[0]
            if resultado[4] < cantidad:
                messagebox.showwarning("Sin stock", f"No hay suficiente existencia del artículo {resultado[1]} (disponible: {resultado[4]})")
                entry_codigo.delete(0, 'end')
                entry_cantidad.delete(0, 'end')
                entry_cantidad.insert(0, "1")
                entry_codigo.focus_set()
                return
            precio = resultado[2]
            subtotal = precio * cantidad
            articulo = (codigo, resultado[1], precio, cantidad, subtotal, metodo_seleccionado.split(" - ")[1])
            print(f"Debug: Añadiendo artículo: {articulo}, código: {codigo}, tipo: {type(codigo)}")
            tabla.insert("", "end", values=articulo)
            venta_estado.articulos.append((codigo, resultado[1], precio, cantidad, subtotal, id_metodo))
            total_var.set(f"{sum(float(item[4]) for item in venta_estado.articulos):.2f}")
            venta_estado.total = total_var.get()
            print(f"Debug: Total después de añadir: {total_var.get()}")
            venta_estado.usuario = entry_usuario.get().strip()
            entry_codigo.delete(0, 'end')
            entry_cantidad.delete(0, 'end')
            entry_cantidad.insert(0, "1")
            calcular_cambio()
        else:
            messagebox.showerror("No encontrado", f"No se encontró el artículo con código {codigo}.")
        entry_codigo.focus_set()

    def actualizar_articulo():
        if hay_corte_de_caja():
            messagebox.showerror("Error", "No se pueden actualizar productos: ya se ha realizado un corte de caja.")
            return
        producto = tabla.selection()
        if not producto:
            messagebox.showerror("Error", "Seleccione un artículo para actualizar")
            return
        try:
            nueva_cantidad = int(entry_cantidad.get().strip()) if entry_cantidad.get().strip() else 1
            if nueva_cantidad <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
                return
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero")
            return
        metodo_seleccionado = metodo_pago_var.get()
        if not metodo_seleccionado:
            messagebox.showerror("Error", "Seleccione un método de pago")
            return
        id_metodo = metodo_seleccionado.split(" - ")[0]
        codigo = tabla.item(producto)['values'][0]
        resultado = buscar_articulo("codigo", codigo)
        if resultado:
            resultado = resultado[0]
            if resultado[4] < nueva_cantidad:
                messagebox.showwarning("Sin stock", f"No hay suficiente existencia del producto {resultado[1]} (disponible: {resultado[4]})")
                return
            precio = resultado[2]
            subtotal = precio * nueva_cantidad
            articulo = (codigo, resultado[1], precio, nueva_cantidad, subtotal, metodo_seleccionado.split(" - ")[1])
            tabla.item(producto, values=articulo)
            index = next(i for i, item in enumerate(venta_estado.articulos) if item[0] == codigo)
            venta_estado.articulos[index] = (codigo, resultado[1], precio, nueva_cantidad, subtotal, id_metodo)
            total_var.set(f"{sum(float(item[4]) for item in venta_estado.articulos):.2f}")
            venta_estado.total = total_var.get()
            venta_estado.usuario = entry_usuario.get().strip()
            entry_codigo.delete(0, 'end')
            entry_cantidad.delete(0, 'end')
            entry_cantidad.insert(0, "1")
            entry_codigo.focus_set()
            calcular_cambio()
        else:
            messagebox.showerror("Error", "El artículo no existe en la base de datos")
            tabla.delete(producto)
            venta_estado.articulos = [item for item in venta_estado.articulos if item[0] != codigo]
            total_var.set(f"{sum(float(item[4]) for item in venta_estado.articulos):.2f}")
            venta_estado.total = total_var.get()
            calcular_cambio()

    def eliminar_articulo():
        if hay_corte_de_caja():
            messagebox.showerror("Error", "No se pueden eliminar productos: ya se ha realizado un corte de caja.")
            return
        producto_seleccionado = tabla.selection()
        if not producto_seleccionado:
            messagebox.showerror("Error", "Seleccione un producto para eliminar")
            return
        
        # Get the code of the selected product from the table
        codigo = tabla.item(producto_seleccionado)['values'][0]
        print(f"Debug: Código del producto seleccionado para eliminar: {codigo}, tipo: {type(codigo)}")
        
        # Log the current state of venta_estado.articulos
        print(f"Debug: Artículos antes de eliminar: {venta_estado.articulos}")
        
        # Remove the item from the table
        tabla.delete(producto_seleccionado)
        
        # Remove the item from venta_estado.articulos
        venta_estado.articulos = [item for item in venta_estado.articulos if str(item[0]) != str(codigo)]
        print(f"Debug: Artículos después de eliminar: {venta_estado.articulos}")
        
        # Recalculate the total
        if not venta_estado.articulos:  # If the list is empty, set total to 0
            total = 0.0
            print("Debug: Lista de artículos vacía, total establecido a 0.0")
        else:
            total = sum(float(item[4]) for item in venta_estado.articulos)
            print(f"Debug: Total recalculado: {total}")
        
        # Update total_var and venta_estado.total
        total_var.set(f"{total:.2f}")
        venta_estado.total = total_var.get()
        print(f"Debug: total_var actualizado a: {total_var.get()}")
        
        # Clear ultima_venta to prevent using old data in the ticket
        venta_estado.ultima_venta = None
        print("Debug: ultima_venta limpiada")
        
        # Update venta_estado.usuario
        venta_estado.usuario = entry_usuario.get().strip()
        
        # Clear and refresh the table to ensure it matches venta_estado.articulos
        for row in tabla.get_children():
            tabla.delete(row)
        for articulo in venta_estado.articulos:
            tabla.insert("", "end", values=articulo)
        print("Debug: Tabla actualizada para reflejar venta_estado.articulos")
        
        # Reset input fields
        entry_codigo.delete(0, 'end')
        entry_cantidad.delete(0, 'end')
        entry_cantidad.insert(0, "1")
        entry_codigo.focus_set()
        
        # Recalculate change
        calcular_cambio()
        
        # Disable ticket button until a new sale is confirmed
        btn_ticket.config(state="disabled")

    def confirmar_venta():
        global btn_ticket
        if hay_corte_de_caja():
            messagebox.showerror("Error", "No se pueden confirmar ventas: ya se ha realizado un corte de caja.")
            return
        if not tabla.get_children():
            messagebox.showerror("Error", "No hay productos en la venta")
            return
        usuario = entry_usuario.get().strip()
        if not usuario:
            messagebox.showerror("Error", "Ingrese un usuario")
            return
        try:
            total = float(total_var.get())
            metodo_seleccionado = metodo_pago_var.get()
            if not metodo_seleccionado:
                messagebox.showerror("Error", "Seleccione un método de pago")
                return
            metodo_nombre = metodo_seleccionado.split(" - ")[1].strip()
            if metodo_nombre == "Efectivo":
                pago = pago_con.get().strip()
                if not pago:
                    messagebox.showerror("Error", "Ingrese un monto de pago")
                    pago_con.focus_set()
                    return
                pago = float(pago)
                cambio_val = calcular_cambio()
                if pago < total:
                    messagebox.showerror("Error", "El pago no puede ser menor al total a pagar")
                    pago_con.delete(0, 'end')
                    cambio.config(state="normal")
                    cambio.delete(0, 'end')
                    cambio.insert(0, "0.00")
                    cambio.config(state="readonly")
                    pago_con.focus_set()
                    return
            else:  # Tarjeta de Crédito o Débito
                pago = total  # Pago es igual al total, ya que se asume que la tarjeta cubre todo
                cambio_val = 0.0  # No hay cambio con tarjeta
                cambio.config(state="normal")
                cambio.delete(0, "end")
                cambio.insert(0, "0.00")
                cambio.config(state="readonly")
            pago_con_centavos = int(pago * 100)
            cambio_con_centavos = int(cambio_val * 100)
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto válido para el pago")
            pago_con.delete(0, 'end')
            cambio.config(state="normal")
            cambio.delete(0, 'end')
            cambio.insert(0, "0.00")
            cambio.config(state="readonly")
            pago_con.focus_set()
            return

        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT EXISTS(SELECT 1 FROM usuarios WHERE usuario = %s)", (usuario,))
                if not cursor.fetchone()[0]:
                    messagebox.showerror("Error", "El usuario no existe")
                    return
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al verificar usuario: {e}")
                return
            finally:
                cursor.close()
                conexion.close()

        telefono = entry_telefono.get().strip()
        print(f"Debug: Telefono en confirmar_venta: {telefono}")
        if telefono:
            if len(telefono) > 15 or not telefono.isdigit():
                messagebox.showerror("Error", "El número de teléfono debe ser un número de hasta 15 dígitos")
                entry_telefono.focus_set()
                return
            cliente = buscar_cliente("telefono", telefono)
            print(f"Debug: Cliente en confirmar_venta: {cliente}")
            if not cliente:
                respuesta = messagebox.askyesno(
                    "Cliente no encontrado",
                    f"No se encontró un cliente con teléfono {telefono}. ¿Desea agregarlo?")
                if respuesta:
                    cliente_agregado = abrir_ventana_agregar(telefono)
                    if not cliente_agregado:
                        messagebox.showinfo("Cancelado", "La venta fue cancelada porque no se agregó el cliente")
                        return
                else:
                    messagebox.showerror("Error", "El cliente debe existir para registrar la venta con teléfono")
                    return
        else:
            telefono = None

        articulos_con_metodo = venta_estado.articulos
        if agregar_venta(usuario, articulos_con_metodo, telefono):
            venta_estado.ultima_venta = {
                "articulos": venta_estado.articulos.copy(),
                "total": total_var.get(),
                "telefono": telefono,
                "pago_con": float(pago),
                "cambio": float(cambio_val)
            }
            print(f"Debug: ultima_venta guardada: {venta_estado.ultima_venta}")
            messagebox.showinfo("Confirmada", f"Venta confirmada correctamente a las {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CST")
            for row in tabla.get_children():
                tabla.delete(row)
            venta_estado.articulos = []
            venta_estado.total = "0.00"
            total_var.set("0.00")
            entry_codigo.delete(0, 'end')
            entry_cantidad.delete(0, 'end')
            entry_cantidad.insert(0, "1")
            combo_metodo_pago.set(combo_metodo_pago['values'][0] if combo_metodo_pago['values'] else '')
            pago_con.delete(0, 'end')
            cambio.config(state='normal')
            cambio.delete(0, 'end')
            cambio.insert(0, "0.00")
            cambio.config(state='readonly')
            entry_telefono.delete(0, 'end')
            cliente_info_label.config(text="")
            entry_codigo.focus_set()
            btn_ticket.config(state="normal")

    def abrir_ventana_agregar(telefono):
        cliente_ventana = Toplevel()
        cliente_ventana.title("Agregar cliente")
        cliente_ventana.geometry("400x300")
        cliente_ventana.resizable(False, False)

        frame = Frame(cliente_ventana, bg="#E6F0FA")
        frame.pack(expand=True, fill="both", padx=10, pady=10)

        Label(frame, text="Agregar Cliente", font=("Arial", 12, "bold"), bg="#E6F0FA").pack(pady=10)

        campos = ["Nombre:", "Apellidos:", "Teléfono:", "Dirección:", "RFC:", "Correo:"]
        entradas = {}
        for i, campo in enumerate(campos):
            Label(frame, text=campo, bg="#E6F0FA", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
            entrada = Entry(frame, font=("Arial", 12))
            entrada.pack(fill="x", padx=10, pady=5)
            entradas[campo] = entrada
            if campo == "Teléfono:":
                entrada.insert(0, telefono)
                entrada.config(state="readonly")

        def guardar_cliente():
            nombre = entradas["Nombre:"].get().strip()
            apellidos = entradas["Apellidos:"].get().strip()
            telefono = entradas["Teléfono:"].get().strip()
            direccion = entradas["Dirección:"].get().strip()
            rfc = entradas["RFC:"].get().strip()
            correo = entradas["Correo:"].get().strip()

            if not all([nombre, apellidos, telefono, direccion, correo]):
                messagebox.showerror("Error", "Todos los campos excepto RFC son obligatorios")
                return
            try:
                agregar_cliente(nombre, apellidos, telefono, direccion, rfc, correo)
                cliente_ventana.destroy()
            except mysql.connector.Error as error:
                messagebox.showerror("Error", f"Error al agregar cliente: {error}")

        Button(frame, text="Guardar", font=("Arial", 10), bg="#4CAF50", fg="white", command=guardar_cliente).pack(pady=10)
        Button(frame, text="Cancelar", font=("Arial", 10), bg="#F44336", fg="white", command=cliente_ventana.destroy).pack(pady=5)

        cliente_ventana.grab_set()
        cliente_ventana.wait_window()
        return entradas["Nombre:"].get().strip() != ""

    def borrar_venta():
        if hay_corte_de_caja():
            messagebox.showerror("Error", "No se pueden borrar ventas: ya se ha realizado un corte de caja.")
            return
        for row in tabla.get_children():
            tabla.delete(row)
        venta_estado.articulos = []
        venta_estado.total = "0.00"
        total_var.set("0.00")
        venta_estado.ultima_venta = None  # Clear ultima_venta
        entry_codigo.delete(0, 'end')
        entry_cantidad.delete(0, 'end')
        entry_cantidad.insert(0, "1")
        combo_metodo_pago.set(combo_metodo_pago['values'][0] if combo_metodo_pago['values'] else '')
        pago_con.delete(0, 'end')
        cambio.config(state='normal')
        cambio.delete(0, 'end')
        cambio.insert(0, "0.00")
        cambio.config(state='readonly')
        entry_telefono.delete(0, 'end')
        cliente_info_label.config(text="")
        entry_codigo.focus_set()
        btn_ticket.config(state='disabled')

    def limpiar_entradas():
        entry_codigo.delete(0, 'end')
        entry_cantidad.delete(0, 'end')
        entry_cantidad.insert(0, '1')
        pago_con.delete(0, 'end')
        cambio.config(state='normal')
        cambio.delete(0, 'end')
        cambio.insert(0, "0.00")
        cambio.config(state='readonly')
        entry_telefono.delete(0, 'end')
        cliente_info_label.config(text="")
        venta_estado.ultima_venta = None  # Clear ultima_venta
        entry_codigo.focus_set()
        btn_ticket.config(state='disabled')

    btn_confirmar = Button(frame_derecho, text="Confirmar", font=("Arial", 10), bg="#4CAF50", fg="white", width=12,
                           command=confirmar_venta)
    btn_confirmar.pack(pady=10)
    btn_borrar = Button(frame_derecho, text="Borrar", font=("Arial", 10), bg="#FFC107", fg="black", width=12,
                        command=borrar_venta)
    btn_borrar.pack(pady=10)
    btn_limpiar = Button(frame_derecho, text="Limpiar", font=("Arial", 10), bg="#FFD108", fg="black", width=12,
                         command=limpiar_entradas)
    btn_limpiar.pack(pady=10)
    btn_eliminar = Button(frame_derecho, text="Eliminar", font=("Arial", 10), bg="#F44336", fg="white", width=12,
                          command=eliminar_articulo)
    btn_eliminar.pack(pady=5)
    btn_actualizar = Button(frame_derecho, text="Actualizar", font=("Arial", 10), bg="#2196F3", fg="white", width=12,
                            command=actualizar_articulo)
    btn_actualizar.pack(pady=5)

    if hay_corte_de_caja():
        entry_codigo.config(state="disabled")
        entry_cantidad.config(state="disabled")
        combo_metodo_pago.config(state="disabled")
        pago_con.config(state="disabled")
        entry_telefono.config(state="disabled")
        btn_agregar.config(state="disabled")
        btn_confirmar.config(state="disabled")
        btn_borrar.config(state="disabled")
        btn_eliminar.config(state="disabled")
        btn_actualizar.config(state="disabled")
        btn_ticket.config(state="disabled")
        messagebox.showerror("Advertencia", "No se pueden realizar operaciones de venta: ya se ha registrado un corte de caja.")

    return frame_principal

if __name__ == "__main__":
    ventana = Tk()
    ventana.title("Ventas")
    ventana.geometry("800x600")
    crear_seccion_ventas(ventana, None, None).pack(expand=True, fill="both")
    ventana.mainloop()