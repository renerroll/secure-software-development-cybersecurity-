# app.py
# Простий веб-додаток на Flask для демонстрації
# Включена потенційна вразливість для перевірки SAST
import os
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/execute")
def execute_code():
    """
    Ця функція є навмисною вразливістю.
    Вона виконує код, переданий як параметр 'code' в URL.
    SAST сканер повинен виявити це.
    """
    code = request.args.get('code')
    if code:
        # Увага: Не використовуйте eval() у реальних додатках!
        # Це є серйозною загрозою безпеки.
        try:
            import ast
            result = ast.literal_eval(code)
            return f"<p>Result of execution: {result}</p>"
        except (ValueError, SyntaxError):
            return "Error: Invalid input. Only literal values allowed."
    return "<p>No code to execute.</p>"

if __name__ == '__main__':
    # Додано для перевірки DAST
    app.run(host='0.0.0.0', port=5000)
