import os
from sqlalchemy import create_engine, text

db_url = "postgresql://education_db_v2q0_user:cQ3mQW1o2bYn4hI73K9r6rFvP1O7Q2p9@dpg-cqq3gdaj1k6c738t1df0-a-dg.frankfurt-postgres.render.com/education_db_v2q0?sslmode=require"
engine = create_engine(db_url)

delete_statements = [
    # Delete transaction tables first
    "TRUNCATE TABLE bookings CASCADE;",
    "TRUNCATE TABLE reviews CASCADE;",
    "TRUNCATE TABLE notifications CASCADE;",
    "TRUNCATE TABLE audit_logs CASCADE;",
    "TRUNCATE TABLE promotions CASCADE;",
    
    # Delete courses, programs, levels, etc.
    "TRUNCATE TABLE courses CASCADE;",
    "TRUNCATE TABLE course_programs CASCADE;",
    "TRUNCATE TABLE levels CASCADE;",
    "TRUNCATE TABLE curriculums CASCADE;",
    
    # Delete banners and requests
    "TRUNCATE TABLE banners CASCADE;",
    "TRUNCATE TABLE super_admin_requests CASCADE;",
    
    # Delete institutes, branches, admins, members
    "TRUNCATE TABLE institute_branches CASCADE;",
    "TRUNCATE TABLE institute_admins CASCADE;",
    "TRUNCATE TABLE institute_members CASCADE;",
    "TRUNCATE TABLE institutes CASCADE;",
    
    # Delete students
    "TRUNCATE TABLE students CASCADE;",
    
    # Delete non-admin users from users and user_roles
    "DELETE FROM user_roles WHERE user_id IN (SELECT id FROM users WHERE email != 'admin@msaar.app');",
    "DELETE FROM users WHERE email != 'admin@msaar.app';"
]

try:
    print("Connecting to production PostgreSQL to clean up dummy/mock data...")
    with engine.begin() as conn:
        for sql in delete_statements:
            print(f"Executing: {sql}")
            conn.execute(text(sql))
    print("Database cleaned up successfully! All dummy/mock data deleted.")
except Exception as e:
    print(f"Error during database cleanup: {e}")
