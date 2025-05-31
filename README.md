# DBSoriana 🛒

**DBSoriana** es una aplicación de escritorio chida, desarrollada en Python con Tkinter, que te permite gestionar una base de datos MySQL llamada `db_soriana`. Es un sistema completo con operaciones CRUD (Crear, Leer, Actualizar, Eliminar) para manejar empleados, categorías, proveedores, métodos de pago, unidades, clientes, usuarios, ventas e historial de compras. Además, tiene control de acceso por roles (Gerente y Trabajador) para que todo sea seguro y cada quien tenga lo que necesita.

## ✨ Características

- **Gestión de Usuarios**: Agrega, actualiza o elimina usuarios (menos el usuario "gerente") con roles bien definidos.
- **Sesiones Rifadas**: Inicia y cierra sesión con una lista de usuarios que se actualiza al momento.
- **Manejo de Entidades**: Controla clientes, empleados, categorías, proveedores, métodos de pago, unidades y ventas con operaciones CRUD.
- **Ventas a Todo Dar**: Registra ventas, genera tickets y vincula clientes con validación de inventario en tiempo real.
- **Historial de Compras**: Revisa compras pasadas filtradas por fecha, con totales calculados al vuelo.
- **Roles Bien Puestos**: Los Gerentes tienen acceso total (empleados, usuarios, etc.); los Trabajadores solo a lo operativo.
- **Interfaz Chingona**: Hecha con Tkinter para que sea fácil de usar y se vea bonita.
- **Base de Datos a Prueba de Balas**: Se conecta sin broncas a MySQL para guardar todo seguro.

## 🛠 Requisitos

- **Python**: 3.8 o superior (¡que no te agarre en curva con versiones viejas!).
- **MySQL Server**: Que esté corriendo (usa MySQL Community Server, por ejemplo).
- **pip**: El manejador de paquetes de Python.
- **Sistema Operativo**: Windows, macOS o Linux, tú decides.

## 🚀 Configuración e Instalación

Sigue estos pasos para echar a andar **DBSoriana** en un entorno virtual. ¡Ponte trucha y no te saltes nada!

### 1. Clona o Descarga el Proyecto
Clona el repositorio o descarga los archivos a tu compu.

```bash
git clone <url-del-repositorio>
cd DBSoriana
```

### 2. Crea un Entorno Virtual
Crea un entorno virtual para mantener las dependencias separadas.

```bash
python -m venv env23270631
```

### 3. Activa el Entorno Virtual
Activa el entorno virtual para usar su Python aislado.

- **Windows**:
  ```bash
  .\env23270631\Scripts\activate
  ```

- **macOS/Linux**:
  ```bash
  source env23270631/bin/activate
  ```

Si todo sale bien, verás `(env23270631)` en tu terminal.

### 4. Checa los Paquetes Instalados
Revisa qué paquetes hay en el entorno virtual (deberían ser poquitos, como `pip` y `setuptools`).

```bash
pip list
```

### 5. Instala las Dependencias
Instala los paquetes que necesita el proyecto.

```bash
pip install mysql-connector-python tk
```

- **`mysql-connector-python`**: Para conectar con la base de datos MySQL.
- **`tk`**: Asegura que Tkinter esté listo (suele venir con Python, pero por si las dudas).

### 6. Configura la Base de Datos MySQL
1. **Arranca el Servidor MySQL**:
   Asegúrate de que MySQL esté corriendo.
   ```bash
   mysql.server start  # macOS
   sudo systemctl start mysql  # Linux
   net start mysql  # Windows
   ```

2. **Crea la Base de Datos**:
   Usa el script `23270631.sql` para crear la base de datos `db_soriana` y sus tablas.
   ```bash
   mysql -u root -p < 23270631.sql
   ```
   - Mete la contraseña de `root` cuando te la pida.
   - El script crea la base, tablas y mete datos iniciales (como el usuario "gerente").

3. **Verifica la Base de Datos**:
   Conéctate a MySQL y checa que todo esté en orden.
   ```bash
   mysql -u root -p
   ```
   ```sql
   SHOW DATABASES;
   USE db_soriana;
   SHOW TABLES;
   ```

### 7. Configura las Credenciales de la Base de Datos
Asegúrate de que el archivo `db_soriana.py` tenga las credenciales correctas.

