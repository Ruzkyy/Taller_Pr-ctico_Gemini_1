import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GENAI_API_KEY")
client = genai.Client(api_key=API_KEY)

def procesar_articulo(texto, tarea):
    if tarea == "1":
        instruccion = "Realiza un resumen ejecutivo del siguiente texto."
    elif tarea == "2":
        instruccion = "Edita el siguiente texto para que suene formal y técnico."
    else:
        return "Opción no válida."

    config = types.GenerateContentConfig(
        system_instruction="Eres un Editor Editorial de prestigio, conocido por tu redacción impecable y capacidad de síntesis."
    )

    prompt = f"{instruccion}\n\nTexto a procesar:\n{texto}"

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            config=config,
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Error al conectar con la IA: {e}"

if __name__ == "__main__":
    print("=======================================")
    print(" Ejercicio 2: Procesador de Textos")
    print("=======================================\n")
    
    # Pedimos al usuario que ingrese el texto manualmente
    texto_usuario = input("Ingresa el texto que deseas procesar:\n> ")
    
    if not texto_usuario.strip():
        print("No ingresaste ningún texto. Saliendo...")
    else:
        print("\n¿Qué deseas hacer con este texto?")
        print("1. Resumir (Crear un resumen ejecutivo)")
        print("2. Profesionalizar (Hacer que suene formal y técnico)")
        opcion = input("\nElige una opción (1 o 2): ")

        if opcion in ["1", "2"]:
            print("\nProcesando el texto con la IA (espera unos segundos)...")
            resultado = procesar_articulo(texto_usuario, opcion)
            print("\n--- Resultado de la IA ---")
            print(resultado)
            print("--------------------------")
        else:
            print("Opción inválida. Saliendo...")
