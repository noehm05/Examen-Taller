
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from wtforms.fields import DateTimeField

from app import appbuilder
from app.models.modelos import (
    Categoria,
    Proveedor,
    Producto,
    Cliente,
    Pedido,
    DetallePedido
)


# CRUD DE CATEGORIAS
class CategoriaView(ModelView):
    datamodel = SQLAInterface(Categoria)

    list_columns = ["id_categoria", "nombre", "descripcion", "estado"]
    search_columns = ["nombre"]


# CRUD DE PROVEEDORES
class ProveedorView(ModelView):
    datamodel = SQLAInterface(Proveedor)

    list_columns = ["id_proveedor", "nombre", "telefono", "correo", "estado"]
    search_columns = ["nombre", "telefono"]


# CRUD DE PRODUCTOS
class ProductoView(ModelView):
    datamodel = SQLAInterface(Producto)

    list_columns = [
        "id_producto",
        "nombre",
        "categoria",
        "proveedor",
        "precio",
        "stock",
        "estado"
    ]

    add_columns = [
        "nombre",
        "descripcion",
        "categoria",
        "proveedor",
        "precio",
        "stock",
        "stock_minimo",
        "imagen",
        "estado"
    ]

    edit_columns = add_columns
    search_columns = ["nombre"]


# CRUD DE CLIENTES
class ClienteView(ModelView):
    datamodel = SQLAInterface(Cliente)

    list_columns = [
        "id_cliente",
        "nombre",
        "telefono",
        "correo",
        "direccion"
    ]

    search_columns = ["nombre", "telefono"]


# CRUD DE PEDIDOS
class PedidoView(ModelView):
    datamodel = SQLAInterface(Pedido)

    list_columns = [
        "id_pedido",
        "cliente",
        "fecha_pedido",
        "fecha_entrega",
        "ocasion",
        "estado",
        "total"
    ]

    add_form_extra_fields = {
        "fecha_entrega": DateTimeField(
            "Fecha de entrega",
            format="%Y-%m-%d %H:%M:%S"
        )
    }

    edit_form_extra_fields = {
        "fecha_entrega": DateTimeField(
            "Fecha de entrega",
            format="%Y-%m-%d %H:%M:%S"
        )
    }

    add_columns = [
        "cliente",
        "fecha_entrega",
        "ocasion",
        "dedicatoria",
        "tipo_entrega",
        "direccion_entrega",
        "estado",
        "metodo_pago",
        "estado_pago",
        "total"
    ]

    edit_columns = add_columns


# CRUD DE DETALLES DE PEDIDOS
class DetallePedidoView(ModelView):
    datamodel = SQLAInterface(DetallePedido)

    list_columns = [
        "id_detalle",
        "pedido",
        "producto",
        "cantidad",
        "precio_unitario",
        "subtotal"
    ]

    add_columns = [
        "pedido",
        "producto",
        "cantidad",
        "precio_unitario",
        "subtotal"
    ]

    edit_columns = add_columns


# REGISTRAR LAS SEIS VISTAS

appbuilder.add_view(
    CategoriaView,
    "Categorias",
    category="Catalogo",
    icon="fa-tags"
)

appbuilder.add_view(
    ProveedorView,
    "Proveedores",
    category="Catalogo",
    icon="fa-truck"
)

appbuilder.add_view(
    ProductoView,
    "Productos",
    category="Catalogo",
    icon="fa-gift"
)

appbuilder.add_view(
    ClienteView,
    "Clientes",
    category="Ventas",
    icon="fa-users"
)

appbuilder.add_view(
    PedidoView,
    "Pedidos",
    category="Ventas",
    icon="fa-shopping-bag"
)

appbuilder.add_view(
    DetallePedidoView,
    "Detalles de pedidos",
    category="Ventas",
    icon="fa-list"
)
