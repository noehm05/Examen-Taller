
from datetime import datetime, timedelta

from flask import render_template, request
from flask_login import login_required
from sqlalchemy import func

from app import app, appbuilder, db
from app.models.modelos import Pedido, Producto, DetallePedido


# ==================================================
# REPORTE 1: VENTAS POR FECHAS
# ==================================================

@app.route("/reportes/ventas", methods=["GET"])
@login_required
def reporte_ventas():

    fecha_actual = datetime.now().date()
    primer_dia_mes = fecha_actual.replace(day=1)

    fecha_inicio = request.args.get(
        "fecha_inicio",
        primer_dia_mes.strftime("%Y-%m-%d")
    )

    fecha_fin = request.args.get(
        "fecha_fin",
        fecha_actual.strftime("%Y-%m-%d")
    )

    pedidos = []
    total_ventas = 0

    try:
        inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fin = datetime.strptime(fecha_fin, "%Y-%m-%d") + timedelta(days=1)

        if inicio >= fin:
            raise ValueError("Rango de fechas no válido")

        pedidos = (
            Pedido.query
            .filter(Pedido.fecha_pedido >= inicio)
            .filter(Pedido.fecha_pedido < fin)
            .order_by(Pedido.fecha_pedido.desc())
            .all()
        )

        total_ventas = sum(
            float(pedido.total or 0)
            for pedido in pedidos
        )

    except ValueError:
        pedidos = []
        total_ventas = 0

    return render_template(
        "reportes/ventas.html",
        pedidos=pedidos,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        total_ventas=total_ventas,
        appbuilder=appbuilder,
        base_template=appbuilder.base_template
    )


# ==================================================
# REPORTE 2: PRODUCTOS MAS VENDIDOS
# ==================================================

@app.route("/reportes/productos-mas-vendidos", methods=["GET"])
@login_required
def reporte_productos_mas_vendidos():

    fecha_actual = datetime.now().date()
    primer_dia_mes = fecha_actual.replace(day=1)

    fecha_inicio = request.args.get(
        "fecha_inicio",
        primer_dia_mes.strftime("%Y-%m-%d")
    )

    fecha_fin = request.args.get(
        "fecha_fin",
        fecha_actual.strftime("%Y-%m-%d")
    )

    productos = []
    total_unidades = 0

    try:
        inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fin = datetime.strptime(fecha_fin, "%Y-%m-%d") + timedelta(days=1)

        if inicio >= fin:
            raise ValueError("Rango de fechas no válido")

        productos = (
            db.session.query(
                Producto.nombre.label("nombre"),
                func.sum(DetallePedido.cantidad).label("unidades"),
                func.sum(DetallePedido.subtotal).label("total")
            )
            .join(
                DetallePedido,
                DetallePedido.id_producto == Producto.id_producto
            )
            .join(
                Pedido,
                Pedido.id_pedido == DetallePedido.id_pedido
            )
            .filter(Pedido.fecha_pedido >= inicio)
            .filter(Pedido.fecha_pedido < fin)
            .group_by(
                Producto.id_producto,
                Producto.nombre
            )
            .order_by(
                func.sum(DetallePedido.cantidad).desc()
            )
            .all()
        )

        total_unidades = sum(
            int(producto.unidades or 0)
            for producto in productos
        )

    except ValueError:
        productos = []
        total_unidades = 0

    return render_template(
        "reportes/productos_mas_vendidos.html",
        productos=productos,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        total_unidades=total_unidades,
        appbuilder=appbuilder,
        base_template=appbuilder.base_template
    )


# ==================================================
# REPORTE 3: INVENTARIO Y STOCK
# ==================================================

@app.route("/reportes/inventario", methods=["GET"])
@login_required
def reporte_inventario():

    filtro = request.args.get("filtro", "todos")

    consulta = Producto.query

    if filtro == "bajo":
        consulta = consulta.filter(
            Producto.stock <= Producto.stock_minimo
        )

    elif filtro == "normal":
        consulta = consulta.filter(
            Producto.stock > Producto.stock_minimo
        )

    productos = (
        consulta
        .order_by(Producto.nombre)
        .all()
    )

    productos_bajos = sum(
        1
        for producto in productos
        if producto.stock <= producto.stock_minimo
    )

    return render_template(
        "reportes/inventario.html",
        productos=productos,
        filtro=filtro,
        productos_bajos=productos_bajos,
        appbuilder=appbuilder,
        base_template=appbuilder.base_template
    )


# ==================================================
# AGREGAR LOS TRES REPORTES AL MENU
# ==================================================

appbuilder.add_link(
    "Ventas por fechas",
    href="/reportes/ventas",
    category="Reportes",
    icon="fa-chart-line"
)

appbuilder.add_link(
    "Productos más vendidos",
    href="/reportes/productos-mas-vendidos",
    category="Reportes",
    icon="fa-trophy"
)

appbuilder.add_link(
    "Inventario y stock",
    href="/reportes/inventario",
    category="Reportes",
    icon="fa-archive"
)
