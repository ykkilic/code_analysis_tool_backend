# scripts/init_postgres.py
import psycopg2
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def init_postgres():
    # Default PostgreSQL connection parameters
    params = {
        'host': os.getenv('POSTGRES_SERVER', 'localhost'),
        'user': os.getenv('POSTGRES_USER', 'postgres'),
        'password': os.getenv('POSTGRES_PASSWORD', 'postgres'),
        'database': os.getenv('POSTGRES_DB', 'security_analysis')
    }

    try:
        # First try to connect to PostgreSQL server
        conn = psycopg2.connect(
            host=params['host'],
            user=params['user'],
            password=params['password']
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        # Check if database exists
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (params['database'],))
        exists = cur.fetchone()

        if not exists:
            print(f"Creating database {params['database']}...")
            cur.execute(f"CREATE DATABASE {params['database']}")
            print(f"Database {params['database']} created successfully!")
        else:
            print(f"Database {params['database']} already exists.")

        cur.close()
        conn.close()

        # Test connection to the new database
        conn = psycopg2.connect(
            host=params['host'],
            user=params['user'],
            password=params['password'],
            database=params['database']
        )
        conn.close()
        print("PostgreSQL connection test successful!")
        return True

    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return False

if __name__ == "__main__":
    print("Initializing PostgreSQL connection...")
    if init_postgres():
        print("PostgreSQL initialization completed successfully!")
    else:
        print("PostgreSQL initialization failed!")
        exit(1)