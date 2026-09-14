# Helpdesk Ticket Management System

A production-oriented Python command-line application for managing internal helpdesk and IT support tickets.

The system allows support teams to create, track, assign, update, resolve, close, search, and audit tickets while maintaining persistent SQLite storage, validation, logging, exception handling, and automated tests.

This project was developed as **Aptura Tech Solutions — Python Internship Week 4, Final Task 1: Production-Grade Python Application**.

---

## Project Overview

Support requests are often handled through informal channels such as messages, emails, or verbal communication. This can make it difficult to track ticket ownership, status, priority, resolution history, and previous changes.

The Helpdesk Ticket Management System provides a structured workflow for handling these requests.

A ticket follows the lifecycle:

```text
OPEN
  ↓
IN_PROGRESS
  ↓
RESOLVED
  ↓
CLOSED
```

All important ticket changes are stored in an audit history.

---

## Key Features

### Ticket Management

The application supports:

- Create new tickets
- View a specific ticket
- List all tickets
- Search tickets
- Update ticket details
- Assign tickets to support personnel
- Change ticket priority
- Change ticket status
- Add ticket resolution
- Close resolved tickets
- View complete ticket audit history

### Ticket Categories

Supported categories:

- Hardware
- Software
- Network
- Email
- Access
- Printer
- Other

### Ticket Priorities

Supported priority levels:

- LOW
- MEDIUM
- HIGH
- CRITICAL

### Ticket Statuses

Supported statuses:

- OPEN
- IN_PROGRESS
- RESOLVED
- CLOSED

---

## Business Rules

The application enforces workflow rules instead of allowing unrestricted ticket changes.

Examples:

- A ticket must contain valid required information before it can be saved.
- A ticket cannot be resolved without a resolution.
- A ticket can only be closed after it has been resolved.
- Closed tickets cannot be edited.
- Closed tickets cannot be reassigned.
- Closed ticket priority cannot be changed.
- Empty searches are rejected.
- Duplicate status or priority operations are rejected.
- Invalid workflow transitions are blocked.

---

## Architecture

The project uses a modular layered architecture.

```text
CLI
 ↓
Application Bootstrap
 ↓
Service Layer
 ↓
Validation Layer
 ↓
Repository Layer
 ↓
SQLite Database
```

Supporting components include:

```text
Configuration Management
Logging
Custom Exceptions
Audit History
Automated Tests
```

### Layer Responsibilities

#### CLI Layer

Handles user interaction through the terminal.

#### Service Layer

Contains helpdesk business rules and ticket workflow logic.

#### Validation Layer

Validates ticket data before it reaches persistent storage.

#### Repository Layer

Handles database operations and converts SQLite records into Python objects.

#### Model Layer

Defines the Ticket domain model, categories, priorities, and statuses.

#### Database Layer

Manages SQLite connections and schema creation.

---

## Project Structure

```text
Task1_Helpdesk_Ticket_Management_System/
│
├── config/
│   └── settings.json
│
├── data/
│   └── helpdesk.db
│
├── docs/
│
├── logs/
│   └── helpdesk.log
│
├── screenshots/
│
├── src/
│   ├── cli/
│   │   ├── __init__.py
│   │   └── menu.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── config_loader.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   └── schema.py
│   │
│   ├── exceptions/
│   │   ├── __init__.py
│   │   └── exceptions.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── ticket.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── ticket_repository.py
│   │   └── ticket_history_repository.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── ticket_service.py
│   │
│   ├── validators/
│   │   ├── __init__.py
│   │   └── ticket_validator.py
│   │
│   ├── __init__.py
│   ├── application.py
│   └── logging_setup.py
│
├── tests/
│   ├── integration/
│   │   ├── test_database_foundation.py
│   │   ├── test_ticket_repository.py
│   │   └── test_ticket_service.py
│   │
│   └── unit/
│       ├── test_config_loader.py
│       ├── test_logging_setup.py
│       ├── test_ticket_model.py
│       └── test_ticket_validator.py
│
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

---

## Technology Stack

- Python 3.10+
- SQLite
- Python `sqlite3`
- Python `logging`
- Python `json`
- Python `pathlib`
- Python `datetime`
- Python `unittest`
- Python `dataclasses`
- Python `enum`

No third-party Python packages are required.

---

## Database

The project uses SQLite for persistent storage.

Default database location:

```text
data/helpdesk.db
```

### Main Tables

#### `tickets`

Stores current ticket information including:

- Ticket number
- Title
- Description
- Category
- Priority
- Status
- Requester
- Assignee
- Resolution
- Creation timestamp
- Update timestamp
- Resolution timestamp
- Closure timestamp

#### `ticket_history`

Stores ticket audit events including:

- Ticket ID
- Action
- Changed field
- Old value
- New value
- Change timestamp

Foreign-key constraints are enabled for database connections.

---

## Configuration Management

Application settings are stored in:

```text
config/settings.json
```

Example:

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

The configuration loader validates required sections and values before application initialization.

---

## Validation

The application validates input before persistence.

Validation includes:

- Ticket number format
- Ticket title length
- Description length
- Requester name
- Email format
- Ticket category
- Ticket priority
- Ticket status
- Assigned technician
- Resolution text

Example ticket number:

```text
HD-00001
```

Invalid data raises controlled application exceptions rather than being silently saved.

---

## Exception Handling

The project uses custom exceptions including:

```text
HelpdeskError
ConfigurationError
DatabaseError
ValidationError
TicketNotFoundError
InvalidStatusTransitionError
```

Expected application errors are shown to the user in a controlled format.

Unexpected application failures are logged for investigation.

---

## Logging

Runtime logs are stored in:

```text
logs/helpdesk.log
```

Example log format:

```text
2026-09-13 14:05:51,923 | INFO | helpdesk | Starting Helpdesk Ticket Management System.
```

The logging system uses rotating file logging to prevent uncontrolled log-file growth.

---

## Running the Application

Open PowerShell or another terminal in the project directory.

Run:

```powershell
python main.py
```

The main menu will appear:

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
```

Use the corresponding menu number to perform an operation.

---

## Example Workflow

A typical support workflow is:

```text
Create Ticket
     ↓
OPEN
     ↓
Assign Support Engineer
     ↓
IN_PROGRESS
     ↓
Add Resolution
     ↓
RESOLVED
     ↓
CLOSED
```

Each meaningful change is also stored in the ticket history.

Example history:

```text
CREATED
ASSIGNED
STATUS_CHANGED
RESOLUTION_UPDATED
STATUS_CHANGED
STATUS_CHANGED
```

---

## Running Automated Tests

### Unit Tests

Run:

```powershell
python -m unittest discover -s tests\unit -p "test_*.py" -v
```

Verified result:

```text
24 tests passed
```

### Integration Tests

Run:

```powershell
python -m unittest discover -s tests\integration -p "test_*.py" -v
```

Verified result:

```text
22 tests passed
```

### Current Verified Test Result

```text
Unit Tests        : 24/24 PASS
Integration Tests : 22/22 PASS
--------------------------------
Total             : 46/46 PASS
```

The test suite covers configuration, logging, ticket models, validation, SQLite connectivity, database schema, repositories, ticket business rules, audit history, and status workflows.

---

## Syntax Verification

The complete project can be syntax-checked with:

```powershell
python -m compileall -q src tests main.py
```

A successful check completes without Python compilation errors.

---

## Manual QA Performed

The application was also tested interactively.

Verified operations include:

- Application startup
- Application clean exit
- Ticket creation
- Ticket retrieval
- Ticket listing
- Ticket search
- Ticket updates
- Assignment
- Priority changes
- Status transitions
- Resolution handling
- Ticket closure
- Audit-history retrieval
- Database persistence
- Log generation

A complete ticket lifecycle was successfully verified:

```text
OPEN → IN_PROGRESS → RESOLVED → CLOSED
```

---

## Security and Reliability Considerations

The application includes several defensive practices:

- Parameterized SQL queries
- SQLite foreign-key enforcement
- Input validation
- Controlled status transitions
- Custom exception handling
- No hard-coded passwords or API keys
- Configuration separated from application logic
- Rotating application logs
- Audit history for ticket changes
- Temporary isolated databases for automated integration tests

---

## Current Limitations

This version is intentionally focused on the Week 4 Task 1 scope.

Current limitations include:

- Command-line interface only
- Single local SQLite database
- No user authentication
- No role-based authorization
- No email or external notification integration
- No web dashboard
- No distributed or multi-server deployment
- No automated scheduled reporting in Task 1

These limitations do not prevent the application from functioning as a complete local helpdesk ticket-management system.

---

## Future Improvements

Possible future improvements include:

- Automated reporting
- Overdue-ticket detection
- Scheduled workflows
- Notification logic
- User authentication
- Role-based access control
- Web or desktop interface
- REST API
- Reporting dashboard
- SLA management
- Database migration support
- Multi-user deployment

Automation and quality-engineering extensions are planned separately under the Week 4 Final Task 2 scope.

---

## Project Status

```text
Task 1 Core Application       COMPLETE
Persistent Storage            COMPLETE
Validation                    COMPLETE
Logging                       COMPLETE
Exception Handling            COMPLETE
Automated Testing             COMPLETE
Manual Functional QA          COMPLETE
```

Verified automated test result:

```text
46/46 tests passing
```

---

## Author

Developed as part of the Python Programming Internship at Aptura Tech Solutions.
