import logging
import threading
import psycopg2
import asyncpg

from datetime import datetime
from venv import logger

from cls_db_helpers import DbConnectionHelpers

class DbRepositorySingleton:
    _instance = None
    _lock = threading.Lock()  # Lock object to ensure thread safety

    def __new__(cls, *args, **kwargs):
        """
        Ensures only one instance of the class is created, even in a multithreaded environment.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Double-checked locking
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, db_params, db_type='psycopg2'):
        """
        Initialize the singleton instance.
        """
        if not hasattr(self, '_initialized'):
            self.db_type = db_type
            self.pg_params = db_params
            if db_type == 'psycopg2':
                self.connection = DbConnectionHelpers.connect_psycopg2(db_params)
            elif db_type == 'asyncpg':
                self.connection = None  # asyncpg connections need to be handled asynchronously
            self._initialized = True

    @classmethod
    def cleanup(cls):
        """
        Cleanup method to reset or release resources.
        """
        with cls._lock:
            if cls._instance is not None:
                cls._instance = None

    def __del__(self):
        """
        Destructor to handle cleanup automatically if the singleton is deleted.
        """
        if self.db_type in ['psycopg2'] and self.connection:
            self.connection.close()

    async def connect_asyncpg(self, db_params):
        """
        Method to handle asyncpg connection asynchronously.
        """
        if self.db_type == 'asyncpg' and self.connection is None:
            self.connection = await asyncpg.connect(**db_params)

    def get_connection(self):
        return self.connection

# Example usage
if __name__ == "__main__":
    def create_instance(db_params, db_type):
        instance = DbRepositorySingleton(db_params, db_type)
        conn = instance.get_connection()
        if db_type == 'asyncpg':
            import asyncio
            asyncio.run(instance.connect_asyncpg(db_params))
            conn = instance.get_connection()
        print(f"Connection for {db_type}: {conn}")

    psycopg2_params = {'dbname': 'postgres', 'user': 'test_user', 'password': 'your_strong_password', 'host': 'localhost'}
    asyncpg_params = {'database': 'postgres', 'user': 'test_user', 'password': 'your_strong_password', 'host': 'localhost'}

    threads = [
        threading.Thread(target=create_instance, args=(psycopg2_params, 'psycopg2')),
        threading.Thread(target=create_instance, args=(asyncpg_params, 'asyncpg'))
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print("[INFO] Cleaning up the thread-safe singleton...")
    DbRepositorySingleton.cleanup()

    print("[DONE] All threads completed.")