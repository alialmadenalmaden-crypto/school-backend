import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Production DATABASE_URL with external host ending in -dg
db_url = "postgresql://education_db_v2q0_user:cQ3mQW1o2bYn4hI73K9r6rFvP1O7Q2p9@dpg-cqq3gdaj1k6c738t1df0-a-dg.frankfurt-postgres.render.com/education_db_v2q0?sslmode=require"
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()
try:
    from sqlalchemy import text
    res = db.execute(text("SELECT slug, category, manager_phone FROM institutes")).fetchall()
    print("Production Institutes:")
    for row in res:
        print(f"Slug: {row[0]}")
        print(f"Category: {repr(row[1])}")
        print(f"Manager Phone: {row[2]}")
        print("-" * 30)
finally:
    db.close()
