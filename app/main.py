from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.routers import auth, institutes, courses, bookings, students, banners, admin_requests, languages, notifications
from app.db.session import Base, engine

app = FastAPI(
    title="Multi-Tenant Educational Platform API",
    description="API for managing students, courses, institutes, and payments.",
    version="1.0.0"
)

# Enable CORS for Flutter Mobile & Desktop apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directory for uploaded images
os.makedirs("app/static", exist_ok=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(institutes.router, prefix="/api/institutes", tags=["Institutes"])
app.include_router(courses.router, prefix="/api/courses", tags=["Courses"])
app.include_router(bookings.router, prefix="/api/bookings", tags=["Bookings"])
app.include_router(students.router, prefix="/api/students", tags=["Students"])
app.include_router(banners.router, prefix="/api/banners", tags=["Banners"])
app.include_router(admin_requests.router, prefix="/api/admin-requests", tags=["Admin Requests"])
app.include_router(languages.router, prefix="/api/languages", tags=["Languages"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["Notifications"])

@app.on_event("startup")
def startup_migration():
    from app.db.session import engine, SessionLocal
    from sqlalchemy import text, inspect
    
    # 1. Check if the new 'users' table exists and has data. If not, seed cleanly
    inspector = inspect(engine)
    db = SessionLocal()
    users_empty = True
    try:
        tables = inspector.get_table_names()
        if "users" in tables:
            from app.models.tables import User
            users_empty = (db.query(User).count() == 0)
    except Exception as e:
        print(f"Error checking users count: {e}")
    finally:
        db.close()
        
    if "users" not in inspector.get_table_names() or users_empty:
        print("Forcing database re-initialization to fix schema drift...")
        print("New database structure ('users' table) not found or table is empty. Reinitializing schema...")
        try:
            db_type = engine.name
            # Drop all existing tables safely using SQLAlchemy metadata (avoids schema permission issues)
            Base.metadata.drop_all(bind=engine)
            print("Successfully dropped all existing tables.")
            
            # Create all tables
            Base.metadata.create_all(bind=engine)
            print("Tables created successfully.")
            
            # Run the seeding script
            from init_db import seed_data
            seed_data()
            print("Database seeded successfully on startup.")
        except Exception as init_err:
            print(f"Error during automatic database initialization: {init_err}")
    else:
        # Create newly added tables if they don't exist (normal fallback)
        Base.metadata.create_all(bind=engine)
    
    try:
        with engine.begin() as conn:
            db_type = engine.name
            if db_type == "sqlite":
                result = conn.execute(text("PRAGMA table_info(courses);")).fetchall()
                cols = [r[1] for r in result]
                if "class_time" not in cols:
                    conn.execute(text("ALTER TABLE courses ADD COLUMN class_time VARCHAR(100) DEFAULT '08:00 - 10:00';"))
                if "category_name" not in cols:
                    conn.execute(text("ALTER TABLE courses ADD COLUMN category_name VARCHAR(100);"))
                if "period" not in cols:
                    conn.execute(text("ALTER TABLE courses ADD COLUMN period VARCHAR(50);"))
                result_banners = conn.execute(text("PRAGMA table_info(banners);")).fetchall()
                banners_cols = [r[1] for r in result_banners]
                if "is_active" not in banners_cols:
                    conn.execute(text("ALTER TABLE banners ADD COLUMN is_active BOOLEAN DEFAULT 1;"))
                
                # Check for fcm_token column in students & institute_admins
                student_cols = [r[1] for r in conn.execute(text("PRAGMA table_info(students);")).fetchall()]
                if "fcm_token" not in student_cols:
                    conn.execute(text("ALTER TABLE students ADD COLUMN fcm_token VARCHAR(255);"))
                admin_cols = [r[1] for r in conn.execute(text("PRAGMA table_info(institute_admins);")).fetchall()]
                if "fcm_token" not in admin_cols:
                    conn.execute(text("ALTER TABLE institute_admins ADD COLUMN fcm_token VARCHAR(255);"))
            else:
                # Run each alter statement in its own transaction context/block
                # so that a failure in one (e.g. invalid type cast) does not prevent the others from running.
                alter_statements = [
                    "ALTER TABLE courses ADD COLUMN IF NOT EXISTS class_time VARCHAR(100) DEFAULT '08:00 - 10:00';",
                    "ALTER TABLE courses ADD COLUMN IF NOT EXISTS category_name VARCHAR(100);",
                    "ALTER TABLE courses ADD COLUMN IF NOT EXISTS period VARCHAR(50);",
                    "ALTER TABLE students ADD COLUMN IF NOT EXISTS fcm_token VARCHAR(255);",
                    "ALTER TABLE institute_admins ADD COLUMN IF NOT EXISTS fcm_token VARCHAR(255);",
                    "ALTER TABLE banners ALTER COLUMN image_url TYPE TEXT;",
                    "ALTER TABLE banners ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;"
                ]
                for statement in alter_statements:
                    try:
                        # We use another connection context or execution to prevent outer block rollback
                        conn.execute(text(statement))
                    except Exception as err:
                        print(f"PostgreSQL migration warning for statement '{statement}': {err}")
            print("Database migration completed: verified column types.")
    except Exception as e:
        print(f"Database startup migration warning: {e}")

    # Self-healing password migration (hashes raw passwords on deploy)
    db = SessionLocal()
    try:
        from app.models.tables import SuperAdmin, InstituteAdmin
        from app.core.security import get_password_hash
        
        # 1. SuperAdmin
        super_admins = db.query(SuperAdmin).all()
        for sa in super_admins:
            if sa.password_hash and not (sa.password_hash.startswith("$2b$") or sa.password_hash.startswith("$2a$")):
                if sa.password_hash in ["hashed_password_for_super_admin", "superadmin"]:
                    sa.password_hash = get_password_hash("superadmin")
                else:
                    sa.password_hash = get_password_hash(sa.password_hash)
        
        # 2. InstituteAdmin
        inst_admins = db.query(InstituteAdmin).all()
        for ia in inst_admins:
            if ia.password_hash and not (ia.password_hash.startswith("$2b$") or ia.password_hash.startswith("$2a$")):
                if ia.password_hash == "1234":
                    ia.password_hash = get_password_hash("1234")
                else:
                    ia.password_hash = get_password_hash(ia.password_hash)
        db.commit()
        print("Database password encryption migration completed successfully.")
    except Exception as e:
        db.rollback()
        print(f"Password encryption migration warning: {e}")
    finally:
        db.close()

@app.get("/api/db-status")
def db_status():
    from app.db.session import engine, SessionLocal
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    db = SessionLocal()
    users_info = []
    institutes_info = []
    try:
        if "users" in tables:
            from app.models.tables import User, Role, UserRole
            users = db.query(User).all()
            for u in users:
                roles = db.query(Role).join(UserRole).filter(UserRole.user_id == u.id).all()
                role_names = [r.code for r in roles]
                users_info.append({
                    "email": u.email,
                    "phone": u.phone,
                    "status": u.status,
                    "roles": role_names
                })
        if "institutes" in tables:
            from app.models.tables import Institute
            insts = db.query(Institute).all()
            for i in insts:
                institutes_info.append({
                    "name": i.name,
                    "slug": i.slug,
                    "manager_phone": i.manager_phone,
                    "is_active": i.is_active
                })
    except Exception as e:
        users_info = f"Error: {e}"
    finally:
        db.close()
        
    return {
        "tables": tables,
        "users": users_info,
        "institutes": institutes_info,
        "database_type": engine.name
    }

@app.get("/")
def read_root():
    return {"message": "Welcome to the Educational Platform API"}
