import os
from sqlalchemy import create_engine, text

db_url = "postgresql://education_db_v2q0_user:cQ3mQW1o2bYn4hI73K9r6rFvP1O7Q2p9@dpg-cqq3gdaj1k6c738t1df0-a-dg.frankfurt-postgres.render.com/education_db_v2q0?sslmode=require"
engine = create_engine(db_url)

try:
    with engine.connect() as conn:
        # Query institutes
        res_inst = conn.execute(text("SELECT id, name, slug, manager_phone FROM institutes")).fetchall()
        print("INSTITUTES IN DB:")
        for r in res_inst:
            print(f"ID: {r[0]} | Name: {r[1]} | Slug: {r[2]} | Manager Phone: {r[3]}")
            
        # Query institute admins
        res_admin = conn.execute(text("SELECT id, institute_id, name, email, phone, password_hash, is_active FROM institute_admins")).fetchall()
        print("\nADMINS IN DB:")
        for a in res_admin:
            is_bcrypt = a[5].startswith("$2b$") or a[5].startswith("$2a$")
            print(f"ID: {a[0]} | InstID: {a[1]} | Name: {a[2]} | Phone: {a[4]} | PasswordIsBcrypt: {is_bcrypt} | Active: {a[6]}")
except Exception as e:
    print(f"Error: {e}")
