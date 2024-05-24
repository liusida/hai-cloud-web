from dotenv import load_dotenv
load_dotenv()  # This loads the environment variables from `.env`.

import os

import psycopg2
from psycopg2 import sql

def create_user_and_database(db_config, username, password, database_name, dryrun=True):
    """Create a new PostgreSQL user and a database, then set the user as the owner."""
    conn = None
    try:
        # Connect to the PostgreSQL database server
        conn = psycopg2.connect(**db_config)
        conn.autocommit = True  # Enable autocommit to allow database creation

        # Create a new cursor
        cur = conn.cursor()

        if not dryrun:
            # Create user command
            cur.execute(sql.SQL("CREATE USER {} WITH PASSWORD %s;").format(
                sql.Identifier(username)), [password])

            # Grant privileges (optional, adjust as needed)
            cur.execute(sql.SQL("ALTER USER {} WITH CREATEDB;").format(
                sql.Identifier(username)))

            # Create database command
            cur.execute(sql.SQL("CREATE DATABASE {} OWNER {};").format(
                sql.Identifier(database_name), sql.Identifier(username)))

        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    db_config = {
        'dbname': 'postgres',
        'user': 'postgres',
        'password': os.getenv('DATABASE_SUPER_PASSWORD'),
        'host': 'localhost'
    }
    username = os.getenv('DATABASE_USER')
    password = os.getenv('DATABASE_PASSWORD')
    database_name = os.getenv('DATABASE_NAME')  # Default to 'my_project_db' if not set in .env
    create_user_and_database(db_config, username, password, database_name, dryrun=False)
