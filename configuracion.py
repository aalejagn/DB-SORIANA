from tkinter import messagebox

# Clase base para Configuración de usuarios
class Configuracion:
    usuarios = {"gerente": "1234", "trabajador": "4321"}  # Usuarios por defecto

    def __init__(self, usuario_actual):
        self.usuario_actual = usuario_actual.lower()

    def verificar_credenciales(self, usuario, contraseña):
        return usuario.lower() in self.usuarios and self.usuarios[usuario.lower()] == contraseña

    def modificar_contraseña(self, usuario, nueva_contraseña):
        if self.usuario_actual != "gerente":
            messagebox.showerror("Error", "Solo el gerente puede cambiar contraseñas.")
            return False
        
        if usuario.lower() in self.usuarios:
            self.usuarios[usuario.lower()] = nueva_contraseña
            messagebox.showinfo("Éxito", f"Contraseña actualizada para {usuario}")
            return True
        else:
            messagebox.showwarning("Advertencia", "Usuario no encontrado.")
            return False

    def agregar_usuario(self, usuario, contraseña):
        if self.usuario_actual != "gerente":
            messagebox.showerror("Error", "Solo el gerente puede agregar usuarios.")
            return False
        
        if usuario.lower() in self.usuarios:
            messagebox.showwarning("Advertencia", "Usuario ya existe.")
            return False
        
        self.usuarios[usuario.lower()] = contraseña
        messagebox.showinfo("Éxito", f"Usuario {usuario} agregado.")
        return True

    def eliminar_usuario(self, usuario):
        if self.usuario_actual != "gerente":
            messagebox.showerror("Error", "Solo el gerente puede eliminar usuarios.")
            return False
        
        if usuario.lower() == "gerente":
            messagebox.showerror("Error", "No se puede eliminar al usuario gerente.")
            return False
        
        if usuario.lower() in self.usuarios:
            del self.usuarios[usuario.lower()]
            messagebox.showinfo("Éxito", f"Usuario {usuario} eliminado.")
            return True
        else:
            messagebox.showwarning("Advertencia", "Usuario no encontrado.")
            return False

# Clase para exportar base de datos
class BaseDeDatosCSV(Configuracion):
    def __init__(self, usuario_actual):
        super().__init__(usuario_actual)

    def exportar(self):
        # Aquí iría la lógica para exportar la BD a CSV
        pass