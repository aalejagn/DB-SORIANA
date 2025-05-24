-- Eliminar la base de datos si existe
DROP DATABASE IF EXISTS db23270631;

-- Crear la base de datos
CREATE DATABASE db23270631;

-- Usar la base de datos
USE db23270631;

-- Creación de la tabla de empleados
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

-- Creación de la tabla de categorías
CREATE TABLE categorias (
    codigo VARCHAR(10) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- Creación de la tabla de clientes
CREATE TABLE clientes (
    nombre VARCHAR(40) NOT NULL,
    apellidos VARCHAR(50) NOT NULL, 
    telefono VARCHAR(15) PRIMARY KEY,
    direccion TEXT NOT NULL,
    rfc VARCHAR(13) NOT NULL UNIQUE,
    correo VARCHAR(100) NOT NULL
);

-- Creación de la tabla de métodos de pago
CREATE TABLE metodo_de_pago (
    id_metodo VARCHAR(2) PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL,
    descripcion TEXT
);

-- Creación de la tabla de proveedores
CREATE TABLE proveedor (
    id_proveedor VARCHAR(2) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    empresa VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- Creación de la tabla de unidades
CREATE TABLE unidades (
    id_unidad VARCHAR(2) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- Creación de la tabla de usuarios
CREATE TABLE usuarios (
    usuario VARCHAR(50) PRIMARY KEY,
    contraseña VARCHAR(50) NOT NULL
);

-- Inserciones para la tabla empleados
INSERT INTO empleados (id_empleado, nombre, apellidos, telefono, edad, puesto, sueldo, fecha_contratacion, rfc) VALUES
('01', 'Juan', 'Pérez Gómez', '9614567890', 30, 'Cajero', 12000.50, '2023-01-15', 'PEGJ930415HDF'),
('02', 'María', 'López Ramírez', '9615678901', 28, 'Gerente', 25000.75, '2022-06-01', 'LORM950622MDF'),
('03', 'Carlos', 'Martínez Díaz', '9616789012', 35, 'Almacenista', 15000.00, '2021-09-10', 'MADC870910HDF');

-- Inserciones para la tabla categorias
INSERT INTO categorias (codigo, nombre, descripcion) VALUES
('CAT001', 'Lácteos', 'Productos derivados de la leche'),
('CAT002', 'Carnes', 'Carnes frescas y procesadas'),
('CAT003', 'Abarrotes', 'Productos no perecederos');

-- Inserciones para la tabla clientes
INSERT INTO clientes (nombre, apellidos, telefono, direccion, rfc, correo) VALUES
('Rodrigo', 'González López', '9611234567', 'Calle Central Poniente 123, Col. Centro, Tuxtla Gutiérrez, Chiapas', 'GOLR920515HCH', 'rodrigo.gonzalez@example.com'),
('Fernando', 'Sánchez Villanueva', '9612345678', 'Av. Las Granjas 456, Fracc. Las Granjas, Tuxtla Gutiérrez, Chiapas', 'SAVF890320MCH', 'fernando.sanchez@example.com'),
('Jothan', 'Gopar Toledo', '9613456789', 'Calle Patria Nueva 789, Col. Patria Nueva, Tuxtla Gutiérrez, Chiapas', 'GOTJ910725HCH', 'jothan.gopar@example.com');

-- Inserciones para la tabla metodo_de_pago
INSERT INTO metodo_de_pago (id_metodo, tipo, descripcion) VALUES
('01', 'Efectivo', 'Pago en moneda física'),
('02', 'Tarjeta de crédito', 'Pago con tarjeta de crédito bancaria'),
('03', 'Transferencia', 'Pago mediante transferencia electrónica');

-- Inserciones para la tabla proveedor
INSERT INTO proveedor (id_proveedor, nombre, telefono, empresa, descripcion) VALUES
('01', 'José', '9617890123', 'Lacteos del Valle', 'Proveedor de productos lácteos'),
('02', 'Laura', '9618901234', 'Carnes Finas SA', 'Proveedor de carnes de calidad'),
('03', 'Miguel', '9619012345', 'Abarrotes El Sol', 'Proveedor de productos no perecederos');

-- Inserciones para la tabla unidades
INSERT INTO unidades (id_unidad, nombre, descripcion) VALUES
('01', 'Kilogramo', 'Unidad de peso para productos a granel'),
('02', 'Litro', 'Unidad de volumen para líquidos'),
('03', 'Pieza', 'Unidad para productos individuales');

-- Inserciones para la tabla usuarios
INSERT INTO usuarios (usuario, contraseña) VALUES
('admin1', 'contraseña123'),
('cajero1', 'clave456'),
('gerente1', 'pass789');