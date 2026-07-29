import os
import sys
import psycopg2
from datetime import datetime, date
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the parent directory to Python path so we can import app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import Base, engine, DATABASE_URL
from app.models.tables import (
    SuperAdmin, Institute, InstituteAdmin, Category, Course, Student, Booking, Banner, 
    SuperAdminRequest, Language, User, Role, Permission, UserRole, Country, City, District, 
    InstituteBranch, InstituteMember, Media, CourseProgram, Level, Curriculum,
    Review, Promotion, Notification, AuditLog
)
from app.core.security import get_password_hash

def create_database_if_not_exists():
    try:
        print("Connecting to PostgreSQL server to check database...")
        # Connect to the default 'postgres' database
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'institutes_db';")
        exists = cursor.fetchone()
        
        if not exists:
            print("Database 'institutes_db' does not exist. Creating it...")
            cursor.execute("CREATE DATABASE institutes_db;")
            print("Database created successfully!")
        else:
            print("Database 'institutes_db' already exists.")
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Skipping database creation check (likely remote/cloud database): {e}")

def seed_data():
    print("Seeding database with default data...")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # =========================================================================
        # 1. SEED GEOGRAPHY
        # =========================================================================
        print("Seeding Geography...")
        yemen = db.query(Country).filter(Country.iso_code == "YE").first()
        if not yemen:
            yemen = Country(name_ar="اليمن", name_en="Yemen", iso_code="YE", phone_code="+967", status="active")
            db.add(yemen)
            db.commit()
            
        sanaa = db.query(City).filter(City.name_en == "Sanaa").first()
        if not sanaa:
            sanaa = City(country_id=yemen.id, name_ar="صنعاء", name_en="Sanaa", status="active")
            db.add(sanaa)
            db.commit()
            
        hadda = db.query(District).filter(District.name_ar == "حدة").first()
        if not hadda:
            hadda = District(city_id=sanaa.id, name_ar="حدة", name_en="Hadda", status="active")
            db.add(hadda)
        sabeen = db.query(District).filter(District.name_ar == "السبعين").first()
        if not sabeen:
            sabeen = District(city_id=sanaa.id, name_ar="السبعين", name_en="Al-Sabeen", status="active")
            db.add(sabeen)
        tahrir = db.query(District).filter(District.name_ar == "التحرير").first()
        if not tahrir:
            tahrir = District(city_id=sanaa.id, name_ar="التحرير", name_en="Al-Tahrir", status="active")
            db.add(tahrir)
        db.commit()

        # =========================================================================
        # 2. SEED ROLES & PERMISSIONS
        # =========================================================================
        print("Seeding Roles and Permissions...")
        roles_list = [
            {"code": "super_admin", "name_ar": "مشرف عام المنصة", "name_en": "Super Admin", "scope": "platform", "is_system": True},
            {"code": "platform_admin", "name_ar": "مدير المنصة", "name_en": "Platform Admin", "scope": "platform", "is_system": True},
            {"code": "institute_owner", "name_ar": "مالك المعهد", "name_en": "Institute Owner", "scope": "institute", "is_system": True},
            {"code": "institute_admin", "name_ar": "مدير المعهد", "name_en": "Institute Admin", "scope": "institute", "is_system": True},
            {"code": "institute_staff", "name_ar": "موظف المعهد", "name_en": "Institute Staff", "scope": "branch", "is_system": True},
            {"code": "student", "name_ar": "طالب", "name_en": "Student", "scope": "user", "is_system": True},
        ]
        
        roles_map = {}
        for r_data in roles_list:
            role = db.query(Role).filter(Role.code == r_data["code"]).first()
            if not role:
                role = Role(
                    name_ar=r_data["name_ar"],
                    name_en=r_data["name_en"],
                    code=r_data["code"],
                    scope=r_data["scope"],
                    is_system=r_data["is_system"]
                )
                db.add(role)
                db.commit()
            roles_map[r_data["code"]] = role

        # =========================================================================
        # 3. SEED USERS & USER ROLES
        # =========================================================================
        print("Seeding default Users...")
        # Super Admin User
        admin_user = db.query(User).filter(User.phone == "+967777777777").first()
        if not admin_user:
            admin_user = User(
                first_name="المشرف",
                last_name="العام",
                email="admin@msaar.com",
                phone="+967777777777",
                password_hash=get_password_hash("admin123"),
                gender="male",
                status="active",
                phone_verified_at=datetime.utcnow()
            )
            db.add(admin_user)
            db.commit()
            
            # Assign Super Admin role
            ur = UserRole(user_id=admin_user.id, role_id=roles_map["super_admin"].id)
            db.add(ur)
            db.commit()

        # Institute Owner User
        owner_user = db.query(User).filter(User.phone == "+967776225879").first()
        if not owner_user:
            owner_user = User(
                first_name="علي عبدالرحمن",
                last_name="المعدن",
                email="msaar.student@gmail.com",
                phone="+967776225879",
                password_hash=get_password_hash("owner123"),
                gender="male",
                status="active",
                phone_verified_at=datetime.utcnow()
            )
            db.add(owner_user)
            db.commit()
            
            # Assign Institute Owner role
            ur = UserRole(user_id=owner_user.id, role_id=roles_map["institute_owner"].id)
            db.add(ur)
            db.commit()

        # =========================================================================
        # 4. SEED CATEGORIES (MVP Compatibility)
        # =========================================================================
        print("Seeding Categories...")
        if db.query(Category).count() == 0:
            lang_cat = Category(name_ar="اللغات", name_en="Languages", icon="language")
            comp_cat = Category(name_ar="الحاسوب", name_en="Computer Science", icon="computer")
            tut_cat = Category(name_ar="التقوية الدراسي", name_en="School Tutoring", icon="school")
            db.add_all([lang_cat, comp_cat, tut_cat])
            db.commit()
            print("Categories seeded.")
        else:
            lang_cat = db.query(Category).filter(Category.name_en == "Languages").first()
            comp_cat = db.query(Category).filter(Category.name_en == "Computer Science").first()
            tut_cat = db.query(Category).filter(Category.name_en == "School Tutoring").first()

        # =========================================================================
        # 5. SEED INSTITUTES & BRANCHES
        # =========================================================================
        print("Seeding Institutes & Branches...")
        if db.query(Institute).count() == 0:
            yali = Institute(
                owner_user_id=owner_user.id,
                name="معهد يالي (إنجليزي)",
                slug="yali",
                logo_url="https://api.dicebear.com/7.x/initials/svg?seed=yali",
                location="صنعاء - شارع بغداد",
                manager_phone="777111222",
                jeep_number="123456789",
                category="اللغات",
                is_active=True,
                status="active",
                verification_status="verified"
            )
            fly = Institute(
                owner_user_id=owner_user.id,
                name="معهد فلاي (إنجليزي)",
                slug="fly",
                logo_url="https://api.dicebear.com/7.x/initials/svg?seed=fly",
                location="صنعاء - حدة",
                manager_phone="777333444",
                jeep_number="987654321",
                category="اللغات",
                is_active=True,
                status="active",
                verification_status="verified"
            )
            telecom = Institute(
                owner_user_id=owner_user.id,
                name="المعهد العام للاتصالات",
                slug="telecom",
                logo_url="https://api.dicebear.com/7.x/initials/svg?seed=telecom",
                location="صنعاء - الجراف",
                manager_phone="777555666",
                jeep_number="112233445",
                category="الحاسوب",
                is_active=True,
                status="active",
                verification_status="verified"
            )
            db.add_all([yali, fly, telecom])
            db.commit()
            
            # Create Branches for each
            b_yali = InstituteBranch(
                institute_id=yali.id,
                name_ar="الفرع الرئيسي - شارع بغداد",
                name_en="Main Branch - Baghdad St",
                phone="777111222",
                country_id=yemen.id,
                city_id=sanaa.id,
                district_id=tahrir.id,
                address_line="صنعاء - شارع بغداد خلف مستشفى يالي",
                is_main_branch=True,
                status="active"
            )
            b_fly = InstituteBranch(
                institute_id=fly.id,
                name_ar="الفرع الرئيسي - حدة",
                name_en="Main Branch - Hadda",
                phone="777333444",
                country_id=yemen.id,
                city_id=sanaa.id,
                district_id=hadda.id,
                address_line="صنعاء - حدة المدينة السياحية",
                is_main_branch=True,
                status="active"
            )
            b_telecom = InstituteBranch(
                institute_id=telecom.id,
                name_ar="الفرع الرئيسي - الجراف",
                name_en="Main Branch - Al-Jaraf",
                phone="777555666",
                country_id=yemen.id,
                city_id=sanaa.id,
                district_id=sabeen.id,
                address_line="صنعاء - الجراف المطار القديم",
                is_main_branch=True,
                status="active"
            )
            db.add_all([b_yali, b_fly, b_telecom])
            db.commit()
            print("Institutes and Branches seeded.")
        else:
            yali = db.query(Institute).filter(Institute.slug == "yali").first()
            fly = db.query(Institute).filter(Institute.slug == "fly").first()
            telecom = db.query(Institute).filter(Institute.slug == "telecom").first()

        # =========================================================================
        # 6. SEED INSTITUTE ADMINS (MVP Compatibility)
        # =========================================================================
        print("Seeding Institute Admins...")
        if db.query(InstituteAdmin).count() == 0:
            yali_admin = InstituteAdmin(
                institute_id=yali.id,
                name="مدير يالي",
                email="yali@msaar.com",
                password_hash=get_password_hash("yali123"),
                is_active=True
            )
            fly_admin = InstituteAdmin(
                institute_id=fly.id,
                name="مدير فلاي",
                email="fly@msaar.com",
                password_hash=get_password_hash("fly123"),
                is_active=True
            )
            telecom_admin = InstituteAdmin(
                institute_id=telecom.id,
                name="مدير الاتصالات",
                email="telecom@msaar.com",
                password_hash=get_password_hash("telecom123"),
                is_active=True
            )
            db.add_all([yali_admin, fly_admin, telecom_admin])
            db.commit()
            print("Institute Admins seeded.")

        # =========================================================================
        # 7. SEED COURSE CATALOG (Languages, Programs, Levels, Curriculums)
        # =========================================================================
        print("Seeding Course Catalog (Languages, Programs, Levels, Curriculums)...")
        # Languages
        lang_en = db.query(Language).filter(Language.code == "en").first()
        if not lang_en:
            lang_en = Language(name="اللغة الإنجليزية", code="en", is_active=True)
            db.add(lang_en)
        lang_de = db.query(Language).filter(Language.code == "de").first()
        if not lang_de:
            lang_de = Language(name="اللغة الألمانية", code="de", is_active=True)
            db.add(lang_de)
        lang_tr = db.query(Language).filter(Language.code == "tr").first()
        if not lang_tr:
            lang_tr = Language(name="اللغة التركية", code="tr", is_active=True)
            db.add(lang_tr)
        db.commit()

        # Programs
        prog_english = db.query(CourseProgram).filter(CourseProgram.slug == "general-english").first()
        if not prog_english:
            prog_english = CourseProgram(
                category_id=lang_cat.id,
                language_id=lang_en.id,
                name_ar="دبلوم اللغة الإنجليزية العامة",
                name_en="General English Diploma",
                slug="general-english",
                program_type="language",
                status="active"
            )
            db.add(prog_english)
            
        prog_conv = db.query(CourseProgram).filter(CourseProgram.slug == "english-conversation").first()
        if not prog_conv:
            prog_conv = CourseProgram(
                category_id=lang_cat.id,
                language_id=lang_en.id,
                name_ar="محادثة إنجليزية مكثفة",
                name_en="English Conversation Intensive",
                slug="english-conversation",
                program_type="language",
                status="active"
            )
            db.add(prog_conv)
            
        prog_prep = db.query(CourseProgram).filter(CourseProgram.slug == "toefl-ielts-prep").first()
        if not prog_prep:
            prog_prep = CourseProgram(
                category_id=lang_cat.id,
                language_id=lang_en.id,
                name_ar="تحضير توفل وأيلتس",
                name_en="TOEFL & IELTS Preparation",
                slug="toefl-ielts-prep",
                program_type="language",
                status="active"
            )
            db.add(prog_prep)
            
        prog_web = db.query(CourseProgram).filter(CourseProgram.slug == "web-dev").first()
        if not prog_web:
            prog_web = CourseProgram(
                category_id=comp_cat.id,
                name_ar="تطوير واجهات الويب الشامل",
                name_en="Front-End Web Development",
                slug="web-dev",
                program_type="computer",
                status="active"
            )
            db.add(prog_web)
        db.commit()

        # Levels
        lvl_1 = db.query(Level).filter(Level.program_id == prog_english.id, Level.level_order == 1).first()
        if not lvl_1:
            lvl_1 = Level(
                program_id=prog_english.id,
                name_ar="المستوى الأول",
                name_en="Level 1",
                code="L1",
                level_order=1,
                status="active"
            )
            db.add(lvl_1)
        lvl_2 = db.query(Level).filter(Level.program_id == prog_english.id, Level.level_order == 2).first()
        if not lvl_2:
            lvl_2 = Level(
                program_id=prog_english.id,
                name_ar="المستوى الثاني",
                name_en="Level 2",
                code="L2",
                level_order=2,
                status="active"
            )
            db.add(lvl_2)
        db.commit()

        # Curriculums
        curr_interchange = db.query(Curriculum).filter(Curriculum.name == "Interchange").first()
        if not curr_interchange:
            curr_interchange = Curriculum(
                name="Interchange",
                publisher="Cambridge University Press",
                edition="5th Edition",
                status="active"
            )
            db.add(curr_interchange)
        db.commit()

        # =========================================================================
        # 8. SEED COURSES (linked to catalog)
        # =========================================================================
        print("Seeding Courses...")
        if db.query(Course).count() == 0:
            c1 = Course(
                institute_id=yali.id,
                category_id=lang_cat.id,
                program_id=prog_english.id,
                level_id=lvl_1.id,
                curriculum_id=curr_interchange.id,
                language_id=lang_en.id,
                category_name="اللغات",
                title="دبلوم اللغة الإنجليزية - المستوى الأول (English Level 1)",
                description="دورة أساسية لتعلم قواعد النطق، الجرامر البسيط، والمفردات اليومية العامة بطرق تفاعلية رائعة.",
                instructor_name="د. محمد الحبيشي",
                price=35000.00,
                image_url="https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?q=80&w=600",
                is_published=True,
                seats_available=25,
                registration_deadline="2026-08-10",
                start_date="2026-08-15",
                end_date="2026-09-15",
                class_time="08:00 - 10:00 صباحاً"
            )
            c2 = Course(
                institute_id=yali.id,
                category_id=lang_cat.id,
                program_id=prog_conv.id,
                language_id=lang_en.id,
                category_name="اللغات",
                title="محادثة إنجليزية متقدمة (English Conversation)",
                description="دورة مكثفة تركز بشكل كامل على الاستماع والتحدث وطلاقة اللسان ومواجهة الجمهور بنطق صحيح وسليم.",
                instructor_name="أ. سوزان ويلسون",
                price=45000.00,
                image_url="https://images.unsplash.com/photo-1524178232363-1fb2b075b655?q=80&w=600",
                is_published=True,
                seats_available=15,
                registration_deadline="2026-08-12",
                start_date="2026-08-18",
                end_date="2026-09-18",
                class_time="04:00 - 06:00 مساءً"
            )
            c3 = Course(
                institute_id=fly.id,
                category_id=lang_cat.id,
                program_id=prog_prep.id,
                language_id=lang_en.id,
                category_name="اللغات",
                title="توفل وأيلتس التحضيرية (TOEFL & IELTS Prep)",
                description="أقوى برنامج تحضيري لاجتياز اختبارات اللغة الإنجليزية الدولية بكفاءة مع نماذج اختبارات حقيقية وتدريب مكثف.",
                instructor_name="د. أحمد الشامي",
                price=60000.00,
                image_url="https://images.unsplash.com/photo-1434030216411-0b793f4b4173?q=80&w=600",
                is_published=True,
                seats_available=20,
                registration_deadline="2026-08-05",
                start_date="2026-08-10",
                end_date="2026-10-10",
                class_time="06:00 - 08:00 مساءً"
            )
            c4 = Course(
                institute_id=telecom.id,
                category_id=comp_cat.id,
                program_id=prog_web.id,
                category_name="الحاسوب",
                title="تطوير واجهات الويب الشامل (Front-End Web Dev)",
                description="تعلم بناء وتصميم مواقع الويب المتجاوبة والحديثة باستخدام HTML5, CSS3, JavaScript, و React من الصفر.",
                instructor_name="أ. علي الرماح",
                price=55000.00,
                image_url="https://images.unsplash.com/photo-1517694712202-14dd9538aa97?q=80&w=600",
                is_published=True,
                seats_available=30,
                registration_deadline="2026-08-14",
                start_date="2026-08-20",
                end_date="2026-10-20",
                class_time="10:00 - 12:00 صباحاً"
            )
            db.add_all([c1, c2, c3, c4])
            db.commit()
            print("Courses seeded.")

        # =========================================================================
        # 8. SEED STUDENTS (MVP Compatibility)
        # =========================================================================
        print("Seeding Students...")
        if db.query(Student).count() == 0:
            s1 = Student(
                full_name="صالح أحمد صالح",
                email="saleh@test.com",
                phone="777888999",
                is_email_verified=True,
                is_active=True
            )
            s2 = Student(
                full_name="رانيا محمد يحيى",
                email="rania@test.com",
                phone="777000111",
                is_email_verified=True,
                is_active=True
            )
            db.add_all([s1, s2])
            db.commit()
            
            # Also seed them into the new User table to keep data in sync
            u_s1 = User(
                first_name="صالح",
                last_name="صالح",
                email="saleh@test.com",
                phone="+967777888999",
                password_hash=get_password_hash("student123"),
                status="active",
                phone_verified_at=datetime.utcnow()
            )
            u_s2 = User(
                first_name="رانيا",
                last_name="يحيى",
                email="rania@test.com",
                phone="+967777000111",
                password_hash=get_password_hash("student123"),
                status="active",
                phone_verified_at=datetime.utcnow()
            )
            db.add_all([u_s1, u_s2])
            db.commit()
            
            # Assign Student role
            ur1 = UserRole(user_id=u_s1.id, role_id=roles_map["student"].id)
            ur2 = UserRole(user_id=u_s2.id, role_id=roles_map["student"].id)
            db.add_all([ur1, ur2])
            db.commit()
            print("Students seeded.")
        else:
            s1 = db.query(Student).filter(Student.email == "saleh@test.com").first()
            s2 = db.query(Student).filter(Student.email == "rania@test.com").first()

        # =========================================================================
        # 9. SEED BOOKINGS (MVP Compatibility)
        # =========================================================================
        print("Seeding Bookings...")
        if db.query(Booking).count() == 0:
            yali_course = db.query(Course).filter(Course.title.like("%Level 1%")).first()
            telecom_course = db.query(Course).filter(Course.title.like("%Front-End%")).first()
            
            if yali_course and s1:
                b1 = Booking(
                    student_id=s1.id,
                    course_id=yali_course.id,
                    registration_type="personal",
                    seats=1,
                    student_name=s1.full_name,
                    student_phone=s1.phone,
                    payment_method="electronic",
                    payment_status="pending",
                    transaction_id="TXN99887766",
                    receipt_image_url="https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?w=400"
                )
                db.add(b1)
                
            if telecom_course and s2:
                b2 = Booking(
                    student_id=s2.id,
                    course_id=telecom_course.id,
                    registration_type="personal",
                    seats=1,
                    student_name=s2.full_name,
                    student_phone=s2.phone,
                    payment_method="cash",
                    payment_status="confirmed"
                )
                db.add(b2)
                
            db.commit()
            print("Bookings seeded.")

        # =========================================================================
        # 10. SEED SUPER ADMIN REQUESTS (MVP Compatibility)
        # =========================================================================
        print("Seeding Super Admin Requests...")
        if db.query(SuperAdminRequest).count() == 0:
            yali_inst = db.query(Institute).filter(Institute.slug == "yali").first()
            if yali_inst:
                req1 = SuperAdminRequest(
                    institute_id=yali_inst.id,
                    request_type="ad",
                    title="خصم 50% بمناسبة عيد الأضحى المبارك",
                    details="يرجى الموافقة على نشر هذا البانر الترويجي لجميع طلاب المنصة للإعلان عن خصم 50% على كافة دورات اللغات المبتدئة والمتقدمة.",
                    image_url="https://images.unsplash.com/photo-1546410531-bb4caa6b424d?q=80&w=800&auto=format&fit=crop",
                    status="pending"
                )
                req2 = SuperAdminRequest(
                    institute_id=yali_inst.id,
                    request_type="category",
                    title="الذكاء الاصطناعي وهندسة البيانات",
                    details="Artificial Intelligence & Data Engineering",
                    status="pending"
                )
                db.add_all([req1, req2])
                db.commit()
            print("Super Admin requests seeded.")

        # =========================================================================
        # 11. SEED BANNERS & LANGUAGES (MVP Compatibility)
        # =========================================================================
        print("Seeding Banners & Languages...")
        if db.query(Banner).count() == 0:
            b1 = Banner(
                title="تخفيضات الصيف الكبرى 40%",
                image_url="https://images.unsplash.com/photo-1546410531-bb4caa6b424d?q=80&w=800",
                category="discount",
                is_active=True
            )
            db.add(b1)
            db.commit()
            print("Banners seeded.")
            
        if db.query(Language).count() == 0:
            l1 = Language(name="اللغة الإنجليزية", code="en", is_active=True)
            l2 = Language(name="اللغة الألمانية", code="de", is_active=True)
            l3 = Language(name="اللغة التركية", code="tr", is_active=True)
            db.add_all([l1, l2, l3])
            db.commit()
            print("Languages seeded.")

        # =========================================================================
        # 12. SEED PROMOTIONS, REVIEWS & NOTIFICATIONS
        # =========================================================================
        print("Seeding Promotions, Reviews & Notifications...")
        if db.query(Promotion).count() == 0:
            p1 = Promotion(
                code="WELCOME10",
                discount_type="fixed",
                discount_value=1000.00,
                start_date=datetime.utcnow(),
                end_date=datetime(2027, 12, 31),
                status="active"
            )
            p2 = Promotion(
                code="MSAAR50",
                discount_type="percentage",
                discount_value=50.00,
                start_date=datetime.utcnow(),
                end_date=datetime(2027, 12, 31),
                status="active"
            )
            db.add_all([p1, p2])
            db.commit()
            print("Promotions seeded.")

        # Seed Review
        if db.query(Review).count() == 0:
            student_user = db.query(User).filter(User.email == "saleh@test.com").first()
            yali_inst = db.query(Institute).filter(Institute.slug == "yali").first()
            yali_course = db.query(Course).filter(Course.title.like("%Level 1%")).first()
            if student_user and yali_inst and yali_course:
                r1 = Review(
                    user_id=student_user.id,
                    course_id=yali_course.id,
                    institute_id=yali_inst.id,
                    rating=5,
                    comment="دورة ممتازة جداً والمدرس متعاون للغاية. أنصح بها الجميع!",
                    status="approved"
                )
                db.add(r1)
                db.commit()
                print("Reviews seeded.")

        # Seed Notification
        if db.query(Notification).count() == 0:
            student_user = db.query(User).filter(User.email == "saleh@test.com").first()
            if student_user:
                n1 = Notification(
                    user_id=student_user.id,
                    title="مرحباً بك في مسار!",
                    body="تم تسجيل حسابك وتفعيله بنجاح. تصفح الكورسات وابدأ رحلتك التعليمية الآن!",
                    notification_type="general",
                    is_read=False
                )
                db.add(n1)
                db.commit()
                print("Notifications seeded.")

        print("Database seeded successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error during seeding: {str(e)}")
    finally:
        db.close()

def main():
    try:
        # Create database if it doesn't exist
        create_database_if_not_exists()
        
        # Drop existing tables to apply schema modifications by cascading schema drop
        print("Dropping public schema to apply clean schema changes...")
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("DROP SCHEMA IF EXISTS public CASCADE;")
        cursor.execute("CREATE SCHEMA public;")
        cursor.close()
        conn.close()
        print("Public schema recreated and tables dropped successfully!")
        
        # Create tables
        print("Creating tables in PostgreSQL...")
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully!")
        
        # Seed database
        seed_data()
        
        print("\nInitialization finished successfully!")
        
    except Exception as e:
        print(f"\nFailed to initialize database: {str(e)}")

if __name__ == "__main__":
    main()
