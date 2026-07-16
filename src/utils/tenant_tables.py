from src.extensions import db


def create_tenant_tables(schema_name: str):
    """
    Creates all tenant specific tables for a newly onboarded school.
    """

    # ==========================
    # USERS TABLE
    # ==========================
    db.session.execute(db.text(f"""
        CREATE TABLE IF NOT EXISTS {schema_name}.users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role VARCHAR(50) NOT NULL,
            status VARCHAR(20) DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """))

    # ==========================
    # STUDENTS TABLE
    # ==========================
    db.session.execute(db.text(f"""
        CREATE TABLE IF NOT EXISTS {schema_name}.students (
            id SERIAL PRIMARY KEY,
            admission_no VARCHAR(50) UNIQUE NOT NULL,
            roll_no VARCHAR(20),

            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100),

            gender VARCHAR(20),
            dob DATE,

            mobile VARCHAR(20),
            email VARCHAR(120),

            father_name VARCHAR(100),
            mother_name VARCHAR(100),

            class_name VARCHAR(50),
            section VARCHAR(20),

            address TEXT,
            photo VARCHAR(255),

            status VARCHAR(20) DEFAULT 'active',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """))

    # ==========================
    # TEACHERS TABLE
    # ==========================
    db.session.execute(db.text(f"""
        CREATE TABLE IF NOT EXISTS {schema_name}.teachers (
            id SERIAL PRIMARY KEY,

            employee_id VARCHAR(50) UNIQUE,

            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100),

            gender VARCHAR(20),

            mobile VARCHAR(20),
            email VARCHAR(120),

            qualification VARCHAR(100),
            experience VARCHAR(50),

            address TEXT,
            photo VARCHAR(255),

            status VARCHAR(20) DEFAULT 'active',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """))

    # ==========================
    # PARENTS TABLE
    # ==========================
    db.session.execute(db.text(f"""
        CREATE TABLE IF NOT EXISTS {schema_name}.parents (
            id SERIAL PRIMARY KEY,

            father_name VARCHAR(100),
            mother_name VARCHAR(100),

            mobile VARCHAR(20),
            email VARCHAR(120),

            address TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """))

    # ==========================
    # CLASSES TABLE
    # ==========================
    db.session.execute(db.text(f"""
        CREATE TABLE IF NOT EXISTS {schema_name}.classes (
            id SERIAL PRIMARY KEY,

            class_name VARCHAR(50) NOT NULL,
            section VARCHAR(20),

            class_teacher VARCHAR(100),

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """))

    db.session.commit()