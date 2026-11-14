import os 
import sqlite3
import secrets

from flask import(
    Flask, render_template, request, 
    redirect, session, url_for, abort
)
from werkzeug.security import generate_password_hash, check_password_hash

import db


app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]

@app.context_processor
def inject_auth():
    if "user_id" in session:
        if "csrf_token" not in session:
            session["csrf_token"] = secrets.token_urlsafe(32)

    return {"csrf_token": session.get("csrf_token")}



@app.route("/")
def index():
    search = request.args.get("search", "").strip()

    connection = db.get_connection()

    try:
        if search:
            recipes = connection.execute(
                """SELECT id, user_id, title, ingredients, instructions
                   FROM recipes
                   WHERE title LIKE ?
                   ORDER BY id DESC""",
                ("%" + search + "%",)
            ).fetchall()
        else:
            recipes = connection.execute(
                """SELECT id, user_id, title, ingredients, instructions
                   FROM recipes
                   ORDER BY id DESC"""
            ).fetchall()
    finally:
        connection.close()

    return render_template(
        "index.html",
        recipes=recipes,
        search=search
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        token = secrets.token_urlsafe(32)
        session["csrf_token"] = token
        return render_template("register.html", csrf_token = token)

    token = request.form.get("csrf_token", "")
    expected_token = session.get("csrf_token","")

    if not expected_token or not secrets.compare_digest(token, expected_token):
        return "Virheellinen lomakepyyntö", 403


    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if not 3 <= len(username) <= 30:
        return "Käyttäjätunnuksen pituus pitää olla 3-30 merkkiä", 400
    
    if not 8 <= len(password) <= 128:
        return "Salasanan pituus pitää olla 8-128 merkkiä", 400

    password_hash = generate_password_hash(password)

    connection = db.get_connection()

    try: 
        connection.execute(
            """INSERT INTO users (username, password_hash)
               values (?, ?)""", 
               (username, password_hash)
        )
        connection.commit()
    except sqlite3.IntegrityError:
        return "Käyttäjätunnus on jo käytössä" , 400
    finally:
        connection.close()
    
    session.pop("csrf_token", None)
    return redirect(url_for("index"))



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        token = secrets.token_urlsafe(32)
        session["csrf_token"] = token
        return render_template("login.html", csrf_token=token)

    token = request.form.get("csrf_token", "")
    expected_token = session.get("csrf_token", "")

    if not expected_token or not secrets.compare_digest(
        token, expected_token
    ):
        return "Virheellinen lomakepyyntö", 403

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    connection = db.get_connection()
    user = connection.execute(
        "SELECT id, password_hash FROM users WHERE username = ?",
        (username,)
    ).fetchone()
    connection.close()

    if user is None or not check_password_hash(
        user["password_hash"], password
    ):
        return "Virheellinen käyttäjätunnus tai salasana", 401

    session.clear()
    session["user_id"] = user["id"]

    return redirect(url_for("index"))



@app.route("/logout", methods=["POST"])
def logout():
    token = request.form.get("csrf_token", "")
    expected_token = session.get("csrf_token", "")

    if not expected_token or not secrets.compare_digest(
        token, expected_token
    ):
        return "Virheellinen lomakepyyntö", 403

    session.clear()
    return redirect(url_for("index"))



@app.route("/recipes/new", methods=["GET", "POST"])
def create_recipe():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "GET":
        if "csrf_token" not in session:
            session["csrf_token"] = secrets.token_urlsafe(32)

        return render_template(
            "create_recipe.html",
            csrf_token=session["csrf_token"]
        )

    token = request.form.get("csrf_token", "")
    expected_token = session.get("csrf_token", "")

    if not expected_token or not secrets.compare_digest(
        token, expected_token
    ):
        return "Virheellinen lomakepyyntö", 403

    title = request.form.get("title", "").strip()
    ingredients = request.form.get("ingredients", "").strip()
    instructions = request.form.get("instructions", "").strip()

    if not title or len(title) > 100:
        return "Reseptin nimen pituus ei kelpaa", 400

    if not ingredients or len(ingredients) > 5000:
        return "Ainesosien pituus ei kelpaa", 400

    if not instructions or len(instructions) > 10000:
        return "Valmistusohjeen pituus ei kelpaa", 400

    connection = db.get_connection()

    try:
        connection.execute(
            """INSERT INTO recipes
               (user_id, title, ingredients, instructions)
               VALUES (?, ?, ?, ?)""",
            (
                session["user_id"],
                title,
                ingredients,
                instructions
            )
        )
        connection.commit()
    finally:
        connection.close()

    return redirect(url_for("index"))



@app.route("/recipes/<int:recipe_id>/edit", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = db.get_connection()

    try:
        recipe = connection.execute(
            """SELECT id, user_id, title, ingredients, instructions
               FROM recipes WHERE id = ?""",
            (recipe_id,)
        ).fetchone()

        if recipe is None:
            abort(404)

        if recipe["user_id"] != session["user_id"]:
            abort(403)

        if request.method == "GET":
            if "csrf_token" not in session:
                session["csrf_token"] = secrets.token_urlsafe(32)

            return render_template(
                "edit_recipe.html",
                recipe=recipe,
                csrf_token=session["csrf_token"]
            )

        token = request.form.get("csrf_token", "")
        expected_token = session.get("csrf_token", "")

        if not expected_token or not secrets.compare_digest(
            token, expected_token
        ):
            abort(403)

        title = request.form.get("title", "").strip()
        ingredients = request.form.get("ingredients", "").strip()
        instructions = request.form.get("instructions", "").strip()

        if not title or len(title) > 100:
            return "Reseptin nimi ei kelpaa", 400

        if not ingredients or len(ingredients) > 5000:
            return "Ainekset eivät kelpaa", 400

        if not instructions or len(instructions) > 10000:
            return "Valmistusohje ei kelpaa", 400

        connection.execute(
            """UPDATE recipes
               SET title = ?, ingredients = ?, instructions = ?
               WHERE id = ? AND user_id = ?""",
            (
                title,
                ingredients,
                instructions,
                recipe_id,
                session["user_id"]
            )
        )
        connection.commit()

    finally:
        connection.close()

    return redirect(url_for("index"))




@app.route("/recipes/<int:recipe_id>/delete", methods=["POST"])
def delete_recipe(recipe_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    token = request.form.get("csrf_token", "")
    expected_token = session.get("csrf_token", "")

    if not expected_token or not secrets.compare_digest(
        token, expected_token
    ):
        abort(403)

    connection = db.get_connection()

    try:
        recipe = connection.execute(
            "SELECT user_id FROM recipes WHERE id = ?",
            (recipe_id,)
        ).fetchone()

        if recipe is None:
            abort(404)

        if recipe["user_id"] != session["user_id"]:
            abort(403)

        connection.execute(
            "DELETE FROM recipes WHERE id = ? AND user_id = ?",
            (recipe_id, session["user_id"])
        )
        connection.commit()

    finally:
        connection.close()

    return redirect(url_for("index"))
