import sqlite3 
from pathlib import Path 

BASE_DIR = Path(__file__).resolve().parent

connection = sqlite3.connect(BASE_DIR / "database.db")

with open(BASE_DIR / "schema.sql", encoding="utf-8") as file:
    connection.executescript(file.read())

connection.close()

print("Database created successfully!")