import sys
import os

# Add current directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
sys.stdout.reconfigure(encoding='utf-8')

from app.db.session import SessionLocal
from app.models.tables import Institute

db = SessionLocal()
try:
    institutes = db.query(Institute).all()
    print("--- INSTITUTES IN DATABASE ---")
    for inst in institutes:
        print(f"ID: {inst.id}")
        print(f"Name: {inst.name}")
        print(f"Slug: {inst.slug}")
        print(f"Logo URL: {inst.logo_url}")
        print("-" * 30)
finally:
    db.close()
