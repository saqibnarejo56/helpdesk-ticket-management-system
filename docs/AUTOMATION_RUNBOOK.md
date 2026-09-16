# Task 2 Automation Runbook

## 1. Purpose

This runbook explains how to execute, verify, and troubleshoot the Helpdesk Ticket Management System automation workflow.

The automation reads ticket data from the existing SQLite database, analyzes the tickets, and generates summary, active-ticket, and alert reports.

---

## 2. Prerequisites

Before running the automation, verify:

- Python 3 is installed.
- The project is opened from the project root directory.
- The SQLite database exists at:

```text
data/helpdesk.db
