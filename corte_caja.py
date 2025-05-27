from tkinter import Tk, Label, Frame, Entry, Button, ttk, messagebox, StringVar
from datetime import datetime
from db_soriana import ver_corte_de_caja, registrar_corte_de_caja, ver_cortes_historicos

def interfaz_corte_de_caja():
    ventana = Tk()
    ventana.title("Corte de Caja")
    ventana.geometry("1200x700")
    crear_seccion_corte_de_caja(ventana, None).pack(expand=True, fill="both")
    ventana.mainloop()

def crear_seccion_corte_de_caja(ventana, barra_lateral):
    campos_historicos = ["ID Corte", "Fecha", "Total", "Núm. Ventas", "Efectivo", "Tarjeta de crédito", "Transferencia", "Usuario"]

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

    Label(frame_superior, text="Corte de Caja - Día Actual", font=("Arial", 16, "bold"), bg="#E6F0FA").pack(pady=5)

    frame_resumen = Frame(frame_superior, bg="#E6F0FA")
    frame_resumen.pack(fill="x", pady=5)
    Label(frame_resumen, text=f"Fecha: {datetime.now().strftime('%Y-%m-%d')}", bg="#E6F0FA", font=("Arial", 12)).pack(side="left", padx=(10, 20))
    total_var = StringVar(value="0.00")
    Label(frame_resumen, text="Total del Día:", bg="#E6F0FA", font=("Arial", 12, "bold")).pack(side="left", padx=(10, 2))
    Label(frame_resumen, textvariable=total_var, bg="#E6F0FA", font=("Arial", 12)).pack(side="left", padx=(0, 20))
    num_ventas_var = StringVar(value="0")
    Label(frame_resumen, text="Número de Ventas:", bg="#E6F0FA", font=("Arial", 12, "bold")).pack(side="left", padx=(10, 2))
    Label(frame_resumen, textvariable=num_ventas_var, bg="#E6F0FA", font=("Arial", 12)).pack(side="left")

    frame_metodos = Frame(frame_superior, bg="#E6F0FA")
    frame_metodos.pack(fill="x", pady=5)
    metodos_vars = {"Efectivo": StringVar(value="0.00"), "Tarjeta de crédito": StringVar(value="0.00"), "Transferencia": StringVar(value="0.00")}
    for tipo, var in metodos_vars.items():
        Label(frame_metodos, text=f"Total {tipo}:", bg="#E6F0FA", font=("Arial", 12)).pack(side="left", padx=(10, 2))
        Label(frame_metodos, textvariable=var, bg="#E6F0FA", font=("Arial", 12)).pack(side="left", padx=(0, 20))

    frame_cajeros = Frame(frame_superior, bg="#E6F0FA")
    frame_cajeros.pack(fill="x", pady=5)
    cajeros_vars = {}
    def actualizar_cajeros(cajeros):
        for widget in frame_cajeros.winfo_children():
            widget.destroy()
        cajeros_vars.clear()
        for usuario, total in cajeros.items():
            cajeros_vars[usuario] = StringVar(value=f"{total:.2f}")
            Label(frame_cajeros, text=f"Total {usuario}:", bg="#E6F0FA", font=("Arial", 12)).pack(side="left", padx=(10, 2))
            Label(frame_cajeros, textvariable=cajeros_vars[usuario], bg="#E6F0FA", font=("Arial", 12)).pack(side="left", padx=(0, 20))

    def hacer_corte():
        fecha = datetime.now().strftime('%Y-%m-%d')
        corte_data = ver_corte_de_caja(fecha)
        if not corte_data["ventas"]:
            messagebox.showwarning("Sin ventas", f"No hay ventas registradas para el {fecha}")
            return
        total = corte_data["total"]
        num_ventas = corte_data["num_ventas"]
        metodos = corte_data["metodos"]
        usuario = max(corte_data["cajeros"], key=corte_data["cajeros"].get) if corte_data["cajeros"] else "cajero1"
        success = registrar_corte_de_caja(
            fecha,
            total,
            num_ventas,
            metodos.get("Efectivo", 0.00),
            metodos.get("Tarjeta de crédito", 0.00),
            metodos.get("Transferencia", 0.00),
            usuario
        )
        if success:
            actualizar_resumen()
            actualizar_tabla()

    Button(frame_superior, text="Hacer Corte", font=("Arial", 12), bg="#4CAF50", fg="white", width=15,
           command=hacer_corte).pack(pady=10)

    frame_inferior = Frame(frame_centrado, bg="#E6F0FA")
    frame_inferior.pack(fill="both", expand=True, pady=10)

    Label(frame_inferior, text="Cortes Históricos", font=("Arial", 14, "bold"), bg="#E6F0FA").pack(pady=5)

    frame_buscador = Frame(frame_inferior, bg="#E6F0FA")
    frame_buscador.pack(fill="x", pady=5)
    Label(frame_buscador, text="Buscar por Fecha (YYYY-MM-DD):", bg="#E6F0FA", font=("Arial", 12)).pack(side="left", padx=(10, 2))
    entry_fecha = Entry(frame_buscador, font=("Arial", 12), width=15)
    entry_fecha.pack(side="left", padx=(0, 10))
    Button(frame_buscador, text="Buscar", font=("Arial", 10), bg="#2196F3", fg="white",
           command=lambda: actualizar_tabla(entry_fecha.get().strip())).pack(side="left", padx=5)

    frame_tabla = Frame(frame_inferior, bg="#E6F0FA")
    frame_tabla.pack(padx=10, fill="both", expand=True)
    tabla = ttk.Treeview(frame_tabla, columns=campos_historicos, show="headings", height=12)
    for col in campos_historicos:
        tabla.heading(col, text=col)
        tabla.column(col, width=120)
    tabla.pack(pady=10, fill="both", expand=True)

    def actualizar_resumen():
        fecha = datetime.now().strftime('%Y-%m-%d')
        corte_data = ver_corte_de_caja(fecha)
        total_var.set(f"{corte_data['total']:.2f}")
        num_ventas_var.set(str(corte_data['num_ventas']))
        for tipo, var in metodos_vars.items():
            var.set(f"{corte_data['metodos'].get(tipo, 0.00):.2f}")
        actualizar_cajeros(corte_data['cajeros'])

    def actualizar_tabla(fecha=None):
        cortes = ver_cortes_historicos(fecha)
        for row in tabla.get_children():
            tabla.delete(row)
        for corte in cortes:
            id_corte, fecha_corte, total, num_ventas, efectivo, tarjeta, transferencia, usuario = corte
            tabla.insert("", "end", values=(id_corte, fecha_corte, total, num_ventas, efectivo, tarjeta, transferencia, usuario))

    actualizar_resumen()
    actualizar_tabla()

    return frame_principal

if __name__ == "__main__":
    interfaz_corte_de_caja()