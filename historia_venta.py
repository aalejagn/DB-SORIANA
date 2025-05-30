from tkinter import Tk, Label, Frame, Entry, Button, ttk, messagebox, StringVar, Scrollbar
from db_soriana import ver_historia_venta
from datetime import datetime

def interfaz_historia_venta():
    """
    Crea y ejecuta la interfaz principal para el historial de ventas.
    Inicializa la ventana principal y llama a la función para crear la sección de historial.
    """
    ventana = Tk()
    ventana.title("Historial de Ventas")
    ventana.geometry("1200x700")
    crear_seccion_historia_venta(ventana, None).pack(expand=True, fill="both")
    ventana.mainloop()

def crear_seccion_historia_venta(ventana, barra_lateral):
    """
    Crea la sección de historial de ventas dentro de la ventana principal.
    Args:
        ventana: Ventana principal de Tkinter.
        barra_lateral: Barra lateral opcional para navegación.
    """
    # Define las columnas que aparecerán en la tabla de historial
    campos = ["ID Venta", "Fecha", "Usuario", "Rol", "Teléfono", "Artículo", "Cantidad", "Subtotal", "Método de Pago", "Total Venta"]

    if barra_lateral:
        for widget in ventana.winfo_children():
            if widget != barra_lateral:
                widget.destroy()

    frame_principal = Frame(ventana, bg="#E6F0FA")
    frame_principal.pack(expand=True, fill="both")

    frame_centrado = Frame(frame_principal, bg="#E6F0FA")
    frame_centrado.pack(expand=True, fill="both", padx=10, pady=10)

    frame_superior = Frame(frame_centrado, bg="#E6F0FA")
    frame_superior.pack(fill="x", pady=10)

    frame_titulo_total = Frame(frame_superior, bg="#E6F0FA")
    frame_titulo_total.pack(fill="x")

    Label(frame_titulo_total, text="Historial de Ventas", font=("Arial", 16, "bold"), bg="#E6F0FA").pack(side="left", pady=5)

    total_var = StringVar(value="Total: 0.00")
    Label(frame_titulo_total, textvariable=total_var, font=("Arial", 14, "bold"), bg="#E6F0FA").pack(side="right", padx=10)

    frame_buscador = Frame(frame_superior, bg="#E6F0FA")
    frame_buscador.pack(fill="x", pady=5)
    Label(frame_buscador, text="Buscar por Fecha (YYYY-MM-DD):", bg="#E6F0FA", font=("Arial", 12)).pack(side="left", padx=(10, 2))
    entry_fecha = Entry(frame_buscador, font=("Arial", 12), width=15)
    entry_fecha.pack(side="left", padx=(0, 10))
    entry_fecha.insert(0, datetime.now().strftime('%Y-%m-%d'))
    Button(frame_buscador, text="Buscar", font=("Arial", 10), bg="#2196F3", fg="white",
           command=lambda: actualizar_tabla(entry_fecha.get().strip(), total_var)).pack(side="left", padx=5)
    Button(frame_buscador, text="Refrescar", font=("Arial", 10), bg="#4CAF50", fg="white",
           command=lambda: actualizar_tabla(entry_fecha.get().strip(), total_var)).pack(side="left", padx=5)

    frame_tabla = Frame(frame_centrado, bg="#E6F0FA")
    frame_tabla.pack(padx=10, fill="both", expand=True)

    # Agrega una barra de desplazamiento horizontal
    scrollbar_x = Scrollbar(frame_tabla, orient="horizontal")
    scrollbar_x.pack(side="bottom", fill="x")

    # Agrega una barra de desplazamiento vertical
    scrollbar_y = Scrollbar(frame_tabla, orient="vertical")
    scrollbar_y.pack(side="right", fill="y")

    # Crea la tabla con las columnas definidas y configura ambas barras
    tabla = ttk.Treeview(frame_tabla, columns=campos, show="headings", height=20,
                         yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    scrollbar_y.config(command=tabla.yview)
    scrollbar_x.config(command=tabla.xview)

    # Configura los encabezados y anchos de las columnas
    for col in campos:
        tabla.heading(col, text=col)
        tabla.column(col, width=120, minwidth=100, stretch=True)
    tabla.pack(pady=10, fill="both", expand=True)

    status_var = StringVar(value="Última actualización: N/A")
    Label(frame_centrado, textvariable=status_var, font=("Arial", 10), bg="#E6F0FA").pack(side="bottom", pady=5)

    def actualizar_tabla(fecha, total_var):
        """
        Actualiza la tabla con el historial de ventas para una fecha específica.
        Calcula y muestra el total de los totales de venta únicos.
        Args:
            fecha: Fecha en formato YYYY-MM-DD para filtrar las ventas.
            total_var: Variable StringVar para mostrar el total.
        """
        try:
            datetime.strptime(fecha, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD")
            return
        success = ver_historia_venta(fecha, tabla)
        if success:
            # Calcula el total sumando los total_venta de ventas únicas
            total = 0.0
            ventas_procesadas = set()  # Para evitar sumar la misma venta varias veces
            for row in tabla.get_children():
                id_venta = tabla.item(row)['values'][0]  # ID Venta en índice 0
                if id_venta not in ventas_procesadas:
                    total_venta = float(tabla.item(row)['values'][9])  # Total Venta en índice 9
                    total += total_venta
                    ventas_procesadas.add(id_venta)
            total_var.set(f"Total: {total:.2f}")
            status_var.set(f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            total_var.set("Total: 0.00")
            status_var.set("Última actualización: Error al cargar")

    actualizar_tabla(entry_fecha.get().strip(), total_var)

    return frame_principal

if __name__ == "__main__":
    interfaz_historia_venta()