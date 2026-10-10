#  PROGRAMACION SOBRE REDES
#  PRACTIFA FORMATIVA 2 
#  Alumno: Specterman Luis Omar    Comision : E
#  
#  Programa cliente.py 
#  PFO 2 - Sistema de Gestión de Tareas con API y Base de Datos
#  API REST con Flask + SQLite. Las contraseñas se guardan hasheadas.
#  Cliente en consola para probar la API del PFO 2.


import requests

BASE = "http://127.0.0.1:5000"
s = requests.Session()  # conserva la cookie de sesión tras el login


def pedir_credenciales():
    return {"usuario": input("Usuario: ").strip(), "contraseña": input("Contraseña: ")}


def mostrar(r):
    print(f"[{r.status_code}]", r.text if "html" in r.headers.get("Content-Type", "") else r.json())


while True:
    print("\n1) Registrarse  2) Iniciar sesión  3) Ver /tareas  4) Salir")
    op = input("Opción: ").strip()
    try:
        if op == "1":
            mostrar(s.post(f"{BASE}/registro", json=pedir_credenciales()))
        elif op == "2":
            mostrar(s.post(f"{BASE}/login", json=pedir_credenciales()))
        elif op == "3":
            mostrar(s.get(f"{BASE}/tareas"))
        elif op == "4":
            break
    except requests.ConnectionError:
        print("No se pudo conectar. ¿Está corriendo servidor.py?")
