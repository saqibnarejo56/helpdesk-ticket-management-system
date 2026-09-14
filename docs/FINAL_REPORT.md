# Final Report — Helpdesk Ticket Management System

## 1. Executive Summary

The Helpdesk Ticket Management System is a Python command-line application developed for Aptura Tech Solutions Python Internship — Week 4, Final Task 1.

The project addresses a practical support-management problem by providing a structured way to create, track, update, assign, resolve, close, and audit helpdesk tickets.

The completed application includes modular architecture, configuration management, SQLite persistence, validation, logging, exception handling, automated testing, and technical documentation.

---

## 2. Project Objective

The objective was to build a complete and usable Python application rather than a standalone script or isolated programming exercise.

The application needed to demonstrate:

- separation of responsibilities
- persistent data storage
- controlled business rules
- input validation
- failure handling
- application logging
- automated verification
- maintainable project organization

A helpdesk ticket-management system was selected because it provides a realistic business workflow with clear states, rules, and persistent records.

---

## 3. Problem Being Addressed

Support requests handled through informal channels can become difficult to manage consistently.

Common problems include:

- unclear ticket ownership
- missing priority information
- difficulty tracking ticket status
- lost resolution details
- lack of change history

The application provides a structured workflow where each support request becomes a trackable ticket with a unique ticket number and persistent history.

---

## 4. Solution Approach

The system was designed around a layered architecture instead of placing all functionality inside one Python file.

The main flow is:

```text
Command-Line Interface
        ↓
Application Bootstrap
        ↓
Service / Business Logic
        ↓
Validation
        ↓
Repositories
        ↓
SQLite Database
```

Supporting components handle:

```text
Configuration
Logging
Exceptions
Audit History
Testing
```

This keeps user interaction, business rules, validation, and database operations separate.

---

## 5. Key Engineering Decisions

### SQLite for Persistent Storage

SQLite was selected because the project requires persistent relational storage but does not require a separate database server.

It provides:

- structured relational data
- SQL querying
- transaction support
- foreign-key relationships
- a portable database file

The application stores its data in:

```text
data/helpdesk.db
```

### Standard Library First

The completed Task 1 implementation uses only Python standard-library modules.

This keeps the project portable and avoids unnecessary dependencies.

Core modules include:

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

### Service Layer for Business Rules

Ticket workflow rules are implemented in the service layer rather than in the CLI or database code.

This allows rules to be reused and tested independently.

### Repository Pattern

Database operations are isolated inside repository classes.

The CLI and service layers therefore do not contain raw SQL statements.

### Audit History

Important ticket changes are stored separately from the current ticket state.

This provides traceability for operations such as:

```text
CREATED
ASSIGNED
UPDATED
PRIORITY_CHANGED
STATUS_CHANGED
RESOLUTION_UPDATED
```

---

## 6. Implemented Functionality

The completed application supports:

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
- Close resolved tickets

The implemented ticket lifecycle is:

```text
OPEN
  ↓
IN_PROGRESS
  ↓
RESOLVED
  ↓
CLOSED
```

---

## 7. Reliability and Validation

The application validates ticket information before persistence.

Validation covers areas such as:

- ticket-number format
- title
- description
- requester information
- email format
- category
- priority
- status
- assignment
- resolution

Business rules also prevent invalid operations.

For example:

- a ticket cannot be resolved without a resolution
- a ticket cannot be closed before it is resolved
- closed tickets cannot be edited
- invalid status transitions are rejected

Application-specific exceptions are used so expected failures can be handled cleanly.

---

## 8. Logging and Operational Visibility

Runtime logging is configured through the application configuration.

The log file is stored at:

```text
logs/helpdesk.log
```

The application records events including startup, initialization, CLI activity, and handled operational failures.

Rotating file logging is used to prevent unlimited log-file growth.

---

## 9. Testing Outcome

Automated unit and integration testing was performed during development.

Final verified automated result:

```text
46/46 tests passed
```

Detailed test commands, coverage areas, and manual QA evidence are documented separately in:

```text
docs/TESTING.md
```

The full project was also syntax-checked and the application was started and exited successfully after the final test runs.

---

## 10. Engineering Challenges

### PowerShell Command Quoting

A database-inspection command initially failed because of PowerShell quoting behavior.

The command was corrected and the SQLite schema was then successfully inspected.

### Integration Test File Editing

During development, a partial test-file replacement temporarily caused the test runner to report:

```text
Ran 0 tests
```

The complete integration-test file was restored, after which all repository tests executed successfully again.

### Optional Database ID Type

The editor correctly identified that a newly created ticket ID is typed as potentially `None` before persistence.

The test was improved to explicitly verify that an ID exists before using it for retrieval.

These issues were resolved during development rather than ignored or suppressed.

---

## 11. Final Verified Outcome

The completed Task 1 application has been verified for:

- configuration loading
- SQLite connection
- schema creation
- ticket persistence
- ticket retrieval
- ticket listing
- ticket searching
- ticket updates
- technician assignment
- priority changes
- controlled status transitions
- resolution handling
- ticket closure
- audit history
- input validation
- application logging
- exception handling
- application startup
- clean application exit

Automated verification at the time of this report:

```text
Unit Tests        : 24/24 PASS
Integration Tests : 22/22 PASS
Total             : 46/46 PASS
```

---

## 12. Current Limitations

The completed Task 1 currently does not include:

- user authentication
- role-based authorization
- web interface
- REST API
- external email notifications
- scheduled processing
- overdue-ticket automation
- automated reporting
- multi-user network deployment

These capabilities are not presented as completed features.

---

## 13. Future Improvements

Future extensions could include:

- scheduled ticket reports
- overdue-ticket detection
- notification workflows
- report export
- authentication
- role-based permissions
- SLA tracking
- dashboard interface
- REST API
- multi-user deployment

Automation and quality-engineering extensions are planned separately for Week 4 Final Task 2.

---

## 14. Conclusion

The final Task 1 outcome is a working Python helpdesk ticket-management application with persistent storage, structured business logic, validation, logging, exception handling, audit history, automated testing, and supporting documentation.

The project was developed and verified incrementally so that each major component could be tested before being integrated into the final application.
