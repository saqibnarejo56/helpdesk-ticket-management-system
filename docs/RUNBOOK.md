# Operational Runbook — Helpdesk Ticket Management System

## 1. Purpose

This runbook explains how to start, operate, verify, and troubleshoot the Helpdesk Ticket Management System.

It is intended for someone who receives the project and needs to run it without understanding the complete source code first.

---

## 2. Runtime Requirements

The application requires:

```text
Python 3.10 or later
```

No third-party Python packages are required for the completed Task 1 application.

The project uses Python standard-library modules including:

```text
sqlite3
logging
json
pathlib
datetime
unittest
dataclasses
enum
```

---

## 3. Project Entry Point

The application is started from:

```text
main.py
```

The command should be executed from the project root:

```text
Task1_Helpdesk_Ticket_Management_System
```

---

## 4. Start the Application

Open PowerShell in the project folder.

Run:

```powershell
python main.py
```

A successful startup displays:

```text
============================================
     HELPDESK TICKET MANAGEMENT SYSTEM
============================================
1.  Create Ticket
2.  View Ticket
3.  List All Tickets
4.  Search Tickets
5.  Update Ticket Details
6.  Assign Ticket
7.  Change Priority
8.  Change Status
9.  Add Resolution
10. View Ticket History
0.  Exit
============================================
Select an option:
```

---

## 5. Stop the Application

From the main menu, enter:

```text
0
```

A normal shutdown displays:

```text
Thank you for using the Helpdesk Ticket Management System.
```

The application can also be interrupted with:

```text
Ctrl + C
```

The entry point handles keyboard interruption separately from unexpected application failures.

---

## 6. Configuration

Runtime configuration is stored in:

```text
config/settings.json
```

Current configuration structure:

```json
{
  "application": {
    "name": "Helpdesk Ticket Management System",
    "version": "1.0.0",
    "environment": "development"
  },
  "database": {
    "path": "data/helpdesk.db"
  },
  "logging": {
    "level": "INFO",
    "file": "logs/helpdesk.log"
  }
}
```

The application validates the required configuration sections during startup.

If the configuration file is missing or invalid, application initialization will fail with a controlled configuration error.

---

## 7. Database

The SQLite database is stored at:

```text
data/helpdesk.db
```

The application uses two main tables:

```text
tickets
ticket_history
```

When the application initializes, the database schema is created if the required tables do not already exist.

The database connection also enables SQLite foreign-key enforcement.

---

## 8. Logs

Application logs are written to:

```text
logs/helpdesk.log
```

To inspect the log from PowerShell:

```powershell
Get-Content logs\helpdesk.log
```

The logging configuration uses rotating file logging.

When troubleshooting unexpected application behavior, this log should be checked first.

---

## 9. Basic Operational Workflow

A normal helpdesk workflow is:

```text
Create Ticket
     ↓
Assign Ticket
     ↓
OPEN
     ↓
IN_PROGRESS
     ↓
Add Resolution
     ↓
RESOLVED
     ↓
CLOSED
```

The application enforces the valid status workflow through the service layer.

---

## 10. Ticket Number Format

Tickets use the format:

```text
HD-00001
HD-00002
HD-00003
```

Ticket numbers are generated sequentially by the application.

---

## 11. Supported Ticket Categories

```text
Hardware
Software
Network
Email
Access
Printer
Other
```

---

## 12. Supported Priorities

```text
LOW
MEDIUM
HIGH
CRITICAL
```

---

## 13. Supported Statuses

```text
OPEN
IN_PROGRESS
RESOLVED
CLOSED
```

---

## 14. Important Workflow Rules

Operators should be aware of the following implemented rules:

- A ticket cannot be resolved without a resolution.
- A ticket must be resolved before it can be closed.
- Closed tickets cannot be edited.
- Closed tickets cannot be reassigned.
- Priority cannot be changed after a ticket is closed.
- Invalid status transitions are rejected.
- Empty searches are rejected.
- Invalid ticket data is rejected before persistence.

---

## 15. Quick Application Verification

To verify that the Python source files compile:

```powershell
python -m compileall -q src tests main.py
```

A successful run completes without compilation errors.

Then start the application:

```powershell
python main.py
```

Confirm that the main menu appears.

Exit using:

```text
0
```

This startup and clean-exit sequence was successfully verified during development.

---

## 16. Automated Verification

Unit tests can be executed with:

```powershell
python -m unittest discover -s tests\unit -p "test_*.py" -v
```

Integration tests can be executed with:

```powershell
python -m unittest discover -s tests\integration -p "test_*.py" -v
```

The most recently verified development result was:

```text
Unit Tests        : 24/24 PASS
Integration Tests : 22/22 PASS
Total             : 46/46 PASS
```

Detailed QA evidence is documented in:

```text
docs/TESTING.md
```

---

## 17. Troubleshooting

### Application Displays No Menu

Confirm that the command is being executed from the project root:

```powershell
python main.py
```

Do not run `main.py` from an unrelated working directory.

---

### Configuration Error

Check:

```text
config/settings.json
```

Validate its JSON syntax with:

```powershell
python -m json.tool config\settings.json
```

A valid configuration should be printed back without a JSON parsing error.

---

### Database Problems

Confirm that the configured database path is:

```text
data/helpdesk.db
```

Check the application log:

```powershell
Get-Content logs\helpdesk.log
```

Database-related application failures are handled through the database exception layer.

---

### Invalid Ticket Data

Review the entered values.

Examples of rejected data include:

```text
Invalid email address
Invalid ticket number
Very short title
Very short description
Unsupported category
Unsupported priority
Unsupported status
Blank assignment
Blank resolution
```

---

### Ticket Cannot Be Resolved

A resolution must be added first.

Use:

```text
9. Add Resolution
```

Then change the status to:

```text
RESOLVED
```

---

### Ticket Cannot Be Closed

The ticket must already be:

```text
RESOLVED
```

before it can transition to:

```text
CLOSED
```

---

### Closed Ticket Cannot Be Modified

This is expected application behavior.

Closed tickets are intentionally protected from:

```text
editing
reassignment
priority changes
```

---

## 18. Audit History

Ticket history can be viewed through:

```text
10. View Ticket History
```

Recorded audit events can include:

```text
CREATED
UPDATED
ASSIGNED
PRIORITY_CHANGED
STATUS_CHANGED
RESOLUTION_UPDATED
```

History records contain old and new values where applicable.

---

## 19. Runtime Files

The main runtime-generated files are:

```text
data/helpdesk.db
logs/helpdesk.log
```

Python may also create:

```text
__pycache__/
*.pyc
```

These generated artifacts are excluded from source-control tracking through `.gitignore` where appropriate.

---

## 20. Recovery Notes

The SQLite database contains the application ticket data.

Deleting:

```text
data/helpdesk.db
```

removes the existing local ticket data.

On a later application startup, the application can create a new SQLite database and schema, but deleted ticket data is not restored automatically.

Therefore, the existing database should not be deleted when its ticket records need to be preserved.

---

## 21. Operational Limitations

The current Task 1 version is a local command-line application.

It does not currently provide:

```text
Authentication
Role-based access control
Web access
REST API
Email notifications
Scheduled automation
Multi-user network operation
```

These capabilities should not be assumed when operating the current version.

---

## 22. Related Documentation

Project overview and usage:

```text
README.md
```

Testing and QA evidence:

```text
docs/TESTING.md
```

Engineering summary and final outcome:

```text
docs/FINAL_REPORT.md
```

This file:

```text
docs/RUNBOOK.md
```

is focused specifically on operating and troubleshooting the application.
