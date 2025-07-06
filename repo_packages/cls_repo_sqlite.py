import sqlite3

class SQLiteRepositorySingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Ensures only one instance of the class is created.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, db_path):
        """
        Initialize the singleton instance.
        """
        if not hasattr(self, '_initialized'):
            self.connection = sqlite3.connect(db_path)
            self._initialized = True

    @classmethod
    def cleanup(cls):
        """
        Cleanup method to reset or release resources.
        """
        if cls._instance is not None:
            cls._instance = None

    def __del__(self):
        """
        Destructor to handle cleanup automatically if the singleton is deleted.
        """
        self.connection.close()

    def get_connection(self):
        return self.connection

# Example usage
if __name__ == "__main__":
    instance = SQLiteRepositorySingleton("example.db")
    conn = instance.get_connection()
    print(f"Connection: {conn}")

    print("[INFO] Cleaning up the singleton...")
    SQLiteRepositorySingleton.cleanup()

    print("[DONE] Completed.")