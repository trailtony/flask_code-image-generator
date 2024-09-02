from flask import Flask, render_template
from typing import Final

app = Flask(__name__)

# PLACEHOLDER_CODE defined as a constant due to it's use throughout the project
PLACEHOLDER_CODE: [Final] = "print('Hello, World!')" 

@app.route("/", methods=["GET"])
def code():
    context = {
        "message": "Paste Your Python Code 🐍",
        "code": PLACEHOLDER_CODE
    }
    return render_template("code_input.html", **context)
