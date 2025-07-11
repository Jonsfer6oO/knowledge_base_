# knowledge_base

Database microservice for the "Knowledge Base" website. Consists of 6 tables:
Accounts table (login, password);
Users table;
Articles table;
Administrators table;
Errors table;
Blacklist table;

For interaction with the database: SQLalchemy.
REST API: FastAPI

## Getting started

`uvicorn main:app --reload`
