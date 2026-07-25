# Database Migration Glossary

- **AST (Abstract Syntax Tree)**: A tree representation of the abstract syntactic structure of the SQL source code.
- **DDL (Data Definition Language)**: SQL commands that define the database structure (e.g., `CREATE`, `ALTER`, `DROP`).
- **DML (Data Manipulation Language)**: SQL commands that manipulate data (e.g., `SELECT`, `INSERT`, `UPDATE`, `DELETE`).
- **CONCURRENTLY**: A PostgreSQL specific keyword used when building indexes. It allows the index to be built without locking out writes to the table.
- **Table Lock**: An exclusive lock placed on a table during a migration that prevents any reads or writes from the application, causing immediate downtime.
- **Backfill**: The process of filling in missing or default data in a newly created column in batches, rather than in a single large transaction.
