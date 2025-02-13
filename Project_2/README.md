- FastAPI: A modern, high-performance web framework for building APIs with Python.
- Tortoise ORM: An asynchronous Object-Relational Mapper (ORM) for interacting with databases. This suggests you're using a database like PostgreSQL, MySQL, or SQLite.
- Pydantic: For data validation and serialization. TodoPost and TodoPut are likely Pydantic models.

# steps for the connecting database:

**1. First, make sure PostgreSQL is installed on your system. Then install the required Python packages:** 

```bash
pip install asyncpg tortoise-orm aerich psycopg2-binary
```

**2. Create a new PostgreSQL database:**

```bash
# Log into PostgreSQL
psql -U postgres

# Create the database
CREATE DATABASE todoapp;

-- Verify the database was created (optional)
\l

-- Connect to the new database
\c todoapp

```

- You can then quit the PostgreSQL CLI using:
```bash
\q
```


**3. Create a .env file in your project root with your PostgreSQL credentials:**

```bash
DB_CONNECTION=postgres://postgres:yourpassword@localhost:5432/todoapp
```
- Replace postgres with your PostgreSQL username, yourpassword with your actual password, and todoapp with your database name.

- Please update your .env file with this new connection string. Here's what changed example: '# became %23' , '& became %26'


**4. Set up Aerich for migrations. We already have the db_config.py file set up correctly. Now initialize Aerich:**

```bash
# Initialize aerich
aerich init -t db_config.ORM

# Create first migration
aerich init-db

```
**5. Then try running your FastAPI application:**

```bash
uvicorn todo.main:app --reload
```

