# FinTrack

FinTrack is a Django-based personal expense tracker that uses an envelope-budgeting approach. Users create envelopes (budget categories), record spending against each envelope, and view monthly transactions and summaries. The project includes user authentication, envelope and transaction management, and a monthly email report.

## Key Features

### Authentication & Account Management
- User signup with validation (required fields, unique username/email, password confirmation, min length).
- Login/logout using Django auth.
- Password reset by email lookup and password update.
- Account deletion.

### Envelope Budgeting
- Create envelopes with a unique name per user and a budget allocation.
- View all envelopes for the current user.
- Update envelope name, budget, and spent amounts.
- Delete envelopes.
- Automatic remaining balance calculation based on allocated and spent.

### Expense Tracking (Envelope Descriptions)
- Add expenses (descriptions) tied to an envelope.
- Current-month-only listing of expense history.
- Update or delete specific expense records.
- Overspend confirmation flow (explicit confirmation required if remaining becomes negative).
- Money remaining is derived from envelope totals and stored on each description entry for historical accuracy.

### Monthly Operations
- Management command to reset all envelopes at the start of each month.
- Monthly email report command that sends a detailed envelope summary and transaction breakdown for the previous month.

## Project Structure

```
FinTrack/
├── db.sqlite3
├── manage.py
├── EnvelopeDescription/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── management/
│   │   └── commands/
│   │       └── send_monthly_report.py
│   ├── migrations/
│   └── templates/
│       ├── DisplayEnvelopeDescriptions.html
│       ├── FormEnvelopeDescription.html
│       └── UpdateEnvelopeDescription.html
├── Envelopes/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── management/
│   │   └── commands/
│   │       └── reset_envelopes.py
│   ├── migrations/
│   └── templates/
│       ├── addenvelope.html
│       ├── displayenvelope.html
│       ├── updateenvelope.html
│       └── updateenvelopeform.html
├── FinTrack/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── login/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   └── templates/
│       ├── index.html
│       ├── login.html
│       ├── resetPassword.html
│       └── signup.html
├── static/
│   ├── css/
│   └── js/
└── templates/
    └── base.html
```

## Tech Stack
- Django 5.2.x
- PostgreSQL (configured in settings)
- HTML/CSS/JS templates

## Database Schema

### `auth_user` (Django built-in)
Used for authentication. Key fields referenced by this project:
- `id` (PK)
- `username`
- `email`
- `first_name`
- `last_name`
- `password`

### `Envelopes.Envelope_Home`
Represents an envelope (budget category).

| Field | Type | Notes |
|------|------|------|
| `id` | PK | Auto generated |
| `username` | FK -> `auth_user` | Owner of envelope |
| `Envelope_Name` | CharField(200) | Must be unique per user (enforced in views) |
| `Money_Allocated` | Decimal(10,2) | Must be >= 0 |
| `Money_Spent` | Decimal(10,2) | Must be >= 0 |
| `Money_Remaining` | Decimal(10,2) | Must equal `Money_Allocated - Money_Spent` |
| `Created_At` | DateTime | Auto timestamp |

**Model-level constraints:**
- `Money_Allocated >= 0`
- `Money_Spent >= 0`
- `Money_Remaining = Money_Allocated - Money_Spent`

**Save behavior:**
- `Money_Remaining` is recomputed on save to keep totals consistent.

### `EnvelopeDescription.EnvelopeDescription`
Represents a spending transaction attached to a specific envelope.

| Field | Type | Notes |
|------|------|------|
| `id` | PK | Auto generated |
| `username` | FK -> `auth_user` | Owner of transaction |
| `EnvelopeName` | FK -> `Envelopes.Envelope_Home` | Envelope linked to this transaction |
| `Description` | TextField | Transaction note |
| `Money_Spent` | Decimal(10,2) | Must be > 0 |
| `Money_Remaining` | Decimal(10,2) | Balance after transaction |
| `created_at` | DateTime | Auto timestamp |

**Model-level constraints:**
- `Money_Spent > 0`

**Save behavior:**
- `full_clean()` enforces validation before saving.

## URL Routes

### Root + Authentication
- `/` → homepage dashboard
- `/login/` → login
- `/signup/` → signup
- `/logout/` → logout
- `/reset-password/` → password reset
- `/delete_account/` → delete current account

### Envelopes
- `/envelopes/addenvelope/` → create envelope
- `/envelopes/displayenvelopes/` → list envelopes
- `/envelopes/updateenvelope/` → select envelope to update
- `/envelopes/updateenvelope/update/<id>/` → update envelope
- `/envelopes/updateenvelope/delete/<id>/` → delete envelope

### Envelope Descriptions (Expenses)
- `/envelopedescription/` → add expense
- `/envelopedescription/showenvelopedescription/` → list current-month expenses
- `/envelopedescription/update/<id>/` → update expense
- `/envelopedescription/delete/<id>/` → delete expense

## Edge Cases & Validation Rules

### Authentication
- Signup rejects missing fields, duplicate usernames/emails, mismatched passwords, and short passwords.
- Reset password validates email existence, required fields, matching passwords, and length.

### Envelopes
- Envelope name required and unique per user (case-insensitive).
- Money allocated must be a positive number.
- Money values must parse to valid integers in the current implementation.
- Negative allocations or spending are rejected.
- Remaining balance cannot be negative for new envelopes.

### Expenses (Envelope Descriptions)
- Expense amount must be greater than 0.
- Envelope must belong to the current user.
- Overspending requires explicit confirmation (prevents accidental negative balances).
- Editing an expense adjusts the envelope’s totals by the delta between old and new spending.
- Deleting an expense reverses the spend and recomputes remaining safely.
- Current-month filter ensures the list view only shows transactions for the active month and year.

### Data Consistency
- Envelope remaining is enforced at model level to match allocated minus spent.
- Expense records store balance-after-transaction for historical accuracy.
- All envelope/expense operations are scoped to the logged-in user.

## Monthly Management Commands

### Reset Envelopes
Resets all envelopes to start a new month:
```
python manage.py reset_envelopes
```
Behavior:
- Sets `Money_Spent = 0`
- Sets `Money_Remaining = Money_Allocated`

### Send Monthly Report
Sends an HTML email report for the previous month:
```
python manage.py send_monthly_report
```
Report includes:
- Envelope summary (allocated, spent, remaining)
- Overspent/within-budget/exact-spend grouping
- Transaction history grouped by envelope

## Configuration

### Database
Configured for PostgreSQL in [FinTrack/settings.py](FinTrack/settings.py):
- `NAME`: FinTrack
- `USER`: postgres
- `PASSWORD`: set in file (update for production)
- `HOST`: localhost
- `PORT`: 5432

### Email
SMTP settings use environment variables loaded from `.env`:
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `DEFAULT_FROM_EMAIL`

## Running the Project (Local)
1. Create and activate a Python environment.
2. Install dependencies (at minimum: Django and psycopg2 for PostgreSQL).
3. Configure database and `.env` values.
4. Run migrations:
   - `python manage.py migrate`
5. Start the server:
   - `python manage.py runserver`

## Notes
- The project is currently configured for PostgreSQL even though `db.sqlite3` exists in the root; update settings if you want to use SQLite for local testing.
- Money values are handled as `DecimalField`, but views currently parse user input as integers; consider aligning this for cents precision if you extend the project.
