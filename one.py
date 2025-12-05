# debug_smtp_check.py  (run locally)
import os, smtplib
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))

print("EMAIL_USER present:", bool(EMAIL_USER))
print("EMAIL_PASSWORD present:", bool(EMAIL_PASSWORD))
print("EMAIL_HOST,PORT:", EMAIL_HOST, EMAIL_PORT)

# Trim whitespace
EMAIL_USER = EMAIL_USER.strip() if EMAIL_USER else EMAIL_USER
EMAIL_PASSWORD = EMAIL_PASSWORD.strip() if EMAIL_PASSWORD else EMAIL_PASSWORD

try:
    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT, timeout=15) as server:
        server.set_debuglevel(1)
        server.starttls()
        server.ehlo()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
    print("SMTP login succeeded")
except smtplib.SMTPAuthenticationError as e:
    print("SMTPAuthenticationError:", e)
except Exception as e:
    print("Other SMTP error:", e)
