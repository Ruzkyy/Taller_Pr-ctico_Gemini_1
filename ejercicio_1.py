import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Instrucciones del sistema para validar el tema y restringir la extensión
configuracion = types.GenerateContentConfig(
    system_instruction="""Eres un asistente estricto. 
Tu única tarea es responder a la pregunta '¿Qué es la Inferencia en IA?' o consultas directamente sobre qué es la inferencia en inteligencia artificial.

Reglas obligatorias:
1. Si el usuario te pregunta cualquier otra cosa que NO sea sobre 'Inferencia en IA', responde exactamente: 'Lo siento, solo puedo responder sobre qué es la Inferencia en IA. Por favor, realiza esa consulta.'
2. Cuando te pregunten sobre la inferencia en IA, explícala en menos de 50 palabras de forma clara y educativa."""
)

print("--- Ejercicio 1: Conexión y Petición Básica ---")
pregunta_usuario = input("Ingrese su consulta: ").strip()

try:
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=pregunta_usuario,
        config=configuracion
    )
    
    print("\nRespuesta del modelo:")
    print(response.text)

except Exception as e:
    print(f"Ocurrió un error al procesar la solicitud: {e}")