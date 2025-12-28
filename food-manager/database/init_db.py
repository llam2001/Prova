import os
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS foods (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT NOT NULL,
    quantity INTEGER DEFAULT 1,
    expiry_date DATE,
    created_at DATE DEFAULT CURRENT_DATE
)
""")

conn.commit()
cur.close()
conn.close()

print("✅ Database PostgreSQL inizializzato")
