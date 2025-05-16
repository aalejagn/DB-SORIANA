-- Eliminar la base de datos si existe
DROP DATABASE IF EXISTS db23270631;

-- Crear la base de datos
CREATE DATABASE db23270631;

-- Usar la base de datos
USE db_soriana;

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
    id_metodo INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL,
    descripcion TEXT
);

-- Creación de la tabla de proveedores
CREATE TABLE proveedor (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    empresa VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- Creación de la tabla de unidades
CREATE TABLE unidades (
    id_unidad INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- Creación de la tabla de usuarios
CREATE TABLE usuarios (
    usuario VARCHAR(50) PRIMARY KEY,
    contraseña VARCHAR(50) NOT NULL
);