import os
from sqlalchemy import create_engine, text

db_url = "postgresql://education_db_v2q0_user:cQ3mQW1o2bYn4hI73K9r6rFvP1O7Q2p9@dpg-cqq3gdaj1k6c738t1df0-a-dg.frankfurt-postgres.render.com/education_db_v2q0?sslmode=require"
engine = create_engine(db_url)

email = "alialmadenalmaden@gmail.com"

try:
    with engine.connect() as conn:
        res_stud = conn.execute(text("SELECT id, email, full_name FROM students WHERE email = :email"), {"email": email}).fetchall()
        print("STUDENTS FOUND:")
        for r in res_stud:
            print(r)
            
        res_user = conn.execute(text("SELECT id, email, first_name FROM users WHERE email = :email"), {"email": email}).fetchall()
        print("\nUSERS FOUND:")
        for u in res_user:
            print(u)
except Exception as e:
    print(f"Error: {e}")
