from app.db.session import SessionLocal
from app.routers.auth import login_institute, InstituteLogin

db = SessionLocal()
try:
    print("Testing local login with YALI...")
    credentials = InstituteLogin(slug="yali", phone="777111222", password="yali123")
    res = login_institute(credentials, db)
    print("Success response:", res)
except Exception as e:
    import traceback
    print("Caught Exception:")
    traceback.print_exc()
finally:
    db.close()
