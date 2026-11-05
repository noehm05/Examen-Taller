
import os

from flask import request, jsonify, render_template
from flask_login import login_required
from groq import Groq

from app import app, appbuilder


# ==========================================
# PAGINA DEL ASISTENTE JEHIELY AI
# ==========================================

@app.route("/asistente", methods=["GET"])
@login_required
def pagina_asistente():
    return render_template("asistente.html")


# ==========================================
# CONEXION CON GROQ
# ==========================================

@app.route("/api/asistente", methods=["POST"])
@login_required
def asistente_jehiely():

    try:
        datos = request.get_json(silent=True) or {}
        mensaje = datos.get("message", "").strip()

        if not mensaje:
            return jsonify({
                "error": "Escribe una pregunta para el asistente."
            }), 400

        api_key = os.getenv("GROQ_API_KEY")
        modelo = os.getenv(
            "GROQ_MODEL",
            "openai/gpt-oss-20b"
        )

        if not api_key:
            return jsonify({
                "error": "No se encontró la clave API de Groq."
            }), 500

        cliente = Groq(api_key=api_key)

        respuesta = cliente.chat.completions.create(
            model=modelo,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres JEHIELY AI, el asistente virtual de "
                        "una florería y regalería llamada JEHIELY. "
                        "Recomiendas flores, regalos, desayunos "
                        "sorpresa, chocolates y detalles personalizados. "
                        "Ayudas a elegir regalos según la ocasión y "
                        "el presupuesto. También creas dedicatorias "
                        "bonitas para tarjetas. Responde siempre en "
                        "español, con amabilidad y de forma clara. "
                        "No inventes precios ni disponibilidad."
                    )
                },
                {
                    "role": "user",
                    "content": mensaje
                }
            ]
        )

        texto_respuesta = respuesta.choices[0].message.content

        return jsonify({
            "response": texto_respuesta
        })

    except Exception:
        app.logger.exception("Error en el asistente JEHIELY")

        return jsonify({
            "error": "No se pudo obtener una respuesta de la IA. "
                     "Verifica la conexión y la configuración de Groq."
        }), 500


# ==========================================
# AGREGAR JEHIELY AI AL MENU PRINCIPAL
# ==========================================

appbuilder.add_link(
    "JEHIELY AI",
    href="/asistente",
    category="Asistente",
    icon="fa-comments"
)
