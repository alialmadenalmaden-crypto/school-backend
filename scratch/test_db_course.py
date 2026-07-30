import os
from sqlalchemy import create_engine, text

db_url = "postgresql://education_db_v2q0_user:cQ3mQW1o2bYn4hI73K9r6rFvP1O7Q2p9@dpg-cqq3gdaj1k6c738t1df0-a-dg.frankfurt-postgres.render.com/education_db_v2q0?sslmode=require"
engine = create_engine(db_url)

try:
    with engine.connect() as conn:
        # Check if period column exists
        res = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='courses'")).fetchall()
        print("Columns in 'courses' table:")
        for r in res:
            print(r[0])
except Exception as e:
    print(f"Error: {e}")
