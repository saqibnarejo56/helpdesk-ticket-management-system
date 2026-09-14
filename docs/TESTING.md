# Testing and QA Evidence

## Project

Helpdesk Ticket Management System

## Purpose

This document records the automated and manual testing performed for the Week 4 Final Task 1 application.

Only tests and results that were actually executed and verified are included here.

---

## Automated Test Summary

### Unit Tests

Command used:

```powershell
python -m unittest discover -s tests\unit -p "test_*.py" -v
```

Verified result:

```text
Ran 24 tests
OK
```

Unit-test coverage includes:

- Configuration loading
- Missing configuration handling
- Invalid logging levels
- Logging initialization
- Log-file creation
- Ticket model defaults
- Ticket timestamps
- Ticket serialization
- Ticket validation
- Invalid email handling
- Invalid ticket-number handling
- Invalid title and description handling
- Invalid category and priority handling
- Empty assignment and resolution handling

---

## Integration Tests

Command used:

```powershell
python -m unittest discover -s tests\integration -p "test_*.py" -v
```

Verified result:

```text
Ran 22 tests
OK
```

Integration-test coverage includes:

- SQLite database creation
- Database connection testing
- SQLite foreign-key enforcement
- Database schema creation
- Required table verification
- Ticket creation and retrieval
- Ticket listing
- Ticket searching
- Ticket updating
- Ticket-number generation
- Missing-ticket handling
- Ticket assignment
- Priority changes
- Ticket-detail updates
- Resolution requirements
- Ticket status workflow
- Invalid status transitions
- Closed-ticket protection
- Audit-history creation
- Audit-history retrieval

---

## Verified Automated Test Total

```text
Unit Tests        : 24/24 PASS
Integration Tests : 22/22 PASS
--------------------------------
Total             : 46/46 PASS
```

---

## Syntax Verification

The full project was compiled using:

```powershell
python -m compileall -q src tests main.py
```

Verified result:

```text
No compilation errors were reported.
```

---

## Manual Functional QA

The application was also tested manually using:

```powershell
python main.py
```

The following operations were successfully verified:

- Application startup
- Application clean exit
- Create Ticket
- View Ticket
- List All Tickets
- Search Tickets
- Update Ticket Details
- Assign Ticket
- Change Priority
- Change Status
- Add Resolution
- View Ticket History

---

## Verified Ticket Lifecycle

A real ticket was created and moved through the following lifecycle:

```text
OPEN
  ↓
IN_PROGRESS
  ↓
RESOLVED
  ↓
CLOSED
```

The ticket was also:

- Assigned to a support engineer
- Given a resolution
- Persisted in SQLite
- Recorded in the audit-history table

---

## Verified Audit History

The tested ticket recorded the following sequence:

```text
CREATED
ASSIGNED
STATUS_CHANGED
RESOLUTION_UPDATED
STATUS_CHANGED
STATUS_CHANGED
```

Each audit entry stored:

- Action
- Field name
- Old value
- New value
- Timestamp

---

## Logging Verification

Logging was tested by writing an actual log entry to:

```text
logs/helpdesk.log
```

Verified log output included:

```text
INFO | helpdesk | Helpdesk logging system initialized successfully.
```

Application startup and initialization were also successfully recorded in the log file.

---

## Database Verification

The SQLite database was verified to contain:

```text
tickets
ticket_history
```

The application also verified:

- Persistent ticket storage
- Ticket retrieval after saving
- Ticket updates
- Ticket history
- Foreign-key enforcement

---

## QA Result

Based on the automated and manual testing performed:

```text
Automated Tests : 46 passed
Manual QA       : Core Task 1 workflows verified
Syntax Check    : Passed
Application Run : Passed
```

No unverified metrics or unsupported results are included in this document.
