# DBSoriana

Este es un proyecto de aplicación de escritorio desarrollada en Python con Tkinter para gestionar una base de datos MySQL llamada db_soriana. La aplicación proporciona un sistema CRUD (Crear, Leer, Actualizar, Eliminar) para administrar empleados, categorías, proveedores, métodos de pago, unidades, clientes y cuentas de usuario con acceso basado en roles (Gerente y Trabajador).


## Características

- **Gestión de Usuarios**: Permite agregar, actualizar y eliminar usuarios (excepto el usuario "gerente") con control de acceso basado en roles.
- **Manejo de Sesiones**: Funcionalidad de inicio y cierre de sesión con actualización dinámica de la lista de usuarios.
- **Gestión de Entidades**: Administra clientes, empleados, categorías, proveedores, métodos de pago y unidades mediante operaciones CRUD.
- **Acceso Basado en Roles**: Los usuarios Gerente tienen acceso a la gestión de empleados y configuración de usuarios; los usuarios Trabajador tienen acceso limitado.
- **Interfaz Responsiva**: Construida con Tkinter para una experiencia de usuario amigable.

## Requisitos

- Python 3.8 o superior
- Servidor MySQL (en ejecución y accesible)
- pip (administrador de paquetes de Python)

## Pasos para Configurar y Ejecutar el Proyecto

### Paso 1: Crear el Entorno Virtual
Crea un entorno virtual para aislar las dependencias del proyecto.

```bash
python -m venv env23270631
```

### Paso 2: Activar el Entorno Virtual
Activa el entorno virtual para instalar y ejecutar las dependencias.

```bash
.\env23270631\Scripts\activate
```

### Paso 3: Verificar Paquetes Instalados
Verifica los paquetes instalados en el entorno virtual.

```bash
pip list
```

### Paso 4: Instalar Dependencias Requeridas
Instala los paquetes necesarios para el proyecto.

```bash
pip install mysql-connector-python tk
```

- `mysql-connector-python`: Para la conectividad con la base de datos MySQL.
- `tk`

### Paso 5: Configurar la Base de Datos
1. **Ejecutar el Script SQL**:
   - Usa el script `db_soriana.sql` incluido en el proyecto para crear la base de datos y las tablas.
   - Ejecuta:
     ```bash
     mysql -u root -p < db_soriana.sql
     ```
   - Ingresa la contraseña de `root` cuando se solicite. 


### Paso 6: Actualizar la Configuración de la Base de Datos
Asegúrate de que el archivo `db_soriana.py` contenga las credenciales correctas de MySQL.

2. Verifica o actualiza la configuración:
   ```python
   MYSQL_CONFIG = {
       'host': 'localhost',
       'user': 'root',
       'password': '23270631@',
       'database': 'db_soriana'
   }
   ```

### Paso 7: Ejecutar la Aplicación
Ejecuta el archivo principal de la aplicación.

```bash
python catalogos.py
```

Alternativamente:
```bash
py catalogos.py
```

## Estructura del Proyecto

- `db_soriana.py`: Funciones de conexión y consultas para la base de datos MySQL.
- `empleados.py`: Interfaz y lógica para la gestión de empleados.
- `categorias.py`: Interfaz y lógica para la gestión de categorías.
- `proveedor.py`: Interfaz y lógica para la gestión de proveedores.
- `metodo_de_pago.py`: Interfaz y lógica para la gestión de métodos de pago.
- `unidades.py`: Interfaz y lógica para la gestión de unidades.
- `clientes.py`: Interfaz y lógica para la gestión de clientes.
- `configuracion.py`: Lógica para autenticación y gestión de usuarios.
- `configuracion_interfaz.py`: Interfaces Tkinter para la configuración de usuarios.
- `catalogos.py`: Punto de entrada principal con lógica de inicio de sesión y navegación.
- `db_soriana.sql`: Script SQL para crear la base de datos y las tablas.

