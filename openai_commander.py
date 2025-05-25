# openai_commander.py – conexión con Luciano AI (GPT)
def ask_ai(prompt):
    print(f"🤖 Asking LucianoAI: {prompt}")
    return {"action": "crear_archivo", "filename": "eth_bot.py", "content": "print('ETH bot listo')"}
