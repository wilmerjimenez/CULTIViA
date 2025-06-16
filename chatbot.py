import openai

openai.api_key = "TU_API_KEY"

print("🤖 CULTIViA AI Chatbot - Escribe tu consulta climática (Ctrl+C para salir)")

while True:
    try:
        pregunta = input("Tú: ")
        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": pregunta}]
        )
        print("CULTIViA:", respuesta.choices[0].message.content.strip())
    except KeyboardInterrupt:
        print("\nFinalizando el chatbot. ¡Hasta luego!")
        break
