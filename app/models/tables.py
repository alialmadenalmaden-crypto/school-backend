import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer, Numeric, Text, Date, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.session import Base

# =========================================================================
# ASSOCIATION TABLES (جداول الربط)
# =========================================================================

# الربط بين الأدوار والصلاحيات
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", UUID(as_uuid=True), ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime, default=datetime.utcnow)
)

# =========================================================================
# 1. AUTHENTICATION & USERS (المصادقة والمستخدمين)
# =========================================================================

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=True)
    email = Column(String(255), unique=True, nullable=True, index=True)
    phone = Column(String(30), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    profile_image_id = Column(UUID(as_uuid=True), ForeignKey("media.id", ondelete="SET NULL", use_alter=True, name="fk_user_profile_image"), nullable=True)
    gender = Column(String(20), nullable=True) # male, female, other
    birth_date = Column(Date, nullable=True)
    status = Column(String(30), nullable=False, default="pending_verification") # active, inactive, blocked, suspended
    preferred_language = Column(String(10), nullable=False, default="ar")
    phone_verified_at = Column(DateTime, nullable=True)
    email_verified_at = Column(DateTime, nullable=True)
    last_login_at = Column(DateTime, nullable=True)
    last_login_ip = Column(String(45), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    
    # Relationships
    user_roles = relationship("UserRole", back_populates="user", cascade="all, delete-orphan", foreign_keys="[UserRole.user_id]")
    memberships = relationship("InstituteMember", back_populates="user", cascade="all, delete-orphan", foreign_keys="[InstituteMember.user_id]")
    uploaded_media = relationship("Media", back_populates="uploader", foreign_keys="[Media.uploaded_by]")

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name_ar = Column(String(100), nullable=False)
    name_en = Column(String(100), nullable=True)
    code = Column(String(100), unique=True, nullable=False, index=True) # super_admin, institute_admin, student, etc.
    description = Column(Text, nullable=True)
    scope = Column(String(30), nullable=False, default="platform") # platform, institute, branch, user
    is_system = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")
    user_roles = relationship("UserRole", back_populates="role", cascade="all, delete-orphan")
    memberships = relationship("InstituteMember", back_populates="role", cascade="all, delete-orphan")

class Permission(Base):
    __tablename__ = "permissions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name_ar = Column(String(150), nullable=False)
    name_en = Column(String(150), nullable=True)
    code = Column(String(150), unique=True, nullable=False, index=True) # institutes.create, courses.publish, etc.
    module = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")

class UserRole(Base):
    __tablename__ = "user_roles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    institute_id = Column(UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=True)
    branch_id = Column(UUID(as_uuid=True), ForeignKey("institute_branches.id", ondelete="CASCADE"), nullable=True)
    assigned_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="user_roles", foreign_keys=[user_id])
    role = relationship("Role", back_populates="user_roles")
    institute = relationship("Institute", back_populates="user_roles")
    branch = relationship("InstituteBranch", back_populates="user_roles")

# =========================================================================
# 2. GEOGRAPHY (المواقع الجغرافية)
# =========================================================================

class Country(Base):
    __tablename__ = "countries"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name_ar = Column(String(100), nullable=False)
    name_en = Column(String(100), nullable=True)
    iso_code = Column(String(2), unique=True, nullable=False)
    phone_code = Column(String(10), nullable=True)
    status = Column(String(20), nullable=False, default="active")
    
    cities = relationship("City", back_populates="country", cascade="all, delete-orphan")

class City(Base):
    __tablename__ = "cities"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    country_id = Column(UUID(as_uuid=True), ForeignKey("countries.id", ondelete="CASCADE"), nullable=False)
    name_ar = Column(String(120), nullable=False)
    name_en = Column(String(120), nullable=True)
    status = Column(String(20), nullable=False, default="active")
    
    country = relationship("Country", back_populates="cities")
    districts = relationship("District", back_populates="city", cascade="all, delete-orphan")

class District(Base):
    __tablename__ = "districts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    city_id = Column(UUID(as_uuid=True), ForeignKey("cities.id", ondelete="CASCADE"), nullable=False)
    name_ar = Column(String(120), nullable=False)
    name_en = Column(String(120), nullable=True)
    status = Column(String(20), nullable=False, default="active")
    
    city = relationship("City", back_populates="districts")

# =========================================================================
# 3. MEDIA (الملفات والوسائط المرفوعة)
# =========================================================================

class Media(Base):
    __tablename__ = "media"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    file_name = Column(String(255), nullable=False)
    original_name = Column(String(255), nullable=False)
    mime_type = Column(String(150), nullable=False)
    file_size = Column(Integer, nullable=False)
    storage_path = Column(String(600), nullable=False)
    public_url = Column(String(1000), nullable=True)
    media_type = Column(String(30), nullable=False, default="image") # image, document, logo, etc.
    status = Column(String(20), nullable=False, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    uploader = relationship("User", back_populates="uploaded_media", foreign_keys=[uploaded_by])

# =========================================================================
# 4. INSTITUTES & MEMBERS (المعاهد وأعضائها)
# =========================================================================

class Institute(Base):
    __tablename__ = "institutes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=True)
    name = Column(String(150), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description_ar = Column(Text, nullable=True)
    description_en = Column(Text, nullable=True)
    logo_url = Column(String(255), nullable=True) # Retained for backward compatibility
    logo_id = Column(UUID(as_uuid=True), ForeignKey("media.id", ondelete="SET NULL"), nullable=True)
    cover_image_id = Column(UUID(as_uuid=True), ForeignKey("media.id", ondelete="SET NULL"), nullable=True)
    location = Column(String(200), nullable=True) # Retained for backward compatibility
    manager_phone = Column(String(20), nullable=True) # Retained for backward compatibility
    jeep_number = Column(String(50), nullable=True) # Retained for backward compatibility
    category = Column(String(100), nullable=True) # Retained for backward compatibility
    is_active = Column(Boolean, default=True) # Retained for backward compatibility
    status = Column(String(30), nullable=False, default="draft") # draft, active, pending_review, suspended
    verification_status = Column(String(30), nullable=False, default="unverified") # unverified, verified, rejected
    publishing_policy = Column(String(30), nullable=False, default="manual_review") # manual_review, auto_publish
    rating_average = Column(Numeric(3, 2), default=0.00)
    ratings_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    
    # Relationships
    admins = relationship("InstituteAdmin", back_populates="institute", cascade="all, delete-orphan")
    courses = relationship("Course", back_populates="institute", cascade="all, delete-orphan")
    user_roles = relationship("UserRole", back_populates="institute", cascade="all, delete-orphan")
    members = relationship("InstituteMember", back_populates="institute", cascade="all, delete-orphan")
    branches = relationship("InstituteBranch", back_populates="institute", cascade="all, delete-orphan")

class InstituteMember(Base):
    __tablename__ = "institute_members"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id = Column(UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(30), nullable=False, default="invited") # invited, active, suspended
    invited_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    joined_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    institute = relationship("Institute", back_populates="members")
    user = relationship("User", back_populates="memberships", foreign_keys=[user_id])
    role = relationship("Role", back_populates="memberships")

class InstituteBranch(Base):
    __tablename__ = "institute_branches"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id = Column(UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False)
    name_ar = Column(String(200), nullable=False)
    name_en = Column(String(200), nullable=True)
    description_ar = Column(Text, nullable=True)
    description_en = Column(Text, nullable=True)
    phone = Column(String(30), nullable=True)
    whatsapp_number = Column(String(30), nullable=True)
    email = Column(String(255), nullable=True)
    country_id = Column(UUID(as_uuid=True), ForeignKey("countries.id", ondelete="RESTRICT"), nullable=True)
    city_id = Column(UUID(as_uuid=True), ForeignKey("cities.id", ondelete="RESTRICT"), nullable=True)
    district_id = Column(UUID(as_uuid=True), ForeignKey("districts.id", ondelete="RESTRICT"), nullable=True)
    address_line = Column(Text, nullable=True)
    latitude = Column(Numeric(10, 7), nullable=True)
    longitude = Column(Numeric(10, 7), nullable=True)
    is_main_branch = Column(Boolean, default=False)
    status = Column(String(30), nullable=False, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    
    # Relationships
    institute = relationship("Institute", back_populates="branches")
    user_roles = relationship("UserRole", back_populates="branch", cascade="all, delete-orphan")

# =========================================================================
# RETAINED MVP MODELS (للمحافظة على عمل التطبيق الحالي)
# =========================================================================

class SuperAdmin(Base):
    __tablename__ = "super_admins"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class InstituteAdmin(Base):
    __tablename__ = "institute_admins"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id = Column(UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    fcm_token = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    institute = relationship("Institute", back_populates="admins")

# =========================================================================
# ASSOCIATION TABLES (جداول الربط الإضافية)
# =========================================================================

# الربط بين البرامج التعليمية والمناهج
program_curriculums = Table(
    "program_curriculums",
    Base.metadata,
    Column("program_id", UUID(as_uuid=True), ForeignKey("course_programs.id", ondelete="CASCADE"), primary_key=True),
    Column("curriculum_id", UUID(as_uuid=True), ForeignKey("curriculums.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime, default=datetime.utcnow)
)

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name_ar = Column(String(100), nullable=False)
    name_en = Column(String(100), nullable=False)
    icon = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    courses = relationship("Course", back_populates="category")
    programs = relationship("CourseProgram", back_populates="category", cascade="all, delete-orphan")

class CourseProgram(Base):
    __tablename__ = "course_programs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    language_id = Column(UUID(as_uuid=True), ForeignKey("languages.id", ondelete="CASCADE"), nullable=True)
    name_ar = Column(String(200), nullable=False)
    name_en = Column(String(200), nullable=True)
    slug = Column(String(220), unique=True, nullable=False, index=True)
    description_ar = Column(Text, nullable=True)
    description_en = Column(Text, nullable=True)
    program_type = Column(String(30), nullable=False, default="language") # language, computer, professional, other
    status = Column(String(20), nullable=False, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    category = relationship("Category", back_populates="programs")
    levels = relationship("Level", back_populates="program", cascade="all, delete-orphan")
    curriculums = relationship("Curriculum", secondary=program_curriculums, back_populates="programs")
    courses = relationship("Course", back_populates="program")

class Level(Base):
    __tablename__ = "levels"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id = Column(UUID(as_uuid=True), ForeignKey("course_programs.id", ondelete="CASCADE"), nullable=False)
    name_ar = Column(String(150), nullable=False)
    name_en = Column(String(150), nullable=True)
    code = Column(String(50), nullable=True)
    description_ar = Column(Text, nullable=True)
    description_en = Column(Text, nullable=True)
    level_order = Column(Integer, nullable=False, default=1)
    minimum_age = Column(Integer, nullable=True)
    status = Column(String(20), nullable=False, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    program = relationship("CourseProgram", back_populates="levels")
    courses = relationship("Course", back_populates="level")

class Curriculum(Base):
    __tablename__ = "curriculums"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    publisher = Column(String(200), nullable=True)
    edition = Column(String(100), nullable=True)
    description_ar = Column(Text, nullable=True)
    description_en = Column(Text, nullable=True)
    cover_image_id = Column(UUID(as_uuid=True), ForeignKey("media.id", ondelete="SET NULL"), nullable=True)
    external_url = Column(String(500), nullable=True)
    status = Column(String(20), nullable=False, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    programs = relationship("CourseProgram", secondary=program_curriculums, back_populates="curriculums")
    courses = relationship("Course", back_populates="curriculum")

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id = Column(UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    program_id = Column(UUID(as_uuid=True), ForeignKey("course_programs.id", ondelete="SET NULL"), nullable=True)
    level_id = Column(UUID(as_uuid=True), ForeignKey("levels.id", ondelete="SET NULL"), nullable=True)
    curriculum_id = Column(UUID(as_uuid=True), ForeignKey("curriculums.id", ondelete="SET NULL"), nullable=True)
    language_id = Column(UUID(as_uuid=True), ForeignKey("languages.id", ondelete="SET NULL"), nullable=True)
    category_name = Column(String(100), nullable=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    instructor_name = Column(String(150), nullable=True)
    price = Column(Numeric(10, 2), nullable=False, default=0.00)
    image_url = Column(String(255), nullable=True)
    is_published = Column(Boolean, default=True)
    seats_available = Column(Integer, nullable=True, default=30)
    registration_deadline = Column(String(100), nullable=True)
    start_date = Column(String(100), nullable=True)
    end_date = Column(String(100), nullable=True)
    class_time = Column(String(100), nullable=True, default="08:00 - 10:00")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    institute = relationship("Institute", back_populates="courses")
    category = relationship("Category", back_populates="courses")
    program = relationship("CourseProgram", back_populates="courses")
    level = relationship("Level", back_populates="courses")
    curriculum = relationship("Curriculum", back_populates="courses")
    language = relationship("Language")
    bookings = relationship("Booking", back_populates="course", cascade="all, delete-orphan")

class Student(Base):
    __tablename__ = "students"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=False)
    is_email_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    fcm_token = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    bookings = relationship("Booking", back_populates="student", cascade="all, delete-orphan")

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    registration_type = Column(String(20), nullable=False) # personal, family
    seats = Column(Integer, nullable=False, default=1)
    student_name = Column(String(150), nullable=False)
    student_phone = Column(String(20), nullable=False)
    payment_method = Column(String(20), nullable=False) # cash, electronic
    payment_status = Column(String(20), default="pending") # pending, confirmed, cancelled
    transaction_id = Column(String(100), nullable=True)
    receipt_image_url = Column(String(255), nullable=True)
    
    # Advanced Phase 4 Fields
    terms_accepted = Column(Boolean, default=True, nullable=False)
    cancellation_reason = Column(Text, nullable=True)
    refunded_amount = Column(Numeric(10, 2), nullable=True)
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    
    student = relationship("Student", back_populates="bookings")
    course = relationship("Course", back_populates="bookings")

class Banner(Base):
    __tablename__ = "banners"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    image_url = Column(Text, nullable=False)
    category = Column(String(50), nullable=False) # news, discount, event
    target_url = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class SuperAdminRequest(Base):
    __tablename__ = "super_admin_requests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id = Column(UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=False)
    request_type = Column(String(50), nullable=False) # ad, category, support
    title = Column(String(200), nullable=True) # ad title, category name
    details = Column(Text, nullable=True) # ad details, category name en, or support details
    image_url = Column(String(255), nullable=True) # ad image URL
    status = Column(String(20), default="pending") # pending, approved, rejected
    created_at = Column(DateTime, default=datetime.utcnow)
    
    institute = relationship("Institute")

class Language(Base):
    __tablename__ = "languages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    code = Column(String(50), nullable=False, unique=True, index=True)
    flag_path = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id", ondelete="CASCADE"), nullable=True)
    institute_id = Column(UUID(as_uuid=True), ForeignKey("institutes.id", ondelete="CASCADE"), nullable=True)
    rating = Column(Integer, nullable=False, default=5) # 1 to 5 stars
    comment = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, default="approved") # approved, hidden, pending
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User")
    course = relationship("Course")
    institute = relationship("Institute")

class Promotion(Base):
    __tablename__ = "promotions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), unique=True, nullable=False, index=True) # Coupon code e.g. SUM50
    discount_type = Column(String(20), nullable=False, default="percentage") # percentage, fixed
    discount_value = Column(Numeric(10, 2), nullable=False) # e.g. 50.00 or 10.00
    min_order_value = Column(Numeric(10, 2), nullable=True)
    max_discount_value = Column(Numeric(10, 2), nullable=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    usage_limit = Column(Integer, nullable=True)
    used_count = Column(Integer, nullable=False, default=0)
    status = Column(String(20), nullable=False, default="active") # active, expired, disabled
    created_at = Column(DateTime, default=datetime.utcnow)

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    body = Column(Text, nullable=False)
    notification_type = Column(String(50), nullable=False, default="general") # general, booking_status, payment_approval
    is_read = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    read_at = Column(DateTime, nullable=True)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action = Column(String(100), nullable=False) # e.g. "update_course_price", "ban_user"
    target_table = Column(String(100), nullable=True) # e.g. "courses"
    target_id = Column(String(100), nullable=True)
    details = Column(Text, nullable=True) # JSON or plain text details
    ip_address = Column(String(45), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
