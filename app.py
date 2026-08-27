import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from google import genai
from google.genai import types


load_dotenv()

API_KEY = os.getenv("GENAI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "No se encontró GENAI_API_KEY en el archivo .env. "
        "Crea una API key de Google AI Studio."
    )



app = Flask(__name__, static_folder="Static")
client = genai.Client(api_key=API_KEY)

configuration = types.GenerateContentConfig(
    max_output_tokens=2048,
    system_instruction="""
Eres un asistente conversacional especializado en videojuegos.
Responde en español de forma clara, útil y entretenida sobre cualquier tema
relacionado con videojuegos: historia, géneros, personajes, consolas, PC,
recomendaciones, estrategias, desarrollo, ventas y novedades.

Si la pregunta no está relacionada con videojuegos, responde exactamente:
Solo puedo responder preguntas sobre videojuegos.
""",
)

chat = client.chats.create(
    model="gemini-flash-lite-latest",
    config=configuration,
)

RESPUESTAS = {
    "hola": "¡Hola, gamer! ¿De qué videojuego quieres hablar hoy?",
    "adios": "¡Nos vemos en el próximo nivel!",
}


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/enviar")
def enviar():
    datos = request.get_json(silent=True) or {}
    mensaje = str(datos.get("mensaje", "")).strip()

    if not mensaje:
        return jsonify({"respuesta": "Escribe una pregunta sobre videojuegos."}), 400

    mensaje_normalizado = mensaje.lower()
    if mensaje_normalizado in RESPUESTAS:
        return jsonify({"respuesta": RESPUESTAS[mensaje_normalizado]})

    try:
        response = chat.send_message(mensaje)
        return jsonify({"respuesta": response.text})
    except Exception as error:
        error_text = str(error)
        if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
            respuesta = "Se alcanzó la cuota de Gemini. Espera un momento e inténtalo de nuevo."
        elif "404" in error_text or "NOT_FOUND" in error_text:
            respuesta = "El modelo configurado no está disponible para esta API key."
        elif "401" in error_text or "403" in error_text or "UNAUTHENTICATED" in error_text:
            respuesta = "La API key no es válida o no tiene permisos para usar Gemini."
        else:
            respuesta = "Gemini no pudo procesar la consulta. Revisa la terminal para ver el detalle."
        print(f"Error al procesar la solicitud: {error}")
        return jsonify({"respuesta": respuesta}), 502


if __name__ == "__main__":
    app.run(debug=True)