1. Abre `db_soriana.py` en Visual Studio Code y revisa el diccionario `MYSQL_CONFIG`:
   ```python
   MYSQL_CONFIG = {
       'host': 'localhost',
       'user': 'root',
       'password': '23270631@',  # Cambia esto por tu contraseña de MySQL
       'database': 'db_soriana'
   }
   ```

2. Guarda el archivo. Si usas otro usuario, contraseña o host, cámbialos aquí.

### 8. Corre la Aplicación
Ejecuta el archivo principal para lanzar la aplicación.

```bash
python catalogos.py
```

O:
```bash
py catalogos.py
```

Se abrirá una ventana de Tkinter con la pantalla de login. Usa las credenciales predeterminadas (usuario: `gerente`, contraseña: `admin`) para entrar.

## 📂 Estructura del Proyecto

Aquí te desgloso qué hace cada archivo del proyecto:

- **`db_soriana.py`**  
  - La neta, este es el cerebro de la base de datos. Tiene la conexión a MySQL y todas las funciones para hacer operaciones CRUD (como `agregar_venta`, `buscar_cliente`, `ver_historia_compra`).
  - Define `MYSQL_CONFIG` para conectar con la base.
  - Se usa en todos los módulos para interactuar con la base de datos.

- **`catalogos.py`**  
  - El punto de arranque de la aplicación.
  - Muestra la pantalla de login y controla la navegación.
  - Carga secciones (Ventas, Empleados, etc.) según el rol del usuario, con una barra lateral bien chida.

- **`ventas.py`**  
  - Maneja la interfaz de ventas (`crear_seccion_ventas`).
  - **Qué puedes hacer**:
    - Agregar, actualizar o quitar productos en una venta.
    - Calcular totales, procesar pagos y dar cambio.
    - Buscar clientes por teléfono o agregar nuevos.
    - Generar tickets en una ventana emergente con todos los detalles (artículos, total, pago, cliente).
  - Valida el inventario en tiempo real y se bloquea si hay corte de caja (`corte_de_caja`).
  - Usa `VentaEstado` para rastrear la venta actual.

- **`unidades.py`**  
  - Administra unidades de medida (Gramos, Litros, etc.) con operaciones CRUD.
  - Tiene una interfaz (`crear_seccion_unidades`) con tabla y campos para buscar, agregar, actualizar o eliminar.
  - Usa un `Combobox` con opciones predefinidas y barras de desplazamiento para la tabla.

- **`historial_compras.py`**  
  - Muestra el historial de compras filtrado por fecha (`crear_seccion_historia_compra`).
  - Te da detalles como ID de compra, fecha, supervisor, artículos y totales.
  - Calcula el total de las compras mostradas y valida que la fecha esté en formato YYYY-MM-DD.

- **`proveedor.py`**  
  - Gestiona proveedores con operaciones CRUD (`crear_seccion_proveedor`).
  - Puedes buscar por ID, nombre o teléfono y ver los detalles en una tabla.
  - Requiere que llenes todos los campos (ID, nombre, teléfono, empresa, descripción).

- **`metodo_de_pago.py`**  
  - Controla los métodos de pago (Efectivo, Tarjeta de Débito, etc.) con operaciones CRUD.
  - Interfaz similar a `proveedor.py` (`crear_seccion_metodo_de_pago`), con búsqueda por ID o tipo.
  - Usa un `Combobox` para elegir el tipo de pago.

- **`empleados.py`**  
  - Maneja los datos de empleados con operaciones CRUD.
  - Solo los Gerentes pueden acceder a este módulo.

- **`categorias.py`**  
  - Administra las categorías de productos con operaciones CRUD.
  - Interfaz similar a otros módulos de gestión.

- **`clientes.py`**  
  - Gestiona la info de clientes con operaciones CRUD.
  - Se usa en `ventas.py` para buscar o agregar clientes durante una venta.

- **`configuracion.py`**  
  - Se encarga de la autenticación y la gestión de usuarios.
  - Permite agregar, actualizar o eliminar usuarios (menos el "gerente").

- **`configuracion_interfaz.py`**  
  - Tiene las interfaces Tkinter para la gestión de usuarios (formularios y demás).
  - Trabaja junto con `configuracion.py`.

- **`23270631.sql`**  
  - Script SQL para crear la base de datos `db_soriana`, sus tablas y datos iniciales.
  - Incluye tablas como `usuarios`, `clientes`, `ventas`, `proveedores`, etc.

## 🧠 Cómo Funciona

### Autenticación y Roles
- **Login**: Inicias sesión en `catalogos.py`, que checa tus credenciales contra la tabla `usuarios` en `db_soriana`.
- **Roles**:
  - **Gerente**: Tiene acceso total a todo (ventas, empleados, usuarios, historial, etc.).
  - **Trabajador**: Solo puede hacer ventas, ver historial de compras y gestionar cosas básicas.
- La barra lateral se ajusta según tu rol, para que no te pierdas.

### Ventas (`ventas.py`)
- **Cómo Jala**:
  1. Mete el código del producto y la cantidad para añadirlo.
  2. Elige el método de pago (Efectivo, Tarjeta). Si es efectivo, pon cuánto te dieron para calcular el cambio.
  3. Si quieres, mete el teléfono del cliente para vincular la venta (puedes buscarlo o agregar uno nuevo).
  4. Confirma la venta para guardarla y limpia la pantalla.
  5. Genera un ticket con todos los detalles.
- **Lo Chido**:
  - Checa el inventario en tiempo real para no vender de más.
  - Los tickets se ven en una ventana emergente con todo bien formateado.
  - Si ya hubo corte de caja, las ventas se bloquean hasta el siguiente día.

### Historial de Compras (`historial_compras.py`)
- **Cómo Jala**:
  1. Pon una fecha (YYYY-MM-DD) para ver las compras de ese día.
  2. Mira una tabla con ID, fecha, supervisor, artículos, etc.
  3. Checa el total de las compras mostradas.
- **Lo Chido**:
  - Valida que la fecha esté bien escrita.
  - Suma los totales al momento.

### Gestión de Entidades (`unidades.py`, `proveedor.py`, `metodo_de_pago.py`, etc.)
- **Cómo Jala**:
  1. Busca registros por ID, nombre, etc., o mira todos.
  2. Agrega, actualiza o elimina usando los campos y botones.
  3. Limpia todo para empezar de nuevo.
- **Lo Chido**:
  - Tablas con barras de desplazamiento para manejar muchos datos.
  - Comboboxes con opciones predefinidas.
  - Valida que no dejes campos vacíos.

### Base de Datos
- Todo lo de la base de datos pasa por `db_soriana.py`, que usa `mysql-connector-python`.
- Las funciones están organizadas por entidad (como `agregar_unidad`) para que sea fácil de mantener.
- Las conexiones se manejan bien para no tener broncas.

## 🛑 Si Algo Falla

- **No Conecta con MySQL**:
  - Checa que el servidor esté corriendo y que las credenciales en `db_soriana.py` estén correctas.
  - Asegúrate de que `db_soriana` exista (`SHOW DATABASES;` en MySQL).

- **Falta un Módulo**:
  - Verifica que el entorno virtual esté activado y las dependencias instaladas (`pip list`).
  - Reinstala si hace falta: `pip install mysql-connector-python tk`.

- **No Sale la Ventana de Tkinter**:
  - Confirma que Tkinter está en tu Python (`python -m tkinter`).
  - Revisa que no haya conflictos con otras bibliotecas.

- **Error de Corte de Caja**:
  - Si no puedes hacer ventas, checa la tabla `cortes_de_caja` para la fecha actual.
  - Solo se permite un corte por día.

## 🤝 ¿Quieres Aportar?

Si quieres meterle mano al proyecto:
1. Haz un fork del repositorio.
2. Crea una rama nueva (`git checkout -b mi-funcionalidad`).
3. Haz tus cambios y commitea (`git commit -m "Añadí algo chido"`).
4. Sube tu rama (`git push origin mi-funcionalidad`).
5. Abre un pull request.

## 📜 Licencia

Este proyecto está bajo la **Licencia MIT**. Échale un ojo al archivo `LICENSE` para los detalles.

## 📩 Contacto

Si tienes dudas o quieres platicar, escribe al mantenedor en [tu-correo@ejemplo.com].

---

¡Échale un ojo en Visual Studio Code y déjalo correr! Si necesitas que le meta más salsa o quieres que revise algo más, nomás dime, compa. 😎