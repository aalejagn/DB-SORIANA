from tkinter import Tk, Label, Frame, Entry, Button, ttk, messagebox, StringVar
from db_soriana import ver_historia_venta
from datetime import datetime

def interfaz_historia_venta():
    ventana = Tk()
    ventana.title("Historial de Ventas")
    ventana.geometry("1200x700")
    crear_seccion_historia_venta(ventana, None).pack(expand=True, fill="both")
    ventana.mainloop()

def crear_seccion_historia_venta(ventana, barra_lateral):
    campos = ["ID Venta", "Fecha", "Usuario", "Artículo", "Cantidad", "Subtotal", "Método de Pago"]

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

    # Frame for title and total
    frame_titulo_total = Frame(frame_superior, bg="#E6F0FA")
    frame_titulo_total.pack(fill="x")

    # Title on the left
    Label(frame_titulo_total, text="Historial de Ventas", font=("Arial", 16, "bold"), bg="#E6F0FA").pack(side="left", pady=5)

    # Total on the right
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

    frame_tabla = Frame(frame_centrado, bg="#E6F0FA")
    frame_tabla.pack(padx=10, fill="both", expand=True)
    tabla = ttk.Treeview(frame_tabla, columns=campos, show="headings", height=20)
    for col in campos:
        tabla.heading(col, text=col)
        tabla.column(col, width=150)
    tabla.pack(pady=10, fill="both", expand=True)

    def actualizar_tabla(fecha, total_var):
        try:
            datetime.strptime(fecha, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD")
            return
        success = ver_historia_venta(fecha, tabla)
        if success:
            # Calculate total from the table
            total = 0.0
            for row in tabla.get_children():
                subtotal = float(tabla.item(row)['values'][5])  # Subtotal is at index 5
                total += subtotal
            total_var.set(f"Total: {total:.2f}")
        else:
            total_var.set("Total: 0.00")

    actualizar_tabla(entry_fecha.get().strip(), total_var)

    return frame_principal

if __name__ == "__main__":
    interfaz_historia_venta()