
import openai
import os

def ask_luciano_ai(prompt):
    print(f"🤖 Preguntando a LucianoAI: {prompt}")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Actuás como el núcleo maestro de LucianoAI, operativo en producción. Respondé con instrucciones directas para crear o actualizar bots reales."},
            {"role": "user", "content": prompt}
        ]
    )
    result = response['choices'][0]['message']['content']
    print(f"🧠 LucianoAI respondió:
{result}")
    return result
