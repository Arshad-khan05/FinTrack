# Monthly Email Report Feature

## Overview
This feature automatically sends a monthly spending report to all users on the 1st of each month, containing:
- Envelope status (Overspent, Within Budget, Spent Exactly)
- Transaction history from the previous month
- Spending analysis and summary

## Setup

### 1. Email Configuration

The email settings are configured in `FinTrack/settings.py`.

**Development Mode (Console Backend):**
By default, emails are printed to the console for testing:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

**Production Mode (SMTP):**
For production, update settings.py with your email provider's SMTP settings:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # or your email provider
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Use app-specific password for Gmail
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

**Note for Gmail users:**
- Enable 2-factor authentication
- Generate an app-specific password: https://myaccount.google.com/apppasswords
- Use the app password instead of your regular Gmail password

### 2. Manual Testing

Test the email report manually:
```bash
python manage.py send_monthly_report
```

This will send reports for the previous month to all users.

### 3. Automated Scheduling

To automatically send emails on the 1st of every month, use one of these methods:

#### Option A: Cron (Linux/Mac)
```bash
# Edit crontab
crontab -e

# Add this line to run at 9 AM on the 1st of every month
0 9 1 * * cd /path/to/FinTrack && /path/to/python manage.py send_monthly_report
```

#### Option B: Task Scheduler (Windows)
1. Open Task Scheduler
2. Create a new task
3. Set trigger: Monthly, on day 1, at 9:00 AM
4. Set action: Start a program
   - Program: `python.exe`
   - Arguments: `manage.py send_monthly_report`
   - Start in: `A:\Projects\FinTrack`

#### Option C: Celery Beat (Django Apps)
For Django projects with Celery:

1. Install Celery:
```bash
pip install celery django-celery-beat
```

2. Add to INSTALLED_APPS in settings.py:
```python
INSTALLED_APPS = [
    ...
    'django_celery_beat',
]
```

3. Create `FinTrack/celery.py`:
```python
from celery import Celery
from celery.schedules import crontab

app = Celery('FinTrack')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-monthly-report': {
        'task': 'EnvelopeDescription.tasks.send_monthly_reports',
        'schedule': crontab(hour=9, minute=0, day_of_month=1),
    },
}
```

4. Create `EnvelopeDescription/tasks.py`:
```python
from celery import shared_task
from django.core.management import call_command

@shared_task
def send_monthly_reports():
    call_command('send_monthly_report')
```

## Email Report Contents

The email includes:

### 1. Envelope Summary
- Envelope name
- Allocated budget
- Amount spent
- Remaining balance
- Status indicator

### 2. Spending Analysis
- **Overspent**: Envelopes where spending exceeded the budget (negative balance)
- **Spent Exactly**: Envelopes where the entire budget was used
- **Within Budget**: Envelopes with remaining balance

### 3. Transaction History
- Chronological list of all transactions from previous month
- Grouped by envelope
- Shows: date, description, amount spent, balance after transaction

## Troubleshooting

### Emails not sending
1. Check email configuration in settings.py
2. Verify user email addresses are set in Django admin
3. Check spam/junk folder
4. For Gmail, ensure app-specific password is used

### Testing
```bash
# Test email configuration
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])
```

### View console output (development mode)
Run the command and check terminal output:
```bash
python manage.py send_monthly_report
```

## Requirements

- Django 5.x
- Python 3.x
- Users must have valid email addresses set in their accounts
