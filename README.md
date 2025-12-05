# JobPilot – AI Job Application Automation

JobPilot is an intelligent agent that automates your end-to-end job application workflow:
- Finds relevant job listings
- Generates personalized cover letters from your CV and job descriptions
- Sends applications via email with attachments
- Logs and tracks everything in Google Sheets
- Provides a real-time dashboard (Streamlit) to monitor progress

This project helps you stay organized, apply faster, and follow up on time.

---

## Key Features

- Job Scraping
  - Automatically scrapes job listings from sources like Adzuna based on predefined queries (role, location, keywords).
- Personalized Cover Letters
  - Generates tailored cover letters using job titles, company names, descriptions, and experience extracted from your uploaded CV.
- Automated Emailing
  - Sends emails to recruiters/HR with the generated cover letter and your CV as attachments via SMTP.
- Google Sheets Tracking
  - Logs each application, status, and follow-up dates into a Google Sheets dashboard.
- Streamlit Dashboard
  - Real-time, interactive dashboard to manage jobs, generate letters, and send applications from a single place.

---

## Tech Stack

- Python 3.x
- Streamlit (dashboard)
- BeautifulSoup / requests (scraping)
- gspread + Google APIs (Sheets/Drive)
- pandas (data handling)
- SMTP (email)

---

## Project Structure

```plaintext
JobPilot/
├── config/                          # Configuration files (.env, SMTP, API keys)
├── database/                        # Local data storage / job application records
├── env/                             # Virtual environment (excluded from Git)
├── src/                             # Core modules
│   ├── job_scraper.py               # Scrapes job listings (e.g., Adzuna)
│   ├── nlp_processing.py            # Processes job text, extracts entities
│   ├── cover_letter_generator.py    # Creates personalized cover letters
│   ├── email_sender.py              # Sends emails with attachments (CV, letter)
│   ├── google_sheet_integration.py  # Logs and reads data from Google Sheets
├── static/                          # Static assets (CSS, JS, images)
├── templates/                       # HTML templates (if needed)
├── uploads/                         # User uploads (CVs, job data exports)
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

Note: Exact filenames may differ; adapt paths as needed for your repository.

---

## Getting Started

### Prerequisites

- Python 3.x
- pip (Python package manager)
- A Google account with access to Google Cloud Console
- SMTP-enabled email account (e.g., Gmail)

### 1) Clone the Repository

```bash
git clone https://github.com/nikhilnagar503/JobPilot.git
cd JobPilot
```

### 2) Create and Activate Virtual Environment (recommended)

```bash
python -m venv env
# Windows
env\Scripts\activate
# macOS/Linux
source env/bin/activate
```

### 3) Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

### 4) Set Up Google APIs

1. Open Google Cloud Console
2. Create a new Project
3. Enable:
   - Google Sheets API
   - Google Drive API
4. Configure OAuth Consent Screen
   - Set to Testing (for development)
5. Create OAuth Client ID
   - Application Type: Desktop App
6. Download credentials file
   - Save as `client_secret.json` under `auth/` (create the folder if missing)

On first run, you will be prompted to authenticate; a token file will be generated (commonly `token.json`) for subsequent access.

### 5) Configure Email (SMTP)

Update your SMTP settings. Option A: Environment variables in `.env`. Option B: Hardcode in `src/email_sender.py` (not recommended).

Example `.env`:

```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password   # Use App Passwords for Gmail
SENDER_NAME=Your Name
SENDER_EMAIL=your_email@gmail.com
```

For Gmail, enable “Less secure app access” or (recommended) create an App Password with 2FA enabled.

### 6) Other Environment Variables

You may define the following in `.env`:

```
# Job search defaults
JOB_QUERY="software engineer"
JOB_LOCATION="remote"
JOB_SOURCES="adzuna"

# Google Sheets
GOOGLE_SHEET_NAME="JobPilot Applications"
GOOGLE_SHEET_WORKSHEET="Applications"
```

---

## Usage

### Run the Streamlit Dashboard

```bash
streamlit run dashboard.py
```

This will:
- Scrape job listings
- Generate tailored cover letters based on your CV and job descriptions
- Send emails with attachments
- Track and update application statuses in Google Sheets

Typical workflow:
1. Search Jobs: Define target roles/locations in the dashboard
2. Upload CV: Extract experience/skills
3. Generate Cover Letters: Tailored per job
4. Apply: Send emails directly via dashboard
5. Track: Monitor status and follow-ups in Google Sheets

---

## How It Works (Architecture)

- Data Flow
  - `job_scraper.py` fetches jobs and normalizes fields (title, company, location, description, URL).
  - `nlp_processing.py` extracts skills, keywords, and relevant experience from your CV and job description.
  - `cover_letter_generator.py` builds a personalized letter with measured alignment to the role and company.
  - `email_sender.py` composes and sends messages, attaching CV and cover letter.
  - `google_sheet_integration.py` logs each application, status, and follow-up dates in Sheets.

- Dashboard
  - Streamlit orchestrates the modules, offering controls for queries, file uploads, previews, and actions.

---

## Data Model (Example)

Applications are stored with fields like:
- id
- date_applied
- role_title
- company_name
- job_location
- job_url
- cover_letter_path
- cv_path
- email_status (sent/failed)
- application_status (applied/interview/offers/rejected)
- next_follow_up_date
- notes

---

## Security and Privacy

- Credentials
  - Keep `client_secret.json`, `token.json`, and `.env` out of source control. Ensure they are listed in `.gitignore`.
- Email
  - Use app-specific passwords for SMTP providers (e.g., Gmail).
- PII
  - CVs and personal data should remain local and encrypted at rest if possible.
- API Quotas
  - Respect rate limits and robots.txt of job sources; scraping should be compliant with terms of service.

---

## Troubleshooting

- Google Auth Errors
  - Ensure `client_secret.json` is in `auth/` and OAuth consent screen is configured.
  - Delete `token.json` and re-authenticate if scopes change.

- SMTP Errors
  - Verify host/port and credentials.
  - For Gmail, ensure App Passwords are used and IMAP/SMTP access enabled.

- Streamlit Not Found
  - Confirm installation: `pip install streamlit`.
  - Re-activate virtual environment.

- Sheets Not Updating
  - Check worksheet name and sharing permissions.
  - Ensure the authenticated Google account has edit access.

---

## Extensibility

- Add new job sources:
  - Implement source-specific scrapers under `src/job_scraper.py` and unify outputs.
- Multi-template cover letters:
  - Support multiple tone/style templates and A/B testing.
- CRM-style tracking:
  - Add reminders, email threading, and interview notes.
- ATS optimization:
  - Enhance CV parsing and keyword alignment scoring.

---

## Example Commands

- Export current applications to CSV:
  ```bash
  python -m src.export_applications --out exports/applications.csv
  ```
- Re-run scraping only:
  ```bash
  python -m src.job_scraper --query "data scientist" --location "remote"
  ```

---

## FAQ

- Can I use Outlook or other SMTP providers?
  - Yes, set the appropriate SMTP host/port and credentials in `.env`.

- Does it support multiple CVs?
  - You can extend the dashboard to select different CVs per application.

- Can I run it headless?
  - Core modules can be scripted; the dashboard is optional for UI.

---

## Contributing

Pull requests are welcome! Please:
- Open an issue describing the change
- Follow Python code style (black/flake8)
- Add tests if applicable
- Keep credentials out of commits

---

## License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.

---

## Acknowledgements

- Streamlit for rapid dashboarding
- Google APIs for convenient application tracking
- Open-source scraping and NLP libraries
