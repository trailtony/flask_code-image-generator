import base64
from flask import Flask, redirect, render_template, request, session, url_for
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import Python3Lexer
from pygments.styles import get_all_styles
from typing import Dict, Text

from utils import take_screenshot_from_url
from session_auth.generate_app_secret_key import create_flask_secret_key


app = Flask(__name__)
app.secret_key = create_flask_secret_key()
# app.config["TESTING"] = True

# PLACEHOLDER_CODE defined as a constant due to it's use throughout the project
PLACEHOLDER_CODE = "print('Hello, World!')"
# Starting Pygments style name
DEFAULT_STYLE = "default"


@app.route("/", methods=["GET"])
def code() -> Text:
    if session.get("code") is None:
        session["code"] = PLACEHOLDER_CODE
    lines = session["code"].split("\n")
    context: Dict = {
        "message": "Paste Your Python Code 🐍",
        "code": session["code"],
        "num_lines": len(lines),
        "max_chars": len(max(lines, key=len)),
    }
    return render_template("code_input.html", **context)


# View to reset a user’s session
@app.route("/save_code", methods=["POST"])
def save_code():
    session["code"] = request.form.get("code")
    return redirect(url_for("code"))


# View to save a user’s custom code in session
@app.route("/reset_session", methods=["POST"])
def reset_session():
    session.clear()
    session["code"] = PLACEHOLDER_CODE
    return redirect(url_for("code"))


# View to set Pygments definitions and render a template that shows the highlighted code
@app.route("/style", methods=["GET"])
def style() -> Text:
    if session.get("style") is None:
        session["style"] = DEFAULT_STYLE
    formatter = HtmlFormatter(style=session["style"])
    context: Dict = {
        "message": "Select Your Style 🎨",
        "all_styles": list(get_all_styles()),
        "style_definitions": formatter.get_style_defs(),
        "style_bg_color": formatter.style.background_color,
        "highlighted_code": highlight(session["code"], Python3Lexer(), formatter),
    }
    return render_template("style_selection.html", **context)


# View that receives the "style" value from the posted form of style_selection.html
@app.route("/save_style", methods=["POST"])
def save_style():
    if request.form.get("style") is not None:
        session["style"] = request.form.get("style")
    if request.form.get("code") is not None:
        session["code"] = request.form.get("code")
    return redirect(url_for("style"))


# View to load and populate image.html with a success message
@app.route("/image", methods=["GET"])
def image():
    session_data: Dict = {
        "name": app.config["SESSION_COOKIE_NAME"],
        "value": request.cookies.get(app.config["SESSION_COOKIE_NAME"]),
        "url": request.host_url,
    }

    target_url = request.host_url + url_for("style")
    image_bytes = take_screenshot_from_url(target_url, session_data)

    context: Dict = {
        "message": "Done! 🎉",
        # Base64-encode the binary image data and convert it to a Base64 string
        "image_b64": base64.b64encode(image_bytes).decode("utf-8"),
    }
    return render_template("image.html", **context)
