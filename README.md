
# DBSoriana

Este es un proyecto de aplicación de escritorio desarrollada en Python con Tkinter para gestionar una base de datos MySQL llamada `db_soriana`.  
La aplicación permite administrar empleados, categorías, proveedores, métodos de pago y unidades dentro de un sistema de gestión.

---

# Pasos para configurar y ejecutar el proyecto

### Paso 1. Crear la base de datos
Ejecuta el script SQL para crear la base de datos y las tablas.

**Ubicación:**  
`C:\Users\aleja\Desktop\4SEMESTRE\TOPICOS AVANZADOS\SegundaUnidad\PRACTICA12-CRUDs de catalogos\db_soriana.sql`

---

### Paso 2. Abrir el proyecto en Visual Studio Code
1. Clona o descarga el repositorio en tu máquina local.  
2. Abre la carpeta del proyecto en **Visual Studio Code**.

---

### Paso 3. Crear el entorno virtual
Desde la terminal en Visual Studio Code, navega al directorio del proyecto y ejecuta:

```bash
python -m venv venv
```

---

### Paso 4. Instalar `mysql-connector-python`
Activa el entorno virtual:

- En Windows:
```bash
venv\Scripts\activate
```

Luego instala la dependencia:

```bash
pip install mysql-connector-python
```

---

### Paso 5. Configurar la conexión a la base de datos
Asegúrate de que el archivo `db_soriana.py` esté configurado con las credenciales correctas:

- Usuario: `root`  
- Contraseña: `23270631@`  
- Base de datos: `db_soriana`

---

### Ejecutar la aplicación
Desde la terminal, con el entorno virtual activado, ejecuta el archivo principal:

```bash
python empleados.py
```

La interfaz gráfica debería abrirse mostrando la sección correspondiente.

---

## 📁 Estructura del proyecto

- `db_soriana.py`: Conexión y funciones para la base de datos.
- `empleados.py`: Gestión de empleados.
- `categorias.py`: Gestión de categorías.
- `proveedor.py`: Gestión de proveedores.
- `metodo_de_pago.py`: Gestión de métodos de pago.
- `unidades.py`: Gestión de unidades.
- `DBSoriana.sql`: Script para crear la base de datos y las tablas.

---

# Requisitos

- Python 3.x  
- MySQL Server  
- `mysql-connector-python` (instalable con `pip`)
