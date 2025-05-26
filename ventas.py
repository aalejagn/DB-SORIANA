from tkinter import Tk, Label, Frame, Entry, Button, ttk, messagebox, StringVar
from db_soriana import buscar_articulo, agregar_venta, actualizar_stock, buscar_cliente, buscar_metodo_de_pago, ver_metodo_de_pago
from datetime import datetime
import uuid
import mysql.connector

# Clase para almacenar el estado de la venta
class VentaEstado:
    def __init__(self):
        self.articulos = []  # Lista de [código, nombre, precio, cantidad, subtotal]
        self.total = "0.00"
        self.telefono = ""

# Estado global de la venta
venta_estado = VentaEstado()

def interfaz_ventas():
    ventana = Tk()
    ventana.title("Ventas")
    ventana.geometry("1000x600")
    crear_seccion_ventas(ventana, None, None).pack(expand=True, fill="both")
    ventana.mainloop()

def crear_seccion_ventas(ventana, barra_lateral, usuario):
    campos = ["Código", "Nombre", "Precio", "Cantidad", "Subtotal"]

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

    # Search and client frame
    frame_search = Frame(frame_izquierdo, bg="#E6F0FA")
    frame_search.pack(fill="x", pady=5)
    Label(frame_search, text="Código:", bg="#E6F0FA", font=("Arial", 12)).pack(side="left", padx=(10, 2))
    entry_codigo = Entry(frame_search, font=("Arial", 12), width=20)
    entry_codigo.pack(side="left", padx=(0, 10))
    Label(frame_search, text="Cantidad:", bg="#E6F0FA", font=("Arial", 12)).pack(side="left", padx=(10, 2))
    entry_cantidad = Entry(frame_search, font=("Arial", 12), width=5)
    entry_cantidad.pack(side="left", padx=(0, 10))
    entry_cantidad.insert(0, "1")  # Valor por defecto
    Button(frame_search, text="Agregar", font=("Arial", 10), bg="#2196F3", fg="white",
           command=lambda: buscar_y_mostrar()).pack(side="left", padx=5)
    Label(frame_search, text="Teléfono Cliente:", bg="#E6F0FA", font=("Arial", 12)).pack(side="left", padx=(10, 2))
    entry_telefono = Entry(frame_search, font=("Arial", 12), width=15)
    entry_telefono.pack(side="left", padx=(0, 10))
    entry_telefono.insert(0, venta_estado.telefono)

    # Payment method frame
    frame_pago = Frame(frame_izquierdo, bg="#E6F0FA")
    frame_pago.pack(fill="x", pady=5)
    Label(frame_pago, text="Método de Pago:", bg="#E6F0FA", font=("Arial", 12)).pack(side="left", padx=(10, 2))
    metodo_pago_var = StringVar()
    combo_metodo_pago = ttk.Combobox(frame_pago, textvariable=metodo_pago_var, font=("Arial", 12), state="readonly", width=15)
    combo_metodo_pago.pack(side="left", padx=(0, 10))

    # Load payment methods from the database
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
                messagebox.showwarning("Advertencia", "No hay métodos de pago registrados. Por favor, añada un método de pago.")
                combo_metodo_pago['values'] = []
                metodo_pago_var.set("")
                return
            # Formato: "id_metodo - tipo"
            opciones = [f"{metodo[0]} - {metodo[1]}" for metodo in metodos]
            combo_metodo_pago['values'] = opciones
            # Seleccionar el primer método por defecto, si existe
            metodo_pago_var.set(opciones[0] if opciones else "")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al cargar los métodos de pago: {e}")
        finally:
            cursor.close()
            conexion.close()

    cargar_metodos_pago()  # Call the function to load payment methods
    
    entry_codigo.focus_set()

    # Table frame (reduced height)
    frame_tabla = Frame(frame_izquierdo, bg="#E6F0FA")
    frame_tabla.pack(padx=10, fill="both", expand=True)
    tabla = ttk.Treeview(frame_tabla, columns=campos, show="headings", height=12)
    for col in campos:
        tabla.heading(col, text=col)
        tabla.column(col, width=100)
    tabla.pack(pady=10, fill="both", expand=True)

    # Cargar artículos almacenados
    for articulo in venta_estado.articulos:
        tabla.insert("", "end", values=articulo)

    def on_select(event):
        selected_item = tabla.selection()
        if selected_item:
            values = tabla.item(selected_item)['values']
            entry_codigo.delete(0, 'end')
            entry_codigo.insert(0, values[0])  # Código
            entry_cantidad.delete(0, 'end')
            entry_cantidad.insert(0, str(int(values[3])))  # Cantidad
        else:
            entry_codigo.delete(0, 'end')
            entry_cantidad.delete(0, 'end')
            entry_cantidad.insert(0, "1")

    tabla.bind('<<TreeviewSelect>>', on_select)

    # Total frame
    frame_total = Frame(frame_izquierdo, bg="#E6F0FA")
    frame_total.pack(fill="x", pady=5)
    Label(frame_total, text="Total:", bg="#E6F0FA", font=("Arial", 12, "bold")).pack(side="left", padx=(10, 2))
    total_var = StringVar(value=venta_estado.total)
    Label(frame_total, textvariable=total_var, bg="#E6F0FA", font=("Arial", 12)).pack(side="left")

    def buscar_y_mostrar():
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

        resultado = buscar_articulo(codigo)
        if resultado:
            if resultado[4] < cantidad:
                messagebox.showwarning("Sin stock", f"No hay suficiente existencia del artículo {resultado[1]} (disponible: {resultado[4]})")
                entry_codigo.delete(0, 'end')
                entry_cantidad.delete(0, 'end')
                entry_cantidad.insert(0, "1")
                entry_codigo.focus_set()
                return
            precio = resultado[2]
            subtotal = precio * cantidad
            articulo = (codigo, resultado[1], precio, cantidad, subtotal)
            tabla.insert("", "end", values=articulo)
            venta_estado.articulos.append(articulo)
            total_var.set(f"{sum(float(item[4]) for item in venta_estado.articulos):.2f}")
            venta_estado.total = total_var.get()
            venta_estado.telefono = entry_telefono.get().strip()
            entry_codigo.delete(0, 'end')
            entry_cantidad.delete(0, 'end')
            entry_cantidad.insert(0, "1")
        else:
            response = messagebox.askyesno("No encontrado", f"No se encontró el artículo con código {codigo}. ¿Desea agregarlo?")
            if response:
                from articulos import crear_seccion_articulos
                for widget in ventana.winfo_children():
                    if widget != barra_lateral:
                        widget.destroy()
                venta_estado.telefono = entry_telefono.get().strip()
                crear_seccion_articulos(ventana, barra_lateral, codigo)
        entry_codigo.focus_set()

    entry_codigo.bind('<Return>', lambda event: entry_cantidad.focus_set())

    def actualizar_producto():
        selected_item = tabla.selection()
        if not selected_item:
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

        codigo = tabla.item(selected_item)['values'][0]
        resultado = buscar_articulo(codigo)
        if resultado:
            if resultado[4] < nueva_cantidad:
                messagebox.showwarning("Sin stock", f"No hay suficiente existencia del artículo {resultado[1]} (disponible: {resultado[4]})")
                return
            precio = resultado[2]
            subtotal = precio * nueva_cantidad
            articulo = (codigo, resultado[1], precio, nueva_cantidad, subtotal)
            tabla.item(selected_item, values=articulo)
            index = next(i for i, item in enumerate(venta_estado.articulos) if item[0] == codigo)
            venta_estado.articulos[index] = articulo
            total_var.set(f"{sum(float(item[4]) for item in venta_estado.articulos):.2f}")
            venta_estado.total = total_var.get()
            venta_estado.telefono = entry_telefono.get().strip()
            entry_codigo.delete(0, 'end')
            entry_cantidad.delete(0, 'end')
            entry_cantidad.insert(0, "1")
            entry_codigo.focus_set()
        else:
            messagebox.showerror("Error", "El artículo no existe en la base de datos")
            tabla.delete(selected_item)
            venta_estado.articulos = [item for item in venta_estado.articulos if item[0] != codigo]
            total_var.set(f"{sum(float(item[4]) for item in venta_estado.articulos):.2f}")
            venta_estado.total = total_var.get()

    def eliminar_producto():
        selected_item = tabla.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione un artículo para eliminar")
            return
        codigo = tabla.item(selected_item)['values'][0]
        tabla.delete(selected_item)
        venta_estado.articulos = [item for item in venta_estado.articulos if item[0] != codigo]
        total_var.set(f"{sum(float(item[4]) for item in venta_estado.articulos):.2f}")
        venta_estado.total = total_var.get()
        venta_estado.telefono = entry_telefono.get().strip()
        entry_codigo.delete(0, 'end')
        entry_cantidad.delete(0, 'end')
        entry_cantidad.insert(0, "1")
        entry_codigo.focus_set()

    def confirmar_venta():
        if not tabla.get_children():
            messagebox.showerror("Error", "No hay artículos en la venta")
            return

        telefono = entry_telefono.get().strip() or None
        if telefono and not buscar_cliente(telefono):
            messagebox.showerror("Error", "El cliente con ese teléfono no existe")
            return

        # Extract id_metodo from Combobox selection
        metodo_seleccionado = metodo_pago_var.get()
        if not metodo_seleccionado:
            messagebox.showerror("Error", "Seleccione un método de pago")
            return
        id_metodo = metodo_seleccionado.split(" - ")[0]
        if not buscar_metodo_de_pago(id_metodo):
            messagebox.showerror("Error", f"El método de pago con ID {id_metodo} no existe en la base de datos")
            return

        id_venta = str(uuid.uuid4())[:10]
        total = float(total_var.get())
        fecha = datetime.now().strftime('%Y-%m-%d')
        id_empleado = 1

        agregar_venta(id_venta, telefono, id_metodo, total, fecha, id_empleado)
        for item in tabla.get_children():
            codigo = tabla.item(item)['values'][0]
            cantidad = int(tabla.item(item)['values'][3])
            actualizar_stock(codigo, cantidad)
        messagebox.showinfo("Éxito", "Venta registrada correctamente")
        for row in tabla.get_children():
            tabla.delete(row)
        venta_estado.articulos = []
        venta_estado.total = "0.00"
        venta_estado.telefono = ""
        total_var.set("0.00")
        entry_telefono.delete(0, 'end')
        entry_codigo.delete(0, 'end')
        entry_cantidad.delete(0, 'end')
        entry_cantidad.insert(0, "1")
        combo_metodo_pago.set(combo_metodo_pago['values'][0] if combo_metodo_pago['values'] else "")
        entry_codigo.focus_set()

    def borrar_venta():
        for row in tabla.get_children():
            tabla.delete(row)
        venta_estado.articulos = []
        venta_estado.total = "0.00"
        venta_estado.telefono = ""
        total_var.set("0.00")
        entry_telefono.delete(0, 'end')
        entry_codigo.delete(0, 'end')
        entry_cantidad.delete(0, 'end')
        entry_cantidad.insert(0, "1")
        combo_metodo_pago.set(combo_metodo_pago['values'][0] if combo_metodo_pago['values'] else "")
        entry_codigo.focus_set()

    def limpiar_entradas():
        entry_codigo.delete(0, 'end')
        entry_cantidad.delete(0, 'end')
        entry_cantidad.insert(0, "1")
        entry_codigo.focus_set()

    Button(frame_derecho, text="Confirmar Venta", font=("Arial", 10), bg="#4CAF50", fg="white", width=15,
           command=confirmar_venta).pack(pady=5)
    Button(frame_derecho, text="Borrar Venta", font=("Arial", 10), bg="#FFC107", fg="black", width=15,
           command=borrar_venta).pack(pady=5)
    Button(frame_derecho, text="Limpiar", font=("Arial", 10), bg="#FF9800", fg="black", width=15,
           command=limpiar_entradas).pack(pady=5)
    Button(frame_derecho, text="Eliminar Producto", font=("Arial", 10), fg="white", bg="#F44336", width=15,
           command=eliminar_producto).pack(pady=5)
    Button(frame_derecho, text="Actualizar", font=("Arial", 10), bg="#2196F3", fg="white", width=15,
           command=actualizar_producto).pack(pady=5)

    return frame_principal

# Función auxiliar para conectar a la base de datos (necesaria para cargar_metodos_pago)
def obtener_conexion():
    import mysql.connector
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="23270631@",
            database="db23270631"
        )
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
        return None

if __name__ == "__main__":
    interfaz_ventas()