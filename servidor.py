#  PROGRAMACION SOBRE REDES
#  PRACTIFA FORMATIVA 2 
#  Alumno: Specterman Luis Omar
#  
#  Programa servidor.py 
#  PFO 2 - Sistema de Gestión de Tareas con API y Base de Datos
#  API REST con Flask + SQLite. Las contraseñas se guardan hasheadas.

import os
import sqlite3

from flask import Flask, jsonify, request, session
from markupsafe import escape
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
# En producción conviene definir SECRET_KEY como variable de entorno.
app.secret_key = os.environ.get("SECRET_KEY", "clave-de-desarrollo-cambiar")

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tareas.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL UNIQUE,
                contrasena_hash TEXT NOT NULL
            )
            """
        )


@app.route("/registro", methods=["POST"])
def registro():
    datos = request.get_json(silent=True) or {}
    usuario = (datos.get("usuario") or "").strip()
    contrasena = datos.get("contraseña") or ""

    if not usuario or not contrasena:
        return jsonify({"error": "Se requieren 'usuario' y 'contraseña'"}), 400

    # generate_password_hash aplica sal aleatoria + algoritmo de derivación (scrypt)
    hash_pw = generate_password_hash(contrasena)

    try:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO usuarios (usuario, contrasena_hash) VALUES (?, ?)",
                (usuario, hash_pw),
            )
    except sqlite3.IntegrityError:
        return jsonify({"error": "El usuario ya existe"}), 409

    return jsonify({"mensaje": f"Usuario '{usuario}' registrado correctamente"}), 201


@app.route("/login", methods=["POST"])
def login():
    datos = request.get_json(silent=True) or {}
    usuario = (datos.get("usuario") or "").strip()
    contrasena = datos.get("contraseña") or ""

    if not usuario or not contrasena:
        return jsonify({"error": "Se requieren 'usuario' y 'contraseña'"}), 400

    with get_db() as conn:
        fila = conn.execute(
            "SELECT contrasena_hash FROM usuarios WHERE usuario = ?", (usuario,)
        ).fetchone()

    if fila is None or not check_password_hash(fila["contrasena_hash"], contrasena):
        # Mismo mensaje en ambos casos para no revelar si el usuario existe
        return jsonify({"error": "Credenciales inválidas"}), 401

    session["usuario"] = usuario
    return jsonify({"mensaje": f"Bienvenido, {usuario}. Ya podés acceder a /tareas"}), 200


@app.route("/tareas", methods=["GET"])
def tareas():
    usuario = session.get("usuario")
    if not usuario:
        return jsonify({"error": "No autorizado. Iniciá sesión en /login"}), 401

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Gestión de Tareas</title>
</head>
<body>
    <h1>¡Bienvenido, {escape(usuario)}!</h1>
    <p>Este es tu Sistema de Gestión de Tareas.</p>
</body>
</html>"""
    return html, 200, {"Content-Type": "text/html; charset=utf-8"}


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=True)
