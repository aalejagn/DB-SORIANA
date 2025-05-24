import mysql.connector
from tkinter import messagebox

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

def buscar_cliente(telefono):
    conexion = obtener_conexion()
    if not conexion:
        return None
    cursor = conexion.cursor()
    query = "SELECT nombre, apellidos, telefono, direccion, rfc, correo FROM clientes WHERE telefono = %s"
    valores = (telefono,)
    try:
        cursor.execute(query, valores)
        row = cursor.fetchone()
        print(f"Resultado de búsqueda para {telefono}: {row}")
        return row
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Hubo un problema al buscar el cliente: {err}")
        return None
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

def buscar_catalogo(codigo):
    conexion = obtener_conexion()
    if not conexion:
        return False
    
    cursor = conexion.cursor()
    query = """
    SELECT codigo, nombre, descripcion FROM categorias WHERE codigo = %s
    """
    valores = (codigo,)
    
    try:
        cursor.execute(query, valores)
        row = cursor.fetchone()
        print(f"Resultado de busqueda para {codigo}: {row}")
        return row
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Hubo un problema al buscar el catalogo: {e}")
        return None
    
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

def buscar_trabajador(id_empleado):
    conexion = obtener_conexion()
    if not conexion:
        return None

    cursor = conexion.cursor()
    query = """
    SELECT id_empleado, nombre, apellidos, telefono, edad, puesto, sueldo, fecha_contratacion, rfc
    FROM empleados WHERE id_empleado = %s
    """
    valores = (id_empleado,)

    try:
        cursor.execute(query, valores)
        row = cursor.fetchone()
        print(f"Resultado de la busqueda para el id_empleado {id_empleado}: {row}")
        return row
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Hubo un problema al buscar el trabajador {e}")
        return None
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
    query = "DELETE FROM proveedor WHERE id_proveedor = %s"
    valores = (id_proveedor,)
    try:
        cursor.execute(query, valores)
        conexion.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Exito", "Proveedor eliminado correctamente")
        else:
            messagebox.showwarning("Error", "No se encontro el proveedor")
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Hubo un problema al eliminar el proveedor {e}")
    finally:
        cursor.close()
        conexion.close()

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

def buscar_proveedor(id_proveedor):
    conexion = obtener_conexion()
    if not conexion:
        return None
    cursor = conexion.cursor()
    query = """
    SELECT id_proveedor, nombre, telefono, empresa, descripcion
    FROM proveedor WHERE id_proveedor = %s
    """
    valores = (id_proveedor,)
    try :
        cursor.execute(query, valores)
        row = cursor.fetchone()
        print(f"Resultado de busqueda para id_proveedor {id_proveedor}: {row}")
        return row
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Hubo un problema al buscar el proveedor: {e}")
        return None
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

def buscar_metodo_de_pago(id_metodo):
    conexion = obtener_conexion()
    if not conexion:
        return None
    cursor = conexion.cursor()
    query = """
    SELECT id_metodo, tipo, descripcion
    FROM metodo_de_pago WHERE id_metodo = %s
    """
    valores = (id_metodo,)
    try:
        cursor.execute(query, valores)
        row = cursor.fetchone()
        print(f"Resultado de busqueda para id_metodo {id_metodo}: {row}")
        return row
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Hubo un problema al buscar el metodo de pago: {e}")
        return None
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
    query = "DELETE FROM unidades WHERE id_unidad = %s"
    valores = (id_unidad,)
    try:
        cursor.execute(query, valores)
        conexion.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Exito", "Unidad eliminada correctamente")
        else:
            messagebox.showwarning("Error", "No se encontro la unidad")
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Hubo un problema al eliminar la unidad {e}")
    finally:
        cursor.close()
        conexion.close()

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

def buscar_unidad(id_unidad):
    conexion = obtener_conexion()
    if not conexion:
        return None
    cursor = conexion.cursor()
    query = """
    SELECT id_unidad, nombre, descripcion
    FROM unidades WHERE id_unidad = %s
    """
    valores = (id_unidad,)
    try:
        cursor.execute(query, valores)
        row = cursor.fetchone()
        print(f"Resultado de busqueda para id_unidad {id_unidad}: {row}")
        return row
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Hubo un problema al buscar la unidad: {e}")
        return None
    finally:
        cursor.close()
        conexion.close()


# TODO: MANEJO DE FUNCIONES PARA EL DB SORIANA CON ARTICULOS

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
    query = "DELETE FROM articulos WHERE codigo = %s"
    valores = (codigo,)
    
    try:
        cursor.execute(query, valores)
        conexion.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Éxito", "Artículo eliminado correctamente")
        else:
            messagebox.showwarning("No encontrado", "No se encontró el artículo")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Hubo un problema al eliminar el artículo: {err}")
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

def buscar_articulo(codigo):
    conexion = obtener_conexion()
    if not conexion:
        return None
    
    cursor = conexion.cursor()
    query = """
    SELECT codigo, nombre, precio, costo, existencia, descripcion, fecha_caducidad, categoria_codigo, id_proveedor, id_unidad 
    FROM articulos WHERE codigo = %s
    """
    valores = (codigo,)
    
    try:
        cursor.execute(query, valores)
        row = cursor.fetchone()
        print(f"Resultado de búsqueda para {codigo}: {row}")
        return row
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Hubo un problema al buscar el artículo: {err}")
        return None
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
        
# Crear la tabla e inicializar usuarios al iniciar el programa
inicializar_usuarios()
