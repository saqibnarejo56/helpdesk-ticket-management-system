\# Task 2 Performance Results



\## Objective



Measure the execution time of the Helpdesk automation workflow and verify that it completes within the defined performance threshold.



\## Test Environment



\- Application: Helpdesk Ticket Management System

\- Automation entry point: `automation.py`

\- Test file: `tests/performance/test\_automation\_performance.py`

\- Database: SQLite

\- Measurement method: Python `time.perf\_counter()`



\## Performance Test



The performance test executes the complete automation workflow through the Python interpreter and measures the elapsed execution time.



Command used:



```text

python -m unittest tests.performance.test\_automation\_performance -v

