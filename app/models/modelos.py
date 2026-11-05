
from datetime import datetime

from sqlalchemy import Numeric
from app import db


# 1. CATEGORIAS
class Categoria(db.Model):
    __tablename__ = "categorias"

    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.String(250))
    estado = db.Column(db.Boolean, default=True, nullable=False)

    productos = db.relationship(
        "Producto",
        back_populates="categoria"
    )

    def __repr__(self):
        return self.nombre


# 2. PROVEEDORES
class Proveedor(db.Model):
    __tablename__ = "proveedores"

    id_proveedor = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(30))
    correo = db.Column(db.String(120))
    direccion = db.Column(db.String(200))
    estado = db.Column(db.Boolean, default=True, nullable=False)

    productos = db.relationship(
        "Producto",
        back_populates="proveedor"
    )

    def __repr__(self):
        return self.nombre


# 3. PRODUCTOS
class Producto(db.Model):
    __tablename__ = "productos"

    id_producto = db.Column(db.Integer, primary_key=True)

    id_categoria = db.Column(
        db.Integer,
        db.ForeignKey("categorias.id_categoria"),
        nullable=False
    )

    id_proveedor = db.Column(
        db.Integer,
        db.ForeignKey("proveedores.id_proveedor"),
        nullable=False
    )

    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.String(250))
    precio = db.Column(Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, default=0, nullable=False)
    stock_minimo = db.Column(db.Integer, default=1, nullable=False)
    imagen = db.Column(db.String(250))
    estado = db.Column(db.Boolean, default=True, nullable=False)

    categoria = db.relationship(
        "Categoria",
        back_populates="productos"
    )

    proveedor = db.relationship(
        "Proveedor",
        back_populates="productos"
    )

    detalles = db.relationship(
        "DetallePedido",
        back_populates="producto"
    )

    def __repr__(self):
        return self.nombre


# 4. CLIENTES
class Cliente(db.Model):
    __tablename__ = "clientes"

    id_cliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(30))
    correo = db.Column(db.String(120))
    direccion = db.Column(db.String(200))

    pedidos = db.relationship(
        "Pedido",
        back_populates="cliente"
    )

    def __repr__(self):
        return self.nombre


# 5. PEDIDOS
class Pedido(db.Model):
    __tablename__ = "pedidos"

    id_pedido = db.Column(db.Integer, primary_key=True)

    id_cliente = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id_cliente"),
        nullable=False
    )

    fecha_pedido = db.Column(db.DateTime, default=datetime.now)
    fecha_entrega = db.Column(db.DateTime)
    ocasion = db.Column(db.String(100))
    dedicatoria = db.Column(db.String(250))
    tipo_entrega = db.Column(db.String(50))
    direccion_entrega = db.Column(db.String(200))
    estado = db.Column(db.String(50), default="Pendiente")
    metodo_pago = db.Column(db.String(50))
    estado_pago = db.Column(db.String(50), default="Pendiente")
    total = db.Column(Numeric(10, 2), default=0)

    cliente = db.relationship(
        "Cliente",
        back_populates="pedidos"
    )

    detalles = db.relationship(
        "DetallePedido",
        back_populates="pedido"
    )

    def __repr__(self):
        return f"Pedido {self.id_pedido}"


# 6. DETALLES DE PEDIDOS
class DetallePedido(db.Model):
    __tablename__ = "detalle_pedidos"

    id_detalle = db.Column(db.Integer, primary_key=True)

    id_pedido = db.Column(
        db.Integer,
        db.ForeignKey("pedidos.id_pedido"),
        nullable=False
    )

    id_producto = db.Column(
        db.Integer,
        db.ForeignKey("productos.id_producto"),
        nullable=False
    )

    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(Numeric(10, 2), nullable=False)
    subtotal = db.Column(Numeric(10, 2), nullable=False)

    pedido = db.relationship(
        "Pedido",
        back_populates="detalles"
    )

    producto = db.relationship(
        "Producto",
        back_populates="detalles"
    )

    def __repr__(self):
        return f"Detalle {self.id_detalle}"
