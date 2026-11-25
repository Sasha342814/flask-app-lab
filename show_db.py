"""Показує схему таблиць і дані - зручно для скрінів у звіт.

python show_db.py
"""
import os
import sqlite3

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "instance", "data.sqlite")

con = sqlite3.connect(DB)
cur = con.cursor()

print("=" * 70)
print("СХЕМА ТАБЛИЦЬ")
print("=" * 70)
for name, sql in cur.execute(
    "SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
).fetchall():
    print(f"\n-- {name}\n{sql}")

for table in ("categories", "products", "alembic_version"):
    print("\n" + "=" * 70)
    print(f"ДАНІ: {table}")
    print("=" * 70)
    cur.execute(f"SELECT * FROM {table}")
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    widths = [max(len(str(x)) for x in [c] + [r[i] for r in rows]) for i, c in enumerate(cols)]
    print(" | ".join(c.ljust(w) for c, w in zip(cols, widths)))
    print("-+-".join("-" * w for w in widths))
    for r in rows:
        print(" | ".join(str(v).ljust(w) for v, w in zip(r, widths)))

con.close()
