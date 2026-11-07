
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_appbuilder import AppBuilder
from sqlalchemy import func

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

from app.models import modelos
from app.models.modelos import Producto, Cliente, Pedido


@app.context_processor
def datos_dashboard():

    if request.path != "/":
        return {}

    total_productos = Producto.query.filter_by(estado=True).count()

    total_clientes = Cliente.query.count()

    total_pedidos = Pedido.query.count()

    valor_total_pedidos = (
        db.session.query(func.coalesce(func.sum(Pedido.total), 0)).scalar()
    )

    productos_stock_bajo = (
        Producto.query
        .filter(
            Producto.estado.is_(True),
            Producto.stock <= Producto.stock_minimo
        )
        .order_by(Producto.stock.asc())
        .limit(5)
        .all()
    )

    ultimos_pedidos = (
        Pedido.query
        .order_by(Pedido.fecha_pedido.desc())
        .limit(5)
        .all()
    )

    return {
        "total_productos": total_productos,
        "total_clientes": total_clientes,
        "total_pedidos": total_pedidos,
        "valor_total_pedidos": valor_total_pedidos,
        "productos_stock_bajo": productos_stock_bajo,
        "ultimos_pedidos": ultimos_pedidos
    }


with app.app_context():
    appbuilder = AppBuilder(app, db.session)

    from app.views import vistas
    from app.views import reportes
    from app.views import asistente
