import mysql.connector
from tkinter import messagebox
from datetime import datetime
"""Hacemos la conexion de la base de datos"""
def obtener_conexion():
    try:
        return mysql.connector.connect(
            host="localhost",  # Host local
            user="root",
            password="23270631@",
            database="db23270631"
        )
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
        return None

# Funciones para clientes
def agregar_cliente(nombre, apellidos, telefono, direccion, rfc, correo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    query = """
    INSERT INTO clientes (nombre, apellidos, telefono, direccion, rfc, correo)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    valores = (nombre, apellidos, telefono, direccion, rfc, correo)
    
    try:
        cursor.execute(query, valores)
        conexion.commit()
        messagebox.showinfo("Exito", "Cliente agregado correctamente")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Hubo un problema al agregar el cliente: {err}")
    
    finally:
        cursor.close()
        conexion.close()

def ver_clientes(tabla):
    conexion = obtener_conexion()
    if not conexion:
        return False
    
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre, apellidos, telefono, direccion, rfc, correo FROM clientes")
        rows = cursor.fetchall()
        
        for row in tabla.get_children():
            tabla.delete(row)
        for row in rows:
            tabla.insert("", "end", values=row)
            
    except mysql.connector.Error as e:
        print(f"Error en la consulta {e}")
        
    finally:
        cursor.close()
        conexion.close()

def eliminar_cliente(telefono):
    conexion = obtener_conexion()
    if not conexion:
        return
    
    cursor = conexion.cursor()
    query = "DELETE FROM clientes WHERE telefono = %s"
    valores = (telefono,)
    
    try:
        cursor.execute(query, valores)
        conexion.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Exito", "Cliente eliminado correctamente")
        else:
            messagebox.showwarning("No encontrado", "No se encontro al cliente")
    except mysql.connector.Error as err:
        messagebox.showwarning("Error", f"Hubo un problema al eliminar al cliente. {err}")
    finally:
        cursor.close()
        conexion.close()

def actualizar_cliente(telefono_original, nombre, apellidos, telefono, direccion, rfc, correo):
    conexion = obtener_conexion()
    if not conexion:
        return
    
    cursor = conexion.cursor()
    query = """
    UPDATE clientes
    SET nombre = %s, apellidos = %s, telefono = %s, direccion = %s, rfc = %s, correo = %s
    WHERE telefono = %s
    """
    
    valores = (nombre, apellidos, telefono, direccion, rfc, correo, telefono_original)
    
    
    try:
        cursor.execute(query, valores)
        conexion.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Exito", "Cliente actualizado correctamente")
        else:
            messagebox.showinfo("Advertencia", "Cliente no encontrado")
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Hubo un problema al actualizar el cliente {e}")
    finally:
        cursor.close()
        conexion.close()

def buscar_cliente(criterio, valor):
    conexion = obtener_conexion()
    if not conexion:
        return []
    cursor = conexion.cursor()
    query = ""
    valores = ()
    
    if criterio == "telefono":
        query = "SELECT nombre, apellidos, telefono, direccion, rfc, correo FROM clientes WHERE telefono = %s"
        valores = (valor,)
    elif criterio == "nombre":
        query = "SELECT nombre, apellidos, telefono, direccion, rfc, correo FROM clientes WHERE CONCAT(nombre, ' ', apellidos) LIKE %s"
        valores = (f"%{valor}%",)
    
    try:
        cursor.execute(query, valores)
        rows = cursor.fetchall()
        return rows  # Retorna lista de clientes (puede ser vacía o con múltiples resultados)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Hubo un problema al buscar el cliente: {err}")
        return []
    finally:
        cursor.close()
        conexion.close()

# Funciones para categorias
def agregar_catalogo(codigo, nombre, descripcion):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = """
    INSERT INTO categorias (codigo, nombre, descripcion)
    VALUES (%s, %s, %s)
    """
    valores = (codigo, nombre, descripcion)
    try:
        cursor.execute(query, valores)
        conexion.commit()
        messagebox.showinfo("Exito", "El catalogo se ha agregado")
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Hubo un problema al agregar el catalogo {e}")
    
    finally:
        cursor.close()
        conexion.close()

def ver_catalogo(tabla):
    conexion = obtener_conexion()
    if not conexion:
        return False
    
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT codigo, nombre, descripcion FROM categorias")
        rows = cursor.fetchall()
        
        for row in tabla.get_children():
            tabla.delete(row)
        for row in rows:
            tabla.insert("", "end", values=row)
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error en la consulta de {e}")
    finally:
        cursor.close()
        conexion.close()

def eliminar_catalogo(codigo):
    conexion = obtener_conexion()
    if not conexion:
        return False
    
    cursor = conexion.cursor()
    query = "DELETE FROM categorias WHERE codigo = %s"
    valores = (codigo,)
    
    try:
        cursor.execute(query, valores)
        conexion.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Exito", "Catalogo eliminado")
        else:
            messagebox.showwarning("Error", "No se encontro el catalogo")
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Hubo un problema al eliminar el catalogo {e}")
    finally:
        cursor.close()
        conexion.close()

def actualizar_catalogo(codigo_original, codigo, nombre, descripcion):
    conexion = obtener_conexion()
    if not conexion:
        return False
    
    cursor = conexion.cursor()
    
    query = """
    UPDATE categorias
    SET codigo = %s, nombre = %s, descripcion = %s WHERE codigo = %s
    """
    
    valores = (codigo, nombre, descripcion, codigo_original)
    
    try:
        cursor.execute(query, valores)
        conexion.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Exito", "Catalogo actualizado correctamente")
        else:
            messagebox.showinfo("Advertencia", "Catalogo no encontrado")
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Hubo un problema al actualizar el catalogo {e}")
    
    finally:
        cursor.close()
        conexion.close()

def buscar_catalogo(criterio, valor):
    conexion = obtener_conexion()
    if not conexion:
        return []
    cursor = conexion.cursor()
    query = ""
    valores = ()
    
    if criterio == "codigo":
        query = "SELECT codigo, nombre, descripcion FROM categorias WHERE codigo = %s"
        valores = (valor,)
    elif criterio == "nombre":
        query = "SELECT codigo, nombre, descripcion FROM categorias WHERE nombre LIKE %s"
        valores = (f"%{valor}%",)
    
    try:
        cursor.execute(query, valores)
        rows = cursor.fetchall()
        return rows
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Hubo un problema al buscar el catálogo: {e}")
        return []
    finally:
        cursor.close()
        conexion.close()

# Funciones para empleados
def agregar_empleado(nombre, apellidos, telefono, edad, puesto, sueldo, fecha_contratacion, rfc):
    conexion = obtener_conexion()
    if not conexion:
        return False
    cursor = conexion.cursor()
    query = """
    INSERT INTO empleados (nombre, apellidos, telefono, edad, puesto, sueldo, fecha_contratacion, rfc)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    valores = (nombre, apellidos, telefono, edad, puesto, sueldo, fecha_contratacion, rfc)
    try:
        print(f"Valores enviados a la base de datos: {valores}")
        cursor.execute(query, valores)
        conexion.commit()
        messagebox.showinfo("Éxito", "Empleado agregado correctamente")
        return True
    except mysql.connector.Error as e:
        if e.errno == 1062:
            messagebox.showerror("Error", f"Ya existe un empleado con el RFC: {rfc}")
        else:
            messagebox.showerror("Error", f"Hubo un problema al agregar el empleado: {str(e)}")
        return False
    finally:
        cursor.close()
        conexion.close()

def ver_empleado(tabla):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id_empleado, nombre, apellidos, telefono, edad, puesto, sueldo, fecha_contratacion, rfc FROM empleados")
        rows = cursor.fetchall()
        for row in tabla.get_children():
            tabla.delete(row)
        for row in rows:
            tabla.insert("", "end", values=row)
        return True
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error en la consulta: {str(e)}")
        return False
    finally:
        cursor.close()
        conexion.close()

def eliminar_empleado(id_empleado):
    conexion = obtener_conexion()
    if not conexion:
        return False

    cursor = conexion.cursor()
    query = "DELETE FROM empleados WHERE id_empleado = %s"
    valores = (id_empleado,)

    try:
        cursor.execute(query, valores)
        conexion.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Exito", "Empleado eliminado correctamente")
        else:
            messagebox.showwarning("Error", "No se encontro el empleado")
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Hubo un problema al eliminar el empleado {e}")
    finally:
        cursor.close()
        conexion.close()

def actualizar_empleado(id_empleado_original, nombre, apellidos, telefono, edad, puesto, sueldo, fecha_contratacion, rfc):
    conexion = obtener_conexion()
    if not conexion:
        return False

    cursor = conexion.cursor()
    query = """
    UPDATE empleados
    SET nombre = %s, apellidos = %s, telefono = %s, edad = %s, puesto = %s, sueldo = %s, fecha_contratacion = %s, rfc = %s
    WHERE id_empleado = %s
    """
    valores = (nombre, apellidos, telefono, edad, puesto, sueldo, fecha_contratacion, rfc, id_empleado_original)
    try:
        cursor.execute(query, valores)
        conexion.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Exito", "Empleado actualizado correctamente")
        else:
            messagebox.showinfo("Advertencia", "Empleado no encontrado")
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Hubo un problema al actualizar el empleado {e}")
    finally:
        cursor.close()
        conexion.close()

def buscar_trabajador(criterio, valor):
    conexion = obtener_conexion()
    if not conexion:
        return []
    cursor = conexion.cursor()
    query = ""
    valores = ()
    
    if criterio == "id_empleado":
        query = "SELECT id_empleado, nombre, apellidos, telefono, edad, puesto, sueldo, fecha_contratacion, rfc FROM empleados WHERE id_empleado = %s"
        valores = (valor,)
    elif criterio == "telefono":
        query = "SELECT id_empleado, nombre, apellidos, telefono, edad, puesto, sueldo, fecha_contratacion, rfc FROM empleados WHERE telefono LIKE %s"
        valores = (f"%{valor}%",)  # Coincidencia parcial
    elif criterio == "nombre":
        query = "SELECT id_empleado, nombre, apellidos, telefono, edad, puesto, sueldo, fecha_contratacion, rfc FROM empleados WHERE CONCAT(nombre, ' ', apellidos) LIKE %s"
        valores = (f"%{valor}%",)
    
    try:
        cursor.execute(query, valores)
        rows = cursor.fetchall()
        return rows
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Hubo un problema al buscar el trabajador: {e}")
        return []
    finally:
        cursor.close()
        conexion.close()

# Funciones para proveedor
def agregar_proveedor(id_proveedor, nombre, telefono, empresa, descripcion):
    conexion = obtener_conexion()
    if not conexion:
        return False
    cursor = conexion.cursor()
    query = """
    INSERT INTO proveedor (id_proveedor, nombre, telefono, empresa, descripcion)
    VALUES (%s, %s, %s, %s, %s)
    """
    valores = (id_proveedor, nombre, telefono, empresa, descripcion)
    try:
        cursor.execute(query, valores)
        conexion.commit()
        messagebox.showinfo("Exito", "Proveedor agregado correctamente")
        return True
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Hubo un problema al agregar el proveedor: {str(e)}")
        return False
    finally:
        cursor.close()
        conexion.close()

def ver_proveedor(tabla):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id_proveedor, nombre, telefono, empresa, descripcion FROM proveedor")
        rows = cursor.fetchall()
        for row in tabla.get_children():
            tabla.delete(row)
        for row in rows:
            tabla.insert("", "end", values=row)
        return True
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error en la consulta: {str(e)}")
        return False
    finally:
        cursor.close()
        conexion.close()

def eliminar_proveedor(id_proveedor):
    conexion = obtener_conexion()
    if not conexion:
        return False
    
    cursor = conexion.cursor()
    
    try:
        # Verificar si el proveedor está en uso por algún artículo
        query_check_articulos = "SELECT COUNT(*) FROM articulos WHERE id_proveedor = %s"
        cursor.execute(query_check_articulos, (id_proveedor,))
        if cursor.fetchone()[0] > 0:
            messagebox.showerror("Error", "No se puede eliminar el proveedor porque está asociado a al menos un artículo.")
            return False

        # Verificar si el proveedor está en uso por algún detalle de compra
        query_check_compras = "SELECT COUNT(*) FROM detalle_compras WHERE id_proveedor = %s"
        cursor.execute(query_check_compras, (id_proveedor,))
        if cursor.fetchone()[0] > 0:
            messagebox.showerror("Error", "No se puede eliminar el proveedor porque está asociado a al menos una compra.")
            return False

        # Eliminar el proveedor
        query = "DELETE FROM proveedor WHERE id_proveedor = %s"
        cursor.execute(query, (id_proveedor,))
        conexion.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Éxito", "Proveedor eliminado correctamente")
        else:
            messagebox.showwarning("Error", "No se encontró el proveedor")
    except mysql.connector.Error as e:
        conexion.rollback()
        messagebox.showerror("Error", f"Hubo un problema al eliminar el proveedor: {e}")
    finally:
        cursor.close()
        conexion.close()

    return cursor.rowcount > 0

def actualizar_proveedor(id_proveedor_original, id_proveedor, nombre, telefono, empresa, descripcion):
    conexion = obtener_conexion()
    if not conexion:
        return False
    cursor = conexion.cursor()
    query = """
    UPDATE proveedor
    SET id_proveedor = %s, nombre = %s, telefono = %s, empresa = %s, descripcion = %s
    WHERE id_proveedor = %s
    """
    valores = (id_proveedor, nombre, telefono, empresa, descripcion, id_proveedor_original)
    try:
        cursor.execute(query, valores)
        conexion.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Exito", "Proveedor actualizado correctamente")
        else:
            messagebox.showinfo("Advertencia", "Proveedor no encontrado")
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Hubo un problema al actualizar el proveedor {e}")
    finally:
        cursor.close()
        conexion.close()

def buscar_proveedor(criterio, valor):
    conexion = obtener_conexion()
    if not conexion:
        return []
    cursor = conexion.cursor()
    query = ""
    valores = ()
    
    if criterio == "id_proveedor":
        query = "SELECT id_proveedor, nombre, telefono, empresa, descripcion FROM proveedor WHERE id_proveedor = %s"
        valores = (valor,)
    elif criterio == "telefono":
        query = "SELECT id_proveedor, nombre, telefono, empresa, descripcion FROM proveedor WHERE telefono LIKE %s"
        valores = (f"%{valor}%",)
    elif criterio == "nombre":
        query = "SELECT id_proveedor, nombre, telefono, empresa, descripcion FROM proveedor WHERE nombre LIKE %s"
        valores = (f"%{valor}%",)
    
    try:
        cursor.execute(query, valores)
        rows = cursor.fetchall()
        return rows
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Hubo un problema al buscar el proveedor: {e}")
        return []
    finally:
        cursor.close()
        conexion.close()

# Funciones para metodo de pago
def agregar_metodo_de_pago(id_metodo, tipo, descripcion):
    conexion = obtener_conexion()
    if not conexion:
        return False
    cursor = conexion.cursor()
    query = """
    INSERT INTO metodo_de_pago (id_metodo, tipo, descripcion)
    VALUES (%s, %s, %s)
    """
    valores = (id_metodo, tipo, descripcion)
    try:
        cursor.execute(query, valores)
        conexion.commit()
        messagebox.showinfo("Exito", "Metodo de pago agregado correctamente")
        return True
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Hubo un problema al agregar el metodo de pago: {str(e)}")
        return False
    finally:
        cursor.close()
        conexion.close()

def ver_metodo_de_pago(tabla):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id_metodo, tipo, descripcion FROM metodo_de_pago")
        rows = cursor.fetchall()
        for row in tabla.get_children():
            tabla.delete(row)
        for row in rows:
            tabla.insert("", "end", values=row)
        return True
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error en la consulta: {str(e)}")
        return False
    finally:
        cursor.close()
        conexion.close()

def eliminar_metodo_de_pago(id_metodo):
    conexion = obtener_conexion()
    if not conexion:
        return False
    cursor = conexion.cursor()
    query = "DELETE FROM metodo_de_pago WHERE id_metodo = %s"
    valores = (id_metodo,)
    try:
        cursor.execute(query, valores)
        conexion.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Exito", "Metodo de pago eliminado correctamente")
        else:
            messagebox.showwarning("Error", "No se encontro el metodo de pago")
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Hubo un problema al eliminar el metodo de pago {e}")
    finally:
        cursor.close()
        conexion.close()

def actualizar_metodo_de_pago(id_metodo_original, id_metodo, tipo, descripcion):
    conexion = obtener_conexion()
    if not conexion:
        return False
    cursor = conexion.cursor()
    query = """
    UPDATE metodo_de_pago
    SET id_metodo = %s, tipo = %s, descripcion = %s
    WHERE id_metodo = %s
    """
    valores = (id_metodo, tipo, descripcion, id_metodo_original)
    try:
        cursor.execute(query, valores)
        conexion.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Exito", "Metodo de pago actualizado correctamente")
        else:
            messagebox.showinfo("Advertencia", "Metodo de pago no encontrado")
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Hubo un problema al actualizar el metodo de pago {e}")
    finally:
        cursor.close()
        conexion.close()

def buscar_metodo_de_pago(criterio, valor):
    conexion = obtener_conexion()
    if not conexion:
        return []
    cursor = conexion.cursor()
    query = ""
    valores = ()
    
    if criterio == "id_metodo":
        query = "SELECT id_metodo, tipo, descripcion FROM metodo_de_pago WHERE id_metodo = %s"
        valores = (valor,)
    elif criterio == "tipo":
        query = "SELECT id_metodo, tipo, descripcion FROM metodo_de_pago WHERE tipo LIKE %s"
        valores = (f"%{valor}%",)
    
    try:
        cursor.execute(query, valores)
        rows = cursor.fetchall()
        return rows
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Hubo un problema al buscar el método de pago: {e}")
        return []
    finally:
        cursor.close()
        conexion.close()


# Funciones para unidades
def agregar_unidad(id_unidad, nombre, descripcion):
    conexion = obtener_conexion()
    if not conexion:
        return False
    cursor = conexion.cursor()
    query = """
    INSERT INTO unidades (id_unidad, nombre, descripcion)
    VALUES (%s, %s, %s)
    """
    valores = (id_unidad, nombre, descripcion)
    try:
        cursor.execute(query, valores)
        conexion.commit()
        messagebox.showinfo("Exito", "Unidad agregada correctamente")
        return True
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Hubo un problema al agregar la unidad: {str(e)}")
        return False
    finally:
        cursor.close()
        conexion.close()

def ver_unidad(tabla):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id_unidad, nombre, descripcion FROM unidades")
        rows = cursor.fetchall()
        for row in tabla.get_children():
            tabla.delete(row)
        for row in rows:
            tabla.insert("", "end", values=row)
        return True
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error en la consulta: {str(e)}")
        return False
    finally:
        cursor.close()
        conexion.close()

def eliminar_unidad(id_unidad):
    conexion = obtener_conexion()
    if not conexion:
        return False
    
    cursor = conexion.cursor()
    
    try:
        # Verificar si la unidad está en uso por algún artículo
        query_check = "SELECT COUNT(*) FROM articulos WHERE id_unidad = %s"
        cursor.execute(query_check, (id_unidad,))
        if cursor.fetchone()[0] > 0:
            messagebox.showerror("Error", "No se puede eliminar la unidad porque está en uso por al menos un artículo.")
            return False

        # Eliminar la unidad
        query = "DELETE FROM unidades WHERE id_unidad = %s"
        cursor.execute(query, (id_unidad,))
        conexion.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Éxito", "Unidad eliminada correctamente")
        else:
            messagebox.showwarning("Error", "No se encontró la unidad")
    except mysql.connector.Error as e:
        conexion.rollback()
        messagebox.showerror("Error", f"Hubo un problema al eliminar la unidad: {e}")
    finally:
        cursor.close()
        conexion.close()

    return cursor.rowcount > 0

def actualizar_unidad(id_unidad_original, id_unidad, nombre, descripcion):
    conexion = obtener_conexion()
    if not conexion:
        return False
    cursor = conexion.cursor()
    query = """
    UPDATE unidades
    SET id_unidad = %s, nombre = %s, descripcion = %s
    WHERE id_unidad = %s
    """
    valores = (id_unidad, nombre, descripcion, id_unidad_original)
    try:
        cursor.execute(query, valores)
        conexion.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Exito", "Unidad actualizada correctamente")
        else:
            messagebox.showinfo("Advertencia", "Unidad no encontrada")
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Hubo un problema al actualizar la unidad {e}")
    finally:
        cursor.close()
        conexion.close()

def buscar_unidad(criterio, valor):
    conexion = obtener_conexion()
    if not conexion:
        return []
    cursor = conexion.cursor()
    query = ""
    valores = ()
    
    if criterio == "id_unidad":
        query = "SELECT id_unidad, nombre, descripcion FROM unidades WHERE id_unidad = %s"
        valores = (valor,)
    elif criterio == "nombre":
        query = "SELECT id_unidad, nombre, descripcion FROM unidades WHERE nombre LIKE %s"
        valores = (f"%{valor}%",)
    
    try:
        cursor.execute(query, valores)
        rows = cursor.fetchall()
        return rows
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Hubo un problema al buscar la unidad: {e}")
        return []
    finally:
        cursor.close()
        conexion.close()


# TODO: MANEJO DE FUNCIONES PARA EL DB SORIANA CON articulos

def agregar_articulo(codigo, nombre, precio, costo, existencia, descripcion, fecha_caducidad, categoria_codigo, id_proveedor, id_unidad):
    conexion = obtener_conexion()
    if not conexion:
        return
    
    cursor = conexion.cursor()
    
    query = """
    INSERT INTO articulos (codigo, nombre, precio, costo, existencia, descripcion, fecha_caducidad, categoria_codigo, id_proveedor, id_unidad)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    valores = (codigo, nombre, precio, costo, existencia, descripcion, fecha_caducidad, categoria_codigo, id_proveedor, id_unidad)
    
    try:
        cursor.execute(query, valores)
        conexion.commit()
        messagebox.showinfo("Éxito", "Artículo agregado correctamente")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Hubo un problema al agregar el artículo: {err}")
    finally:
        cursor.close()
        conexion.close()

def ver_articulos(tabla):
    conexion = obtener_conexion()
    if not conexion:
        return False
    
    try:
        cursor = conexion.cursor()
        query = """
        SELECT codigo, nombre, precio, costo, existencia, descripcion, fecha_caducidad, categoria_codigo, id_proveedor, id_unidad 
        FROM articulos
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Clear existing table data
        for row in tabla.get_children():
            tabla.delete(row)
        
        # Insert new data into the table
        for row in rows:
            tabla.insert("", "end", values=row)
            
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error en la consulta: {e}")
        return False
    finally:
        cursor.close()
        conexion.close()
    return True

def eliminar_articulos(codigo):
    conexion = obtener_conexion()
    if not conexion:
        return
    
    cursor = conexion.cursor()
    
    try:
        # Verificar si el artículo existe primero
        query_check = "SELECT codigo FROM articulos WHERE codigo = %s"
        cursor.execute(query_check, (codigo,))
        if not cursor.fetchone():
            messagebox.showwarning("No encontrado", f"El artículo con código {codigo} no existe en la base de datos.")
            return

        # Iniciar transacción
        query_delete_detalles_ventas = "DELETE FROM detalles_ventas WHERE codigo_articulo = %s"
        cursor.execute(query_delete_detalles_ventas, (codigo,))

        query_delete_detalles_compras = "DELETE FROM detalle_compras WHERE codigo_articulo = %s"
        cursor.execute(query_delete_detalles_compras, (codigo,))

        # Establecer a NULL las llaves foráneas antes de eliminar (si el esquema lo permite)
        query_update = """
        UPDATE articulos 
        SET categoria_codigo = NULL, id_proveedor = NULL, id_unidad = NULL 
        WHERE codigo = %s
        """
        cursor.execute(query_update, (codigo,))

        # Eliminar el artículo
        query_articulo = "DELETE FROM articulos WHERE codigo = %s"
        cursor.execute(query_articulo, (codigo,))
        
        conexion.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Éxito", f"Artículo con código {codigo} y registros asociados eliminados correctamente")
        else:
            messagebox.showwarning("No encontrado", f"No se pudo eliminar el artículo con código {codigo}.")
    except mysql.connector.Error as err:
        conexion.rollback()
        messagebox.showerror("Error", f"Error al eliminar el artículo: {err}")
    finally:
        cursor.close()
        conexion.close()


def actualizar_articulo(codigo, nombre, precio, costo, existencia, descripcion, fecha_caducidad, categoria_codigo, id_proveedor, id_unidad):
    conexion = obtener_conexion()
    if not conexion:
        return
    
    cursor = conexion.cursor()
    query = """
    UPDATE articulos
    SET nombre = %s, precio = %s, costo = %s, existencia = %s, descripcion = %s, fecha_caducidad = %s, 
        categoria_codigo = %s, id_proveedor = %s, id_unidad = %s
    WHERE codigo = %s
    """
    valores = (nombre, precio, costo, existencia, descripcion, fecha_caducidad, categoria_codigo, id_proveedor, id_unidad, codigo)
    
    try:
        cursor.execute(query, valores)
        conexion.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Éxito", "Artículo actualizado correctamente")
        else:
            messagebox.showinfo("Advertencia", "Artículo no encontrado")
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Hubo un problema al actualizar el artículo: {e}")
    finally:
        cursor.close()
        conexion.close()

def buscar_articulo(criterio, valor):
    conexion = obtener_conexion()
    if not conexion:
        return []
    cursor = conexion.cursor()
    query = ""
    valores = ()
    
    if criterio == "codigo":
        query = "SELECT codigo, nombre, precio, costo, existencia, descripcion, fecha_caducidad, categoria_codigo, id_proveedor, id_unidad FROM articulos WHERE codigo = %s"
        valores = (valor,)
    elif criterio == "nombre":
        query = "SELECT codigo, nombre, precio, costo, existencia, descripcion, fecha_caducidad, categoria_codigo, id_proveedor, id_unidad FROM articulos WHERE nombre LIKE %s"
        valores = (f"%{valor}%",)
    
    try:
        cursor.execute(query, valores)
        rows = cursor.fetchall()
        return rows
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Hubo un problema al buscar el artículo: {e}")
        return []
    finally:
        cursor.close()
        conexion.close()


def inicializar_usuarios():
    """
    Inserta usuarios predeterminados si no existen.
    """
    usuarios_predeterminados = [
        ("gerente", "2327")
    ]
    
    conexion = obtener_conexion()
    if not conexion:
        return

    cursor = conexion.cursor()
    try:
        for usuario, contraseña in usuarios_predeterminados:
            query = "INSERT IGNORE INTO usuarios (usuario, contraseña) VALUES (%s, %s)"
            cursor.execute(query, (usuario, contraseña))
        conexion.commit()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al inicializar usuarios: {err}")
    finally:
        cursor.close()

        conexion.close()
"""Nuevos cambios"""
def agregar_venta(usuario, articulos, telefono):
    """
    Registra una venta en la base de datos.
    Args:
        usuario: Nombre del usuario (cajero).
        articulos: Lista de tuplas (código, nombre, precio, cantidad, subtotal, id_metodo).
        telefono: Teléfono del cliente (opcional).
    Returns:
        bool: True si la venta se registró correctamente, False en caso de error.
    """
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        # Insertar en la tabla ventas
        query_venta = """
        INSERT INTO ventas (fecha, usuario, telefono)
        VALUES (%s, %s, %s)
        """
        fecha = datetime.now()
        valores_venta = (fecha, usuario, telefono)
        cursor.execute(query_venta, valores_venta)
        id_venta = cursor.lastrowid

        # Insertar en la tabla detalles_ventas
        query_detalle = """
        INSERT INTO detalles_ventas (id_venta, codigo_articulo, cantidad, subtotal, id_metodo)
        VALUES (%s, %s, %s, %s, %s)
        """
        for item in articulos:
            codigo, _, precio, cantidad, subtotal, id_metodo = item
            valores_detalle = (id_venta, codigo, cantidad, subtotal, id_metodo)
            cursor.execute(query_detalle, valores_detalle)
            
            # Actualizar el articulo
            query_update = "UPDATE articulos SET existencia = existencia - %s WHERE codigo = %s"
            cursor.execute(query_update, (cantidad, codigo))

        conexion.commit()
        return True
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error al registrar la venta: {e}")
        conexion.rollback()
        return False
    finally:
        cursor.close()
        conexion.close()


def actualizar_stock(codigo, cantidad):
    conexion = obtener_conexion()
    if not conexion:
        return
    cursor = conexion.cursor()
    query = "UPDATE articulos SET existencia = existencia - %s WHERE codigo = %s"
    valores = (cantidad, codigo)
    try:
        cursor.execute(query, valores)
        conexion.commit()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al actualizar stock: {err}")
    finally:
        cursor.close()
        conexion.close()

def buscar_articulo_por_nombre(nombre):
    conexion = obtener_conexion()
    if not conexion:
        return []
    cursor = conexion.cursor()
    query = """
    SELECT codigo, nombre, precio, costo, existencia, descripcion, fecha_caducidad, categoria_codigo, id_proveedor, id_unidad 
    FROM articulos WHERE nombre LIKE %s
    """
    valores = (f"%{nombre}%",)
    try:
        cursor.execute(query, valores)
        rows = cursor.fetchall()
        return rows
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al buscar artículo por nombre: {err}")
        return []
    finally:
        cursor.close()
        conexion.close()


def registrar_venta(codigo_articulo):
    conexion = obtener_conexion()
    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return
    cursor = conexion.cursor()
    query = "INSERT INTO ventas (codigo_articulo, fecha_venta) VALUES (%s, NOW())"
    valores = (codigo_articulo,)
    try:
        cursor.execute(query, valores)
        conexion.commit()
        # TODO: Mostrar mensaje de éxito opcional para depuración
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al registrar venta: {err}")
    finally:
        cursor.close()
        conexion.close()

def agregar_compra(supervisor, articulos):
    conexion = obtener_conexion()
    if not conexion:
        return
    try:
        cursor = conexion.cursor()
        # Insertar en tabla compras
        total = sum(float(item[4]) for item in articulos)
        id_metodo = articulos[0][5]  # Asumimos que todos los artículos usan el mismo método de pago
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(
            "INSERT INTO compras (supervisor, fecha, total, id_metodo) VALUES (%s, %s, %s, %s)",
            (supervisor, fecha, total, id_metodo)
        )
        id_compra = cursor.lastrowid
        # Insertar en detalle_compras y actualizar stock
        for articulo in articulos:
            codigo, _, costo, cantidad, subtotal, id_metodo, id_proveedor = articulo
            cursor.execute(
                "INSERT INTO detalle_compras (id_compra, codigo_articulo, cantidad, subtotal, id_proveedor) "
                "VALUES (%s, %s, %s, %s, %s)",
                (id_compra, codigo, cantidad, subtotal, id_proveedor)
            )
            cursor.execute(
                "UPDATE articulos SET existencia = existencia + %s WHERE codigo = %s",
                (cantidad, codigo)
            )
        conexion.commit()
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error al registrar compra: {e}")
        conexion.rollback()
    finally:
        cursor.close()
        conexion.close()



def ver_ventas(tabla):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        query = """
        SELECT v.id_venta, v.fecha, v.usuario, SUM(d.subtotal) as total
        FROM ventas v
        JOIN detalles_ventas d ON v.id_venta = d.id_venta
        GROUP BY v.id_venta, v.fecha, v.usuario
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in tabla.get_children():
            tabla.delete(row)
        for row in rows:
            tabla.insert("", "end", values=row)
        return True
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error al mostrar ventas: {e}")
        return False
    finally:
        cursor.close()
        conexion.close()

def ver_historia_venta(fecha, tabla):
    """
    Muestra el historial de ventas para una fecha específica en la tabla proporcionada.
    Incluye ID Venta, Fecha, Usuario, Rol, Teléfono, Artículo, Cantidad, Subtotal, Método de Pago y Total por venta.
    Args:
        fecha: Fecha en formato YYYY-MM-DD para filtrar las ventas.
        tabla: Objeto Treeview donde se mostrarán los datos.
    Returns:
        bool: True si la operación fue exitosa, False en caso de error.
    """
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        query = """
        SELECT v.id_venta, v.fecha, v.usuario, u.rol, COALESCE(v.telefono, '') AS telefono,
               a.nombre, d.cantidad, d.subtotal, m.tipo,
               SUM(d2.subtotal) AS total_venta
        FROM ventas v
        JOIN usuarios u ON v.usuario = u.usuario
        JOIN detalles_ventas d ON v.id_venta = d.id_venta
        JOIN articulos a ON d.codigo_articulo = a.codigo
        JOIN metodo_de_pago m ON d.id_metodo = m.id_metodo
        JOIN detalles_ventas d2 ON v.id_venta = d2.id_venta
        WHERE DATE(v.fecha) = %s
        GROUP BY v.id_venta, v.fecha, v.usuario, u.rol, v.telefono, a.nombre, d.cantidad, d.subtotal, m.tipo
        ORDER BY v.fecha DESC
        """
        cursor.execute(query, (fecha,))
        rows = cursor.fetchall()
        
        # Limpia las filas existentes en la tabla
        for row in tabla.get_children():
            tabla.delete(row)
        
        if not rows:
            messagebox.showinfo("Información", f"No se encontraron ventas para la fecha {fecha}")
            return True
        
        for row in rows:
            # Formatea la fecha y los valores numéricos
            formatted_row = (
                row[0],  # id_venta
                row[1].strftime('%Y-%m-%d %H:%M:%S'),  # fecha
                row[2],  # usuario
                row[3],  # rol (now from usuarios table)
                row[4],  # telefono
                row[5],  # nombre artículo
                row[6],  # cantidad
                f"{row[7]:.2f}",  # subtotal
                row[8],  # método de pago
                f"{row[9]:.2f}"  # total_venta
            )
            tabla.insert("", "end", values=formatted_row)
        return True
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error al mostrar historial de ventas: {e}")
        return False
    finally:
        cursor.close()
        conexion.close()

def ver_corte_de_caja(fecha):
    conexion = obtener_conexion()
    if not conexion:
        return {"ventas": [], "total": 0.00, "num_ventas": 0, "metodos": {}, "cajeros": {}}
    cursor = conexion.cursor()
    query = """
    SELECT v.id_venta, v.fecha, v.usuario, d.subtotal, m.tipo
    FROM ventas v
    JOIN detalles_ventas d ON v.id_venta = d.id_venta
    JOIN metodo_de_pago m ON d.id_metodo = m.id_metodo
    WHERE DATE(v.fecha) = %s
    """
    valores = (fecha,)
    try:
        cursor.execute(query, valores)
        rows = cursor.fetchall()
        total = 0.00
        num_ventas = len(set(row[0] for row in rows))
        metodos = {"Efectivo": 0.00, "Tarjeta de crédito": 0.00, "Transferencia": 0.00}
        cajeros = {}
        ventas = []
        for row in rows:
            id_venta, fecha, usuario, subtotal, tipo_metodo = row
            ventas.append((id_venta, fecha, usuario, subtotal))
            total += float(subtotal)
            if tipo_metodo in metodos:
                metodos[tipo_metodo] += float(subtotal)
            cajeros[usuario] = cajeros.get(usuario, 0.00) + float(subtotal)
        return {"ventas": ventas, "total": total, "num_ventas": num_ventas, "metodos": metodos, "cajeros": cajeros}
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error al obtener el corte de caja: {e}")
        return {"ventas": [], "total": 0.00, "num_ventas": 0, "metodos": {}, "cajeros": {}}
    finally:
        cursor.close()
        conexion.close()
        
def ver_historia_compra(fecha, tabla):
    conexion = obtener_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        query = """
        SELECT c.id_compra, c.fecha, c.supervisor, a.nombre, d.cantidad, d.subtotal, m.tipo, p.nombre, p.id_proveedor
        FROM compras c
        JOIN detalle_compras d ON c.id_compra = d.id_compra
        JOIN articulos a ON d.codigo_articulo = a.codigo
        JOIN metodo_de_pago m ON c.id_metodo = m.id_metodo
        JOIN proveedor p ON d.id_proveedor = p.id_proveedor
        WHERE DATE(c.fecha) = %s
        """
        cursor.execute(query, (fecha,))
        rows = cursor.fetchall()
        for row in tabla.get_children():
            tabla.delete(row)
        for row in rows:
            tabla.insert("", "end", values=row)
        return True
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error al mostrar historial de compras: {e}")
        return False
    finally:
        cursor.close()
        conexion.close()


def registrar_corte_de_caja(fecha, total, num_ventas, efectivo, tarjeta_credito, transferencia, usuario):
    conexion = obtener_conexion()
    if not conexion:
        return False
    cursor = conexion.cursor()
    query = """
    INSERT INTO cortes_de_caja (fecha, total, num_ventas, efectivo, tarjeta_credito, tarjeta_debito, transferencia, usuario)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    valores = (fecha, total, num_ventas, efectivo, tarjeta_credito, 0.00, transferencia, usuario)  # Add tarjeta_debito as 0.00
    try:
        cursor.execute(query, valores)
        conexion.commit()
        messagebox.showinfo("Éxito", f"Corte de caja del {fecha} registrado correctamente")
        return True
    except mysql.connector.Error as e:
        if e.errno == 1062:
            messagebox.showerror("Error", f"Ya existe un corte de caja para la fecha {fecha}")
        else:
            messagebox.showerror("Error", f"Error al registrar el corte de caja: {e}")
        return False
    finally:
        cursor.close()
        conexion.close()

def ver_cortes_historicos(fecha=None):
    conexion = obtener_conexion()
    if not conexion:
        return []
    cursor = conexion.cursor()
    query = """
    SELECT id_corte, fecha, total, num_ventas, efectivo, tarjeta_credito, transferencia, usuario
    FROM cortes_de_caja
    """
    valores = ()
    if fecha:
        query += " WHERE DATE(fecha) = %s"
        valores = (fecha,)
    try:
        cursor.execute(query, valores)
        rows = cursor.fetchall()
        return rows
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error al obtener los cortes históricos: {e}")
        return []
    finally:
        cursor.close()
        conexion.close()
        conexion.close()

def buscar_cliente(campo, valor):
    conexion = obtener_conexion()
    if not conexion:
        print("Error: No se pudo conectar a la base de datos")
        return None
    try:
        cursor = conexion.cursor()
        query = f"SELECT nombre, apellidos, telefono, direccion, rfc, correo FROM clientes WHERE {campo} = %s"
        cursor.execute(query, (valor,))  
        resultado = cursor.fetchone()  
        return resultado
    except mysql.connector.Error as e:
        print(f"Error al buscar cliente: {e}")
        return None
    finally:
        cursor.close()
        conexion.close()

        
# Crear la tabla e inicializar usuarios al iniciar el programa
inicializar_usuarios()
