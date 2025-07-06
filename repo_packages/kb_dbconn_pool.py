from psycopg2 import pool

class PgConnPoolMgr:
    """
    Base class for database connection managers.
    Provides functionality for creating and managing connection pools.
    """
    
    def __init__(self):
        """Initialize the base connection manager."""
        self.connection_pools = {}

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close_all_pools()
        
    def initialize_pool(self, pool_name, db_config, min_conn=5, max_conn=20):
        """
        Initialize a database connection pool.
        
        Args:
            pool_name (str): Name of the pool for reference
            db_config (dict): Database configuration parameters
            min_conn (int): Minimum number of connections in the pool
            max_conn (int): Maximum number of connections in the pool
            
        Returns:
            bool: True if pool was created, False if pool already exists
        """
        if pool_name in self.connection_pools:
            return False
            
        if db_config is not None:
            self.connection_pools[pool_name] = pool.ThreadedConnectionPool(min_conn, max_conn, **db_config)
            return True
        return False
    
    def get_connection(self, pool_name):
        """
        Get a connection from a specified pool.
        
        Args:
            pool_name (str): Name of the pool to get connection from
            
        Returns:
            connection: Database connection
            
        Raises:
            RuntimeError: If the pool does not exist
        """
        if pool_name not in self.connection_pools:
            raise RuntimeError(f"Pool '{pool_name}' not initialized")
        return self.connection_pools[pool_name].getconn()
    
    def return_connection(self, pool_name, connection):
        """
        Return a connection to its pool.
        
        Args:
            pool_name (str): Name of the pool
            connection: Connection to return
            
        Raises:
            RuntimeError: If the pool does not exist
        """
        if pool_name not in self.connection_pools:
            raise RuntimeError(f"Pool '{pool_name}' not initialized")
        self.connection_pools[pool_name].putconn(connection)
    
    def close_pool(self, pool_name):
        """
        Close a specific connection pool.
        
        Args:
            pool_name (str): Name of the pool to close
            
        Returns:
            bool: True if pool was closed, False if pool doesn't exist
        """
        if pool_name in self.connection_pools:
            self.connection_pools[pool_name].closeall()
            del self.connection_pools[pool_name]
            return True
        return False
    
    def close_all_pools(self):
        """Close all connection pools."""
        for pool_name in list(self.connection_pools.keys()):
            self.close_pool(pool_name)