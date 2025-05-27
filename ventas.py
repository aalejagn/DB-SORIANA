from tkinter import Tk, Label, Frame, Entry, Button, ttk, messagebox, StringVar
from db_soriana import buscar_articulo, agregar_venta, buscar_metodo_de_pago, ver_metodo_de_pago
from datetime import datetime
import mysql.connector

class VentaEstado:
    def __init__(self):
        self.articulos = []  # Lista de [código, nombre, precio, cantidad, subtotal, id_metodo]
        self.total = "0.00"
        self.usuario = "cajero1"  # Valor por defecto

venta_estado = VentaEstado()

def interfaz_ventas():
    ventana = Tk()
    ventana.title("Ventas")
    ventana.geometry("1000x600")
    crear_seccion_ventas(ventana, None, None).pack(expand=True, fill="both")
    ventana.mainloop()

def crear_seccion_ventas(ventana, barra_lateral, usuario):
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

    # Search frame
    frame_search = Frame(frame_izquierdo, bg="#E6F0FA")
    frame_search.pack(fill="x", pady=5)
    Label(frame_search, text="Código:", bg="#E6F0FA", font=("Arial", 12)).pack(side="left", padx=(10, 2))
    entry_codigo = Entry(frame_search, font=("Arial", 12), width=20)
    entry_codigo.pack(side="left", padx=(0, 10))
    Label(frame_search, text="Cantidad:", bg="#E6F0FA", font=("Arial", 12)).pack(side="left", padx=(10, 2))
    entry_cantidad = Entry(frame_search, font=("Arial", 12), width=5)
    entry_cantidad.pack(side="left", padx=(0, 10))
    entry_cantidad.insert(0, "1")
    Button(frame_search, text="Agregar", font=("Arial", 10), bg="#2196F3", fg="white",
           command=lambda: buscar_y_mostrar()).pack(side="left", padx=5)

    # Payment and cashier frame
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
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al cargar los métodos de pago: {e}")
        finally:
            cursor.close()
            conexion.close()

    cargar_metodos_pago()
    entry_codigo.focus_set()

    # Table frame
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
            tabla.insert("", "end", values=articulo)
            venta_estado.articulos.append((codigo, resultado[1], precio, cantidad, subtotal, id_metodo))
            total_var.set(f"{sum(float(item[4]) for item in venta_estado.articulos):.2f}")
            venta_estado.total = total_var.get()
            venta_estado.usuario = entry_usuario.get().strip()
            entry_codigo.delete(0, 'end')
            entry_cantidad.delete(0, 'end')
            entry_cantidad.insert(0, "1")
        else:
            messagebox.showerror("No encontrado", f"No se encontró el artículo con código {codigo}.")
        entry_codigo.focus_set()

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
        metodo_seleccionado = metodo_pago_var.get()
        if not metodo_seleccionado:
            messagebox.showerror("Error", "Seleccione un método de pago")
            return
        id_metodo = metodo_seleccionado.split(" - ")[0]
        codigo = tabla.item(selected_item)['values'][0]
        resultado = buscar_articulo("codigo", codigo)
        if resultado:
            resultado = resultado[0]
            if resultado[4] < nueva_cantidad:
                messagebox.showwarning("Sin stock", f"No hay suficiente existencia del artículo {resultado[1]} (disponible: {resultado[4]})")
                return
            precio = resultado[2]
            subtotal = precio * nueva_cantidad
            articulo = (codigo, resultado[1], precio, nueva_cantidad, subtotal, metodo_seleccionado.split(" - ")[1])
            tabla.item(selected_item, values=articulo)
            index = next(i for i, item in enumerate(venta_estado.articulos) if item[0] == codigo)
            venta_estado.articulos[index] = (codigo, resultado[1], precio, nueva_cantidad, subtotal, id_metodo)
            total_var.set(f"{sum(float(item[4]) for item in venta_estado.articulos):.2f}")
            venta_estado.total = total_var.get()
            venta_estado.usuario = entry_usuario.get().strip()
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
        venta_estado.usuario = entry_usuario.get().strip()
        entry_codigo.delete(0, 'end')
        entry_cantidad.delete(0, 'end')
        entry_cantidad.insert(0, "1")
        entry_codigo.focus_set()

    def confirmar_venta():
        if not tabla.get_children():
            messagebox.showerror("Error", "No hay artículos en la venta")
            return
        usuario = entry_usuario.get().strip()
        if not usuario:
            messagebox.showerror("Error", "Ingrese un usuario")
            return
        conexion = obtener_conexion()
        if not conexion:
            return
        cursor = conexion.cursor()
        cursor.execute("SELECT usuario FROM usuarios WHERE usuario = %s", (usuario,))
        if not cursor.fetchone():
            messagebox.showerror("Error", "El usuario no existe")
            cursor.close()
            conexion.close()
            return
        cursor.close()
        conexion.close()
        
        # Prepare articulos with id_metodo
        articulos_con_metodo = []
        for item in tabla.get_children():
            values = tabla.item(item)['values']
            codigo, nombre, precio, cantidad, subtotal, metodo_nombre = values
            metodo_seleccionado = metodo_pago_var.get()
            id_metodo = metodo_seleccionado.split(" - ")[0]  # Extract id_metodo from combo
            articulos_con_metodo.append((codigo, nombre, float(precio), int(cantidad), float(subtotal), int(id_metodo)))
        
        agregar_venta(usuario, articulos_con_metodo)
        messagebox.showinfo("Éxito", "Venta registrada correctamente")
        for row in tabla.get_children():
            tabla.delete(row)
        venta_estado.articulos = []
        venta_estado.total = "0.00"
        venta_estado.usuario = usuario
        total_var.set("0.00")
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
        total_var.set("0.00")
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

def obtener_conexion():
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