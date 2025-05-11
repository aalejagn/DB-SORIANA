import mysql.connector
from tkinter import messagebox
import re
from db_soriana import obtener_conexion

# Clase base para Configuración de usuarios
class Configuracion:
    def __init__(self, usuario_actual):
        self.usuario_actual = usuario_actual.lower()
        # Asegurarnos que la tabla existe al inicializar
        self.crear_tabla_si_no_existe()

    def crear_tabla_si_no_existe(self):
        conexion = obtener_conexion()
        if not conexion:
            return False

        cursor = conexion.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    usuario VARCHAR(50) PRIMARY KEY,
                    contraseña VARCHAR(50) NOT NULL
                )
            """)
            conexion.commit()
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al verificar tabla usuarios: {err}")
            return False
        finally:
            cursor.close()
            conexion.close()

    def verificar_credenciales(self, usuario, contraseña):
        """Verifica si las credenciales son correctas"""
        usuarios = self.obtener_usuarios()
        return usuario.lower() in usuarios and usuarios[usuario.lower()] == contraseña

    def obtener_usuarios(self):
        """Obtiene todos los usuarios con sus contraseñas"""
        if not self.crear_tabla_si_no_existe():
            return {}

        conexion = obtener_conexion()
        if not conexion:
            return {}

        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT usuario, contraseña FROM usuarios")
            return {row[0].lower(): row[1] for row in cursor.fetchall()}
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al obtener usuarios: {err}")
            return {}
        finally:
            cursor.close()
            conexion.close()

    def modificar_contraseña(self, usuario, nueva_contraseña):
        if self.usuario_actual != "gerente":
            messagebox.showerror("Error", "Solo el gerente puede cambiar contraseñas.")
            return False
        
        if not self.validar_nombre_usuario(usuario):
            return False
        
        conexion = obtener_conexion()
        if not conexion:
            return False

        cursor = conexion.cursor()
        try:
            # Verificar si el usuario existe
            cursor.execute("SELECT usuario FROM usuarios WHERE usuario = %s", (usuario.lower(),))
            if not cursor.fetchone():
                messagebox.showwarning("Advertencia", "Usuario no encontrado.")
                return False

            # Actualizar contraseña
            cursor.execute("UPDATE usuarios SET contraseña = %s WHERE usuario = %s", 
                         (nueva_contraseña, usuario.lower()))
            conexion.commit()
            messagebox.showinfo("Éxito", f"Contraseña actualizada para {usuario}")
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al actualizar contraseña: {err}")
            return False
        finally:
            cursor.close()
            conexion.close()

    def agregar_usuario(self, usuario, contraseña):
        if self.usuario_actual != "gerente":
            messagebox.showerror("Error", "Solo el gerente puede agregar usuarios.")
            return False
        
        if not self.validar_nombre_usuario(usuario) or not self.validar_contraseña(contraseña):
            return False
        
        conexion = obtener_conexion()
        if not conexion:
            return False

        cursor = conexion.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (usuario, contraseña) VALUES (%s, %s)", 
                         (usuario.lower(), contraseña))
            conexion.commit()
            messagebox.showinfo("Éxito", f"Usuario {usuario} agregado.")
            return True
        except mysql.connector.IntegrityError:
            messagebox.showwarning("Advertencia", "El nombre de usuario ya existe. Elija otro.")
            return False
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al agregar usuario: {err}")
            return False
        finally:
            cursor.close()
            conexion.close()

    def eliminar_usuario(self, usuario):
        if self.usuario_actual != "gerente":
            messagebox.showerror("Error", "Solo el gerente puede eliminar usuarios.")
            return False
        
        if not self.validar_nombre_usuario(usuario):
            return False
        
        if usuario.lower() == "gerente":
            messagebox.showerror("Error", "No se puede eliminar al usuario gerente.")
            return False
        
        conexion = obtener_conexion()
        if not conexion:
            return False

        cursor = conexion.cursor()
        try:
            cursor.execute("DELETE FROM usuarios WHERE usuario = %s", (usuario.lower(),))
            if cursor.rowcount == 0:
                messagebox.showwarning("Advertencia", "Usuario no encontrado.")
                return False
                
            conexion.commit()
            messagebox.showinfo("Éxito", f"Usuario {usuario} eliminado.")
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al eliminar usuario: {err}")
            return False
        finally:
            cursor.close()
            conexion.close()

    def validar_nombre_usuario(self, usuario):
        """Valida que el nombre de usuario sea válido"""
        if not usuario:
            messagebox.showerror("Error", "El nombre de usuario no puede estar vacío.")
            return False
        if len(usuario) < 3:
            messagebox.showerror("Error", "El nombre de usuario debe tener al menos 3 caracteres.")
            return False
        if not re.match("^[a-zA-Z0-9_]+$", usuario):
            messagebox.showerror("Error", "El nombre de usuario solo puede contener letras, números y guiones bajos.")
            return False
        return True

    def validar_contraseña(self, contraseña):
        """Valida que la contraseña sea válida"""
        if len(contraseña) < 4:
            messagebox.showerror("Error", "La contraseña debe tener al menos 4 caracteres.")
            return False
        return True

# Clase para exportar base de datos
class BaseDeDatosCSV(Configuracion):
    def __init__(self, usuario_actual):
        super().__init__(usuario_actual)

    def exportar(self):
        # Aquí iría la lógica para exportar la BD a CSV
        pass