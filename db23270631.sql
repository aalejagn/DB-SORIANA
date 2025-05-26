-- Eliminar la base de datos si existe
DROP DATABASE IF EXISTS db23270631;

-- Crear la base de datos
CREATE DATABASE db23270631;

-- Usar la base de datos
USE db23270631;

-- Crear tablas sin dependencias primero
-- ================================================

-- Categorías
CREATE TABLE categorias (
    codigo VARCHAR(10) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- Proveedores
CREATE TABLE proveedor (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    empresa VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- Unidades
CREATE TABLE unidades (
    id_unidad INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- Empleados
CREATE TABLE empleados (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    edad INT NOT NULL,
    puesto VARCHAR(50) NOT NULL,
    sueldo DECIMAL(10, 2) NOT NULL,
    fecha_contratacion DATE NOT NULL,
    rfc VARCHAR(13) NOT NULL UNIQUE
);

-- Clientes
CREATE TABLE clientes (
    nombre VARCHAR(40) NOT NULL,
    apellidos VARCHAR(50) NOT NULL, 
    telefono VARCHAR(15) PRIMARY KEY,
    direccion TEXT NOT NULL,
    rfc VARCHAR(13) NOT NULL UNIQUE,
    correo VARCHAR(100) NOT NULL
);

-- Métodos de pago
CREATE TABLE metodo_de_pago (
    id_metodo INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL,
    descripcion TEXT
);

-- Usuarios
CREATE TABLE usuarios (
    usuario VARCHAR(50) PRIMARY KEY,
    contraseña VARCHAR(50) NOT NULL
);

-- Crear tablas con claves foráneas
-- ================================================

-- Artículos
CREATE TABLE articulos (
    codigo VARCHAR(25) PRIMARY KEY,
    nombre VARCHAR(100),
    precio DECIMAL(10,2),
    costo DECIMAL(10,2),
    existencia INT, 
    descripcion TEXT,
    fecha_caducidad DATE,
    categoria_codigo VARCHAR(10),
    id_proveedor INT,
    id_unidad INT,
    FOREIGN KEY (categoria_codigo) REFERENCES categorias(codigo),
    FOREIGN KEY (id_proveedor) REFERENCES proveedor(id_proveedor),
    FOREIGN KEY (id_unidad) REFERENCES unidades(id_unidad)
);

-- Ventas
CREATE TABLE ventas (
    id_venta INT AUTO_INCREMENT PRIMARY KEY,
    codigo_articulo VARCHAR(50) NOT NULL,
    fecha_venta DATETIME NOT NULL,
    FOREIGN KEY (codigo_articulo) REFERENCES articulos(codigo)
);

-- Insertar datos en las tablas
-- ================================================

-- Categorías
INSERT INTO categorias (codigo, nombre, descripcion) VALUES
('CAT1', 'Lácteos', 'Productos derivados de la leche'),
('CAT2', 'Panadería', 'Productos de panadería como pan, galletas, etc.'),
('CAT3', 'Higiene', 'Productos de higiene personal como jabón, shampoo, etc.'),
('CAT4', 'Endulzantes', 'Productos para endulzar como azúcar, miel, etc.'),
('CAT5', 'Granos', 'Granos básicos como arroz, frijoles, etc.'),
('CAT6', 'Limpieza', 'Productos de limpieza para el hogar como detergente, etc.'),
('CAT7', 'Harinas', 'Harinas de trigo, maíz, etc.'),
('CAT8', 'Aceites', 'Aceites comestibles para cocinar'),
('CAT9', 'Condimentos', 'Condimentos secos como sal, pimienta, etc.'),
('CAT10', 'Pastas', 'Pastas alimenticias como espagueti, macarrón, etc.'),
('CAT11', 'Leguminosas', 'Leguminosas como frijoles, lentejas, etc.'),
('CAT12', 'Enlatados', 'Productos enlatados como atún, vegetales, etc.'),
('CAT13', 'Pescados enlatados', 'Pescados enlatados como sardinas, atún, etc.'),
('CAT14', 'Aderezos', 'Aderezos como mayonesa, mostaza, etc.'),
('CAT15', 'Salsas', 'Salsas como kétchup, salsa de soya, etc.'),
('CAT16', 'Condimentos líquidos', 'Condimentos líquidos como mostaza, salsa inglesa, etc.'),
('CAT17', 'Bebidas', 'Bebidas no alcohólicas como jugos, refrescos, etc.'),
('CAT18', 'Galletas', 'Galletas dulces y saladas'),
('CAT19', 'Cereales', 'Cereales para desayuno'),
('CAT20', 'Mermeladas', 'Mermeladas y jaleas'),
('CAT21', 'Café y té', 'Café y té en sus diferentes presentaciones'),
('CAT22', 'Infusiones', 'Infusiones como té, manzanilla, etc.'),
('CAT23', 'Postres', 'Ingredientes para postres como leche condensada, etc.'),
('CAT24', 'Yogures', 'Yogures de diferentes sabores'),
('CAT25', 'Quesos', 'Quesos frescos y madurados'),
('CAT26', 'Mantequillas', 'Mantequillas y margarinas');

-- Proveedores
INSERT INTO proveedor (id_proveedor, nombre, telefono, empresa, descripcion) VALUES
(1, 'Proveedor1', '5551234567', 'Lala', 'Proveedor de lácteos'),
(5, 'Pedro Sánchez', '5550105', 'La Costeña', 'Proveedor de granos y enlatados'),
(6, 'Laura Ramírez', '5550106', 'Fabuloso', 'Proveedor de productos de limpieza'),
(7, 'Miguel Torres', '5550107', 'Maseca', 'Proveedor de harinas'),
(8, 'Sofía Díaz', '5550108', 'Mazola', 'Proveedor de aceites comestibles'),
(9, 'Luis Fernández', '5550109', 'La Sierra', 'Proveedor de condimentos'),
(10, 'Elena Vargas', '5550110', 'Barilla', 'Proveedor de pastas'),
(11, 'José Morales', '5550111', 'Verde Valle', 'Proveedor de leguminosas'),
(12, 'Carmen Ruiz', '5550112', 'Herdez', 'Proveedor de enlatados'),
(13, 'Ricardo Ortiz', '5550113', 'Dolores', 'Proveedor de pescados enlatados'),
(14, 'Patricia Castro', '5550114', 'McCormick', 'Proveedor de aderezos'),
(15, 'Fernando Silva', '5550115', 'Heinz', 'Proveedor de salsas'),
(16, 'Gabriela Méndez', '5550116', 'Dijon', 'Proveedor de condimentos líquidos'),
(17, 'Andrés Herrera', '5550117', 'Jumex', 'Proveedor de bebidas'),
(18, 'Verónica Flores', '5550118', 'Gamesa', 'Proveedor de galletas'),
(19, 'Raúl González', '5550119', 'Kellogg\'s', 'Proveedor de cereales'),
(20, 'Mónica Salazar', '5550120', 'La Morena', 'Proveedor de mermeladas'),
(21, 'Héctor Navarro', '5550121', 'Nescafé', 'Proveedor de café'),
(22, 'Diana Rojas', '5550122', 'Lipton', 'Proveedor de infusiones'),
(23, 'Pablo Mendoza', '5550123', 'Nestlé', 'Proveedor de postres'),
(24, 'Claudia Pineda', '5550124', 'Danone', 'Proveedor de yogures'),
(25, 'Esteban Cruz', '5550125', 'Chiapas', 'Proveedor de quesos'),
(26, 'Julia Espinoza', '5550126', 'Lurpak', 'Proveedor de mantequillas');

-- Unidades
INSERT INTO unidades (id_unidad, nombre, descripcion) VALUES
(1, 'Litro', 'Unidad de volumen para líquidos'),
(5, 'Kilogramo', 'Unidad de peso para granos (2 kg)'),
(6, 'Litro', 'Unidad de volumen para detergente'),
(7, 'Kilogramo', 'Unidad de peso para harina'),
(8, 'Litro', 'Unidad de volumen para aceite'),
(9, 'Gramo', 'Unidad de peso (500 g)'),
(10, 'Gramo', 'Unidad de peso para pasta (500 g)'),
(11, 'Kilogramo', 'Unidad de peso para frijoles'),
(12, 'Gramo', 'Unidad de peso para atún (140 g)'),
(13, 'Gramo', 'Unidad de peso para sardinas (120 g)'),
(14, 'Gramo', 'Unidad de peso para mayonesa (400 g)'),
(15, 'Gramo', 'Unidad de peso para kétchup (300 g)'),
(16, 'Gramo', 'Unidad de peso para mostaza (200 g)'),
(17, 'Litro', 'Unidad de volumen para jugo'),
(18, 'Gramo', 'Unidad de peso para galletas (200 g)'),
(19, 'Gramo', 'Unidad de peso para cereal (500 g)'),
(20, 'Gramo', 'Unidad de peso para mermelada (300 g)'),
(21, 'Gramo', 'Unidad de peso para café (250 g)'),
(22, 'Gramo', 'Unidad de peso para té (100 g)'),
(23, 'Gramo', 'Unidad de peso para leche condensada (400 g)'),
(24, 'Litro', 'Unidad de volumen para yogurt'),
(25, 'Gramo', 'Unidad de peso para queso (500 g)'),
(26, 'Gramo', 'Unidad de peso para mantequilla (200 g)');

-- Empleados
INSERT INTO empleados (id_empleado, nombre, apellidos, telefono, edad, puesto, sueldo, fecha_contratacion, rfc) VALUES
(1, 'Juan', 'Pérez Gómez', '9614567890', 30, 'Cajero', 12000.50, '2023-01-15', 'PEGJ930415HDF'),
(2, 'María', 'López Ramírez', '9615678901', 28, 'Gerente', 25000.75, '2022-06-01', 'LORM950622MDF'),
(3, 'Carlos', 'Martínez Díaz', '9616789012', 35, 'Almacenista', 15000.00, '2021-09-10', 'MADC870910HDF');

-- Clientes
INSERT INTO clientes (nombre, apellidos, telefono, direccion, rfc, correo) VALUES
('Rodrigo', 'González López', '9611234567', 'Calle Central Poniente 123, Col. Centro, Tuxtla Gutiérrez, Chiapas', 'GOLR920515HCH', 'rodrigo.gonzalez@example.com'),
('Fernando', 'Sánchez Villanueva', '9612345678', 'Av. Las Granjas 456, Fracc. Las Granjas, Tuxtla Gutiérrez, Chiapas', 'SAVF890320MCH', 'fernando.sanchez@example.com'),
('Jothan', 'Gopar Toledo', '9613456789', 'Calle Patria Nueva 789, Col. Patria Nueva, Tuxtla Gutiérrez, Chiapas', 'GOTJ910725HCH', 'jothan.gopar@example.com');

-- Métodos de pago
INSERT INTO metodo_de_pago (id_metodo, tipo, descripcion) VALUES
(1, 'Efectivo', 'Pago en moneda física'),
(2, 'Tarjeta de crédito', 'Pago con tarjeta de crédito bancaria'),
(3, 'Transferencia', 'Pago mediante transferencia electrónica');

-- Usuarios
INSERT INTO usuarios (usuario, contraseña) VALUES
('admin1', 'contraseña123'),
('cajero1', 'clave456'),
('gerente1', 'pass789');

-- Artículos
INSERT INTO articulos (codigo, nombre, precio, costo, existencia, descripcion, fecha_caducidad, categoria_codigo, id_proveedor, id_unidad) VALUES
('ABC123', 'Leche', 20.50, 15.00, 10, 'Leche entera 1L', '2025-12-31', 'CAT1', 1, 1),
('PQR678', 'Harina', 14.50, 11.00, 40, 'Harina de trigo 1kg', '2025-10-25', 'CAT7', 7, 7),
('STU901', 'Aceite', 25.00, 20.00, 35, 'Aceite vegetal 1L', '2026-02-15', 'CAT8', 8, 8),
('VWX234', 'Sal', 5.50, 4.00, 50, 'Sal de mesa 500g', '2025-12-01', 'CAT9', 9, 9),
('YZA567', 'Pasta', 8.00, 6.50, 45, 'Pasta espagueti 500g', '2025-11-30', 'CAT10', 10, 10),
('BCD890', 'Frijoles', 15.00, 12.00, 30, 'Frijoles negros 1kg', '2026-01-10', 'CAT11', 11, 11),
('EFG123', 'Atún', 18.00, 14.50, 25, 'Atún en lata 140g', '2025-09-15', 'CAT12', 12, 12),
('HIJ456', 'Sardinas', 12.50, 10.00, 20, 'Sardinas en lata 120g', '2025-08-20', 'CAT13', 13, 13),
('KLM789', 'Mayonesa', 22.00, 18.00, 15, 'Mayonesa 400g', '2025-07-30', 'CAT14', 14, 14),
('NOP012', 'Kétchup', 16.00, 13.00, 25, 'Kétchup 300g', '2025-10-10', 'CAT15', 15, 15),
('QRS345', 'MostF', 14.00, 11.50, 20, 'Mostaza 200g', '2025-09-05', 'CAT16', 16, 16),
('TUV678', 'Jugo', 10.00, 8.00, 30, 'Jugo de naranja 1L', '2025-06-15', 'CAT17', 17, 17),
('WXY901', 'Galletas', 9.50, 7.50, 40, 'Galletas de chocolate 200g', '2025-11-20', 'CAT18', 18, 18),
('ZAB234', 'Cereal', 28.00, 23.00, 15, 'Cereal de maíz 500g', '2025-12-15', 'CAT19', 19, 19),
('CDE567', 'Mermelada', 13.00, 10.00, 25, 'Mermelada de fresa 300g', '2025-08-25', 'CAT20', 20, 20),
('FGH890', 'Café', 35.00, 30.00, 20, 'Café molido 250g', '2026-04-10', 'CAT21', 21, 21),
('IJK123', 'Té', 20.00, 16.00, 30, 'Té negro 100g', '2025-10-30', 'CAT22', 22, 22),
('LMN456', 'Leche condensada', 18.50, 15.00, 25, 'Leche condensada 400g', '2025-07-15', 'CAT23', 23, 23),
('OPQ789', 'Yogurt', 7.00, 5.50, 35, 'Yogurt natural 1L', '2025-06-05', 'CAT24', 24, 24),
('RST012', 'Queso', 40.00, 35.00, 10, 'Queso fresco 500g', '2025-05-20', 'CAT25', 25, 25),
('UVW345', 'Mantequilla', 25.00, 20.00, 15, 'Mantequilla 200g', '2025-09-30', 'CAT26', 26, 26);

-- Ventas
INSERT INTO ventas (codigo_articulo, fecha_venta) VALUES
('ABC123', NOW());