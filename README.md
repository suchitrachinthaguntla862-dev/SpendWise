# SpendWise — Expense Tracker

SpendWise is a beginner-friendly Django web app for recording everyday expenses and understanding where your money goes.

## Features
- Sign up, log in, and log out
- Add, edit, and delete personal expenses
- Categories, dates, notes, and amounts
- Dashboard with total spending this month and all-time
- Category-wise spending summary
- Responsive interface
- SQLite database for local development

## Requirements
- Python 3.10 or newer
- Internet connection for the first dependency installation

## Run on Windows (PowerShell)
Open PowerShell in the folder containing `manage.py`, then run:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

Create an account using **Sign up**. The included migration creates the app's database tables.

## GitHub
Create an empty GitHub repository, then run in the project folder:

```powershell
git init
git add .
git commit -m "Initial SpendWise expense tracker"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the example URL with your repository URL. Do not upload passwords or secret keys. This project uses a development-only secret key and is not production-ready without security configuration.
