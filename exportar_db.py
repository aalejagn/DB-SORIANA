import mysql.connector
import pandas as pd
from db_soriana import obtener_conexion
from tkinter import messagebox

def listar_tablas():
    """
    Obtiene una lista de las tablas disponibles en la base de datos.
    """
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SHOW TABLES")
        tablas = [row[0] for row in cursor.fetchall()]
        return tablas
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al listar tablas: {err}")
        return []
    finally:
        cursor.close()
        conexion.close()

def exportar_tabla_a_csv(nombre_tabla):
    """
    Exporta los datos de una tabla a un archivo CSV.
    """
    try:
        conexion = obtener_conexion()
        query = f"SELECT * FROM {nombre_tabla}"
        df = pd.read_sql(query, conexion)
        archivo_csv = f"{nombre_tabla}.csv"
        df.to_csv(archivo_csv, index=False)
        messagebox.showinfo("Éxito", f"Tabla {nombre_tabla} exportada a {archivo_csv}")
        return True
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al exportar tabla {nombre_tabla}: {err}")
        return False
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado: {e}")
        return False
    finally:
        conexion.close()