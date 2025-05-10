# DBSoriana

Este es un proyecto de aplicación de escritorio desarrollada en Python con Tkinter para gestionar una base de datos MySQL llamada `db_soriana`.  
La aplicación permite administrar empleados, categorías, proveedores, métodos de pago y unidades dentro de un sistema de gestión.

### Pasos para configurar y ejecutar el proyecto

**Paso 1:** Ejecutar el script de la base de datos  
Ubicación sugerida del archivo SQL:  
`C:\Users\aleja\Desktop\4SEMESTRE\TOPICOS AVANZADOS\SegundaUnidad\DB SORIANA\db_soriana.sql`

**Paso 2:** Crear el entorno virtual  
```bash
python -m venv env23270631
```

**Paso 3:** Activar el entorno virtual  
```bash
.\env23270631\Scripts\ctivate
```

**Paso 4:** Verifica los paquetes instalados  
```bash
pip list
```

**Paso 5:** Instalar el conector de MySQL  
```bash
pip install mysql-connector
```

**Paso 6:** Instalar Tkinter (si es necesario)  
```bash
pip install tk
```

**Paso 7:** Crear o tener un archivo `.gitignore`  
Asegúrate de incluir el entorno virtual en el `.gitignore`.

**Paso 8:** Agregar `env23270631` al archivo `.gitignore` para excluirlo del repositorio.


**Paso 9:** Navegar a la carpeta del módulo deseado

**Paso 10:** Ejecutar el archivo con:  
```bash
python nombrearchivo.py
```
O bien:  
```bash
py nombrearchivo.py
```

---
### Requisitos

- Python 3.x  
- MySQL Server  
- `mysql-connector`  
- `tkinter`  

---

### Notas

- Asegúrate de que el archivo `db_soriana.py` esté correctamente configurado con las credenciales de acceso a MySQL.
- Verifica que el servidor de MySQL esté corriendo antes de ejecutar la aplicación.


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

