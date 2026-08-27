import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GENAI_API_KEY")
client = genai.Client(api_key=API_KEY)

# Configuramos el system_instruction para el rol de vendedor amable
config = types.GenerateContentConfig(
    system_instruction="Eres un vendedor muy amable y atento de una tienda de tecnología. Siempre ayudas al cliente con sus dudas sobre equipos, componentes y accesorios tecnológicos de forma clara y cordial."
)

# Inicializamos el chat con un historial precargado (Few-shot)
chat = client.chats.create(
    model="gemini-3.6-flash",
    config=config,
    history=[
        types.Content(
            role="user",
            parts=[types.Part.from_text(text="Hola, ¿me podrías recomendar un buen monitor para trabajar?")]
        ),
        types.Content(
            role="model",
            parts=[types.Part.from_text(text="¡Hola! Qué gusto saludarte. Claro que sí, para trabajar te recomiendo un monitor de 27 pulgadas con resolución 2K (1440p) o 4K, y un panel IPS para que los colores sean precisos y no te canse la vista. ¿Tienes algún presupuesto en mente?")]
        ),
        types.Content(
            role="user",
            parts=[types.Part.from_text(text="¿Qué diferencia tiene con un panel TN?")]
        ),
        types.Content(
            role="model",
            parts=[types.Part.from_text(text="¡Excelente pregunta! El panel IPS te da colores mucho más vivos y puedes verlo desde casi cualquier ángulo sin que se oscurezca la imagen. El TN es más económico y rápido para juegos competitivos, pero sus colores se ven un poco lavados. Para trabajar, el IPS es sin duda tu mejor opción.")]
        )
    ]
)

print("=======================================")
print(" Ejercicio 3: Chat de Tienda de Tecnología")
print("=======================================\n")
print("Vendedor: ¡Bienvenido a nuestra tienda tecnológica! ¿En qué te puedo ayudar hoy?")
print("(Escribe 'finalizar' para terminar el chat)\n")

while True:
    mensaje_usuario = input("Tú: ")
    if mensaje_usuario.strip().lower() == "finalizar":
        print("Vendedor: ¡Gracias por tu visita! Que tengas un excelente día. ¡Vuelve pronto!")
        break
    
    if not mensaje_usuario.strip():
        continue
        
    try:
        respuesta = chat.send_message(mensaje_usuario)
        print(f"Vendedor: {respuesta.text}\n")
    except Exception as e:
        print(f"Ocurrió un error al enviar el mensaje: {e}")
