# email_sender.py
import smtplib
import os
import time
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv(dotenv_path=r"C:\Users\dell\OneDrive\Desktop\new_AI_job\AI-Agent-Job-Assistant\env\email.env")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_job_application_email(to_email, subject, body, cv_path, cover_letter_path=None,
                               job_title=None, company=None, applicant_name=None,
                               max_retries=3):
    """
    Sends an email with CV and cover letter attached.
    - to_email: string or list of strings
    - subject: string
    - body: string
    - cv_path: path to CV file (required)
    - cover_letter_path: path to an already-created cover letter. If None, we will try to generate it
      using generate_cover_letter(job_title, company, applicant_name, cv_path) if job_title/company/applicant_name provided.
    Returns True on success, False otherwise.
    """
    try:
        # Validate CV
        if not os.path.exists(cv_path):
            logging.error("CV file not found at %s", cv_path)
            return False

        # Possibly generate cover letter (if not supplied)
        if cover_letter_path is None:
            # Only attempt if we have enough info to generate
            if all([job_title, company, applicant_name]):
                try:
                    # Import here to avoid circular imports if needed
                    from src.cover_letter_generator import generate_cover_letter
                    cover_letter_path = generate_cover_letter(job_title, company, applicant_name, cv_path)
                except Exception as e:
                    logging.error("Error generating cover letter: %s", e, exc_info=True)
                    return False
            else:
                logging.error("No cover letter provided and not enough data to generate one.")
                return False

        # Validate cover letter
        if not os.path.exists(cover_letter_path):
            logging.error("Cover letter file not found at %s", cover_letter_path)
            return False

        # Load SMTP credentials
        email_user = os.getenv('EMAIL_USER')
        email_password = os.getenv('EMAIL_PASSWORD')
        email_host = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
        email_port = int(os.getenv('EMAIL_PORT', 587))

        if not email_user or not email_password:
            logging.error("Email credentials are not set properly in environment variables.")
            return False

        # Build message
        msg = MIMEMultipart()
        msg['From'] = email_user
        # Normalize recipients to list
        recipients = to_email if isinstance(to_email, (list, tuple)) else [to_email]
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Attach CV (use application/pdf when possible)
        logging.info("Attaching CV from %s", cv_path)
        with open(cv_path, 'rb') as f:
            part = MIMEBase('application', 'pdf')
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(cv_path)}"')
        msg.attach(part)

        # Attach cover letter
        logging.info("Attaching cover letter from %s", cover_letter_path)
        with open(cover_letter_path, 'rb') as f:
            part = MIMEBase('application', 'pdf')
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(cover_letter_path)}"')
        msg.attach(part)

        # Send with retries
        for attempt in range(1, max_retries + 1):
            try:
                logging.info("Connecting to SMTP server %s:%s (attempt %d)", email_host, email_port, attempt)
                with smtplib.SMTP(email_host, email_port, timeout=30) as server:
                    server.set_debuglevel(1)
                    server.starttls()
                    logging.info("Started TLS")
                    server.login(email_user, email_password)
                    logging.info("Logged in as %s", email_user)
                    # sendmail expects a list of recipients
                    server.sendmail(email_user, recipients, msg.as_string())
                    logging.info("Email sent successfully to %s", recipients)
                    return True
            except Exception as e:
                logging.error("Failed to send email (attempt %d): %s", attempt, str(e), exc_info=True)
                if attempt < max_retries:
                    time.sleep(5)
                else:
                    logging.error("All retry attempts failed.")
                    return False

    except Exception as e:
        logging.error("Unexpected error in send_job_application_email: %s", e, exc_info=True)
        return False
