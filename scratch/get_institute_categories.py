from app.db.session import SessionLocal
from app.models.tables import Institute

db = SessionLocal()
try:
    insts = db.query(Institute).all()
    for inst in insts:
        print(f"Slug: {inst.slug}")
        print(f"Category Field: {repr(inst.category)}")
        print("-" * 30)
finally:
    db.close()
