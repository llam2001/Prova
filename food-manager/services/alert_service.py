from datetime import date, timedelta
from models.db import get_db
from services.mail_service import send_email

def check_alerts():
    db = get_db()
    cur = db.cursor()

    limit = date.today() + timedelta(days=3)

    cur.execute("""
        SELECT name, expiry_date
        FROM foods
        WHERE expiry_date IS NOT NULL
        AND expiry_date <= %s
    """, (limit,))

    foods = cur.fetchall()
    cur.close()
    db.close()

    if foods:
        body = "\n".join([f"{f[0]} - {f[1]}" for f in foods])
        send_email("⚠️ Alimenti in scadenza", body)

if __name__ == "__main__":
    check_alerts()
