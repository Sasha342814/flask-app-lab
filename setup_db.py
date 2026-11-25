"""Створює міграцію та базу (flask db init / migrate / upgrade).

python setup_db.py
"""
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
ENV = dict(os.environ, FLASK_APP="run.py")


def flask(*args):
    print("\n> flask", " ".join(args))
    r = subprocess.run([sys.executable, "-m", "flask", *args], cwd=ROOT, env=ENV)
    if r.returncode != 0:
        sys.exit(f"Помилка ({r.returncode})")


shutil.rmtree(os.path.join(ROOT, "migrations"), ignore_errors=True)
db_file = os.path.join(ROOT, "instance", "data.sqlite")
if os.path.exists(db_file):
    os.remove(db_file)

flask("db", "init")
flask("db", "migrate", "-m", "Add User")
flask("db", "upgrade")
flask("db", "history")
print("\nГОТОВО: python run.py")
