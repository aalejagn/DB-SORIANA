from tkinter import messagebox
from abc import ABC, abstractmethod

# Clase base para Configuración de usuarios
class Configuracion:
    usuarios = {"gerente": "1234"}  # usuarios por defecto

    def __init__(self, usuario_actual):
        self.usuario_actual = usuario_actual

    def verificar_credenciales(self, usuario, contraseña):
        return self.usuarios.get(usuario) == contraseña

    def modificar_contraseña(self, usuario, nueva_contraseña):
        if self.usuario_actual != "gerente":
            return messagebox.showerror("Error", "Solo el gerente puede cambiar contraseñas.")
        
        if usuario in self.usuarios:
            self.usuarios[usuario] = nueva_contraseña
            return messagebox.showinfo("Éxito", f"Contraseña actualizada para {usuario}")
        else:
            return messagebox.showwarning("Advertencia", "Usuario no encontrado.")

    def agregar_usuario(self, usuario, contraseña):
        if self.usuario_actual != "gerente":
            return messagebox.showerror("Error", "Solo el gerente puede agregar usuarios.")
        
        if usuario in self.usuarios:
            return messagebox.showwarning("Advertencia", "Usuario ya existe.")
        
        self.usuarios[usuario] = contraseña
        return messagebox.showinfo("Éxito", f"Usuario {usuario} agregado.")

    def eliminar_usuario(self, usuario):
        if self.usuario_actual != "gerente":
            return messagebox.showerror("Error", "Solo el gerente puede eliminar usuarios.")
        
        if usuario in self.usuarios:
            del self.usuarios[usuario]
            return messagebox.showinfo("Éxito", f"Usuario {usuario} eliminado.")
        else:
            return messagebox.showwarning("Advertencia", "Usuario no encontrado.")

# Clase abstracta para Ticket
class Ticket(ABC):
    @abstractmethod
    def crear_ticket(self, ticket, titulo, empresa, cantidad, iva):
        pass

# Clase para exportar base de datos (a implementar)
class BaseDeDatosCSV(Configuracion):
    def __init__(self, usuario_actual):
        super().__init__(usuario_actual)

    def exportar(self):
        # Aquí iría la lógica para exportar la BD a CSV
        pass
