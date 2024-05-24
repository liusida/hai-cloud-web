from dotenv import load_dotenv
load_dotenv()  # This loads the environment variables from `.env`.

import os
import psycopg2
from psycopg2 import sql
import django
from django.conf import settings
from django.core.management import execute_from_command_line

def configure_django():
    """Configure Django settings."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hai_server.settings')
    django.setup()

def run_migrations():
    """Run Django migrations."""
    execute_from_command_line(['manage.py', 'migrate'])

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
            # Check if the user already exists
            cur.execute(sql.SQL("SELECT 1 FROM pg_roles WHERE rolname = %s;"), [username])
            user_exists = cur.fetchone() is not None

            if not user_exists:
                # Create user command
                cur.execute(sql.SQL("CREATE USER {} WITH PASSWORD %s;").format(
                    sql.Identifier(username)), [password])

                # Grant privileges (optional, adjust as needed)
                cur.execute(sql.SQL("ALTER USER {} WITH CREATEDB;").format(
                    sql.Identifier(username)))

            # Drop database command
            cur.execute(sql.SQL("DROP DATABASE IF EXISTS {};").format(
                sql.Identifier(database_name)))
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

def create_superuser():
    """Create a Django superuser."""
    configure_django()
    run_migrations()
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'adminpassword')
    
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
    else:
        print(f"Superuser with username '{username}' already exists.")

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
    create_superuser()
