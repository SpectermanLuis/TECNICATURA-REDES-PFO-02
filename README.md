# PFO 2 – Sistema de Gestión de Tareas con API y Base de Datos

API REST hecha con **Flask** y **SQLite**. Los usuarios se registran con contraseña hasheada, inician sesión y acceden a una página de bienvenida en `/tareas`.

## Estructura

```
servidor.py        # API Flask + SQLite
cliente.py         # Cliente en consola (opcional)
requirements.txt
tareas.db          # se crea automáticamente al iniciar el servidor
```

## Cómo ejecutarlo

```bash
git clone <URL-DEL-REPOSITORIO>
cd <carpeta>
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python servidor.py
```

El servidor queda en `http://127.0.0.1:5000`.

## Endpoints

| Método | Ruta        | Descripción                                             |
|--------|-------------|---------------------------------------------------------|
| POST   | `/registro` | Crea un usuario. Body: `{"usuario": "...", "contraseña": "..."}` |
| POST   | `/login`    | Verifica credenciales e inicia sesión (cookie)          |
| GET    | `/tareas`   | HTML de bienvenida. Requiere haber iniciado sesión      |

## Cómo probarlo

**Con curl** (`-c`/`-b` guardan y envían la cookie de sesión):

```bash
curl -X POST http://127.0.0.1:5000/registro -H "Content-Type: application/json" \
     -d '{"usuario":"ana","contraseña":"1234"}'

curl -c cookies.txt -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" \
     -d '{"usuario":"ana","contraseña":"1234"}'

curl -b cookies.txt http://127.0.0.1:5000/tareas
```

**Con el cliente de consola:** en otra terminal, `python cliente.py`.

Casos esperados: registro `201`, usuario repetido `409`, login correcto `200`, login incorrecto `401`, `/tareas` sin sesión `401` y con sesión `200`.

## Capturas de pantalla

_(Agregar acá las capturas de las pruebas exitosas: registro, login, /tareas y la tabla en SQLite.)_

## Respuestas conceptuales

**¿Por qué hashear contraseñas?**
Porque si la base de datos se filtra o alguien con acceso la lee, las contraseñas en texto plano quedarían expuestas, y como mucha gente reutiliza la misma clave en varios sitios, el daño se extendería más allá de esta aplicación. Un hash es una transformación de un solo sentido: no se puede revertir para obtener la contraseña original. Al login se hashea lo que ingresa el usuario y se compara con el hash guardado. Además, las funciones modernas (scrypt, bcrypt, argon2) agregan una *sal* aleatoria, de modo que dos usuarios con la misma contraseña tienen hashes distintos, y son deliberadamente lentas para dificultar ataques de fuerza bruta.

**Ventajas de usar SQLite en este proyecto**
- No requiere instalar ni configurar un servidor de base de datos: es un único archivo (`tareas.db`).
- Viene incluida en Python (módulo `sqlite3`), sin dependencias extra.
- Persiste los datos entre reinicios del servidor, a diferencia de guardarlos en memoria.
- Es SQL estándar, con integridad (por ejemplo `UNIQUE` para evitar usuarios duplicados).
- Es liviana y portable, ideal para un proyecto académico o un prototipo.
