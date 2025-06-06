"""
Common utilities for the USPTO Patents Processing Python project

This module provides common utilities for the USPTO Patents Processing Python project. It includes functions to load configuration files, load application keys, and load modules dynamically.

Todos:
- Add more functions for common utilities.
- Add more error handling and logging.
- Add more documentation.
- Add monitoring and alerting
"""
import asyncpg
import psycopg2
import urllib.parse

class DbConnectionHelpers:
    @staticmethod
    def connect_psycopg2(pg_params: dict) -> psycopg2.extensions.connection:
        conn_params = pg_params.copy()
        conn_params.pop('database', None)  # Remove 'database' key if it exists
        conn = psycopg2.connect(**conn_params)
        return conn

    @staticmethod
    async def connect_asyncpg(pg_params: dict) -> asyncpg.connection.Connection:
        conn_params = pg_params.copy()
        conn_params.pop('dbname', None)  # Remove 'dbname' key if it exists
        conn = await asyncpg.connect(**conn_params)
        return conn
    
    @staticmethod
    def pg_params_to_sqlalchemy(pg_params: dict) -> str:
        """
        Convert psycopg2 connection parameters to an SQLAlchemy PostgreSQL URL string.
        
        Expected pg_params keys:
        - user: database username
        - password: database password
        - host: database host (default: 'localhost')
        - port: database port (optional)
        - dbname or database: database name
        - Any additional keys (e.g., sslmode) will be added as query parameters.
        
        Example:
        pg_params = {
            "user": "myuser",
            "password": "mypassword",
            "host": "localhost",
            "port": "5432",
            "dbname": "mydatabase",
            "sslmode": "prefer"
        }
        connection_url = pg_params_to_sqlalchemy(pg_params)
        # connection_url: "postgresql://myuser:mypassword@localhost:5432/mydatabase?sslmode=prefer"
        """
        user = pg_params.get("user", "")
        password = pg_params.get("password", "")
        host = pg_params.get("host", "localhost")
        port = pg_params.get("port", "")

        # Accept either 'dbname' or 'database' for the database name.
        dbname = pg_params.get("dbname") or pg_params.get("database", "")
        
        # Prepare any extra parameters (sslmode, etc.)
        extra_params = {
            k: v for k, v in pg_params.items()
            if k not in {"user", "password", "host", "port", "dbname", "database"}
        }
        
        # URL encode user and password
        user_enc = urllib.parse.quote_plus(user)
        password_enc = urllib.parse.quote_plus(password)
        
        # Start building the connection URL
        url = f"postgresql://{user_enc}:{password_enc}@{host}"
        if port:
            url += f":{port}"
        url += f"/{dbname}"
        
        if extra_params:
            url += "?" + urllib.parse.urlencode(extra_params)
        
        return url
