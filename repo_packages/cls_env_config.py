import os
import json
import logging
import threading

from cls_env_tools import EnvTools

class EnvConfigSingleton:
    _instance = None
    _lock = threading.Lock()  # For thread safety

    def __new__(cls, project_root=None, additional_config=None, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(EnvConfigSingleton, cls).__new__(cls, *args, **kwargs)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self, project_root=None, additional_config=None):
        if self._initialized:
            return
            
        # Store the project_root
        self._project_root = project_root or EnvTools.find_repo_root()
        
        # Check if project_root exists and is valid
        if not self._project_root or not os.path.isdir(self._project_root):
            logging.warning(f"⚠️ Warning: Project root '{self._project_root}' is not a valid directory")
            self._project_root = os.getcwd()
            logging.warning(f"⚠️ Using current directory as fallback: {self._project_root}")
        
        # Initialize the configuration settings here
        self._load_env_config()
        
        # Load additional config if provided
        if additional_config:
            self.load_additional_config(additional_config)
            
        self._initialized = True

    def _load_env_config(self):
        hostname = EnvTools.get_hostname()

        # Load config relative to project_root
        config_path = os.path.join(self._project_root, 'config.json')
        self._config = EnvTools.load_settings(config_path) or {}

        # Load local config file if it exists which should have settings specific to the local machine
        local_config_file = os.path.join(self._project_root, f'config.{hostname}.json')
        self._local_config = EnvTools.load_settings(local_config_file)
        if self._local_config is not None:
            self._merge_dicts(self._config, self._local_config)

        # Load app keys which might be property values or a relative path to a key file
        app_keys_path = os.path.join(self._project_root, 'app_keys.json')
        self._app_keys = EnvTools.load_settings(app_keys_path)
        if self._app_keys is not None:
            self._merge_dicts(self._config, self._app_keys)

        # Set workspace root - try environment variable first, then project_root
        self._workspace_root = os.getenv('WORKSPACE_ROOT')
        if not self._workspace_root or not os.path.isdir(self._workspace_root):
            # If env variable not set or invalid, try using a config property
            config_workspace = self._config.get('workspace_root')
            if config_workspace and os.path.isdir(config_workspace):
                self._workspace_root = config_workspace
            else:
                # Use project_root as a fallback, which should be the repo root
                self._workspace_root = self._project_root
                logging.info(f"🔹 Using project root as workspace root: {self._workspace_root}")

    def _merge_dicts(self, base, updates):
        for key, value in updates.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._merge_dicts(base[key], value)
            else:
                base[key] = value

    def load_additional_config(self, config_file_path):
        """
        Load additional configuration from a JSON file and merge with existing config.
        Searches for the file in multiple locations:
        1. As provided (if absolute path)
        2. Relative to workspace_root
        3. Relative to project_root
        
        Args:
            config_file_path (str): Path to additional config file
            
        Returns:
            bool: True if config was loaded successfully, False otherwise
        """
        # If it's already an absolute path, use it directly
        if os.path.isabs(config_file_path):
            search_paths = [config_file_path]
        else:
            # Create search paths in priority order
            search_paths = []
            
            # 1. Workspace root if defined
            if self._workspace_root:
                logging.debug(f"Adding workspace_root search path: {self._workspace_root}")
                search_paths.append(os.path.join(self._workspace_root, config_file_path))
            
            # 2. Project root
            logging.debug(f"Adding project_root search path: {self._project_root}")
            search_paths.append(os.path.join(self._project_root, config_file_path))
        
        # Try each path in order
        logging.debug(f"Searching for '{config_file_path}' in: {search_paths}")

        for path in search_paths:

            if os.path.exists(path):

                additional_config = EnvTools.load_settings(path)

                if additional_config:
                    logging.info(f"🔹 Loading additional configuration from: {path}")
                    self._merge_dicts(self._config, additional_config)
                    return path # Return the path where the config was found to validate later
                else:
                    logging.warning(f"⚠️ Failed to parse configuration file: {path}")
                    # Continue trying other paths
        
        # If we get here, we couldn't find or parse any of the files
        searched_paths = "\n  - ".join(search_paths)

        logging.warning(f"⚠️ Could not find or load additional configuration file '{config_file_path}'. Searched in:\n  - {searched_paths}")

        return None

    @property
    def merged_config(self):
        return self._config

    @property
    def project_root(self):
        return self._project_root

    @property
    def workspace_root(self):
        return self._workspace_root

    def get(self, key, default=None):
        return self.merged_config.get(key, default)

    def set(self, key, value):
        self.merged_config[key] = value

    def app_key(self, app_key, key):
        return self.merged_config['keys'][app_key][key]

    def app_keys(self, app_keys):
        return self.merged_config['keys'][app_keys]

    def all_app_keys(self):
        return self.merged_config['keys']

    def get_asyncpg_params(self, server_alias, database="postgres"):
        pgSourceKey = self.merged_config['pgServers'][server_alias]
        pgsql_params = self.merged_config['pgConnStrs'][pgSourceKey][database].copy()
        pgsql_params.pop('dbname', None)  # Remove 'database' key if it exists
        #pgsql_params['password'] = self.merged_config['pgPwds'][pgSourceKey][database]['password']
        return pgsql_params

    def get_psycopg2_params(self, server_alias, database="postgres"):
        pgSourceKey = self.merged_config['pgServers'][server_alias]
        pgsql_params = self.merged_config['pgConnStrs'][pgSourceKey][database].copy()
        pgsql_params.pop('database', None)  # Remove 'database' key if it exists
        #pgsql_params['password'] = self.merged_config['pgPwds'][pgSourceKey][database]['password']
        return pgsql_params

    def get_source_psycopg2_params(self, database="postgres"):
        pgSourceKey = self.merged_config['pgServers']["source"]
        pgsql_params = self.merged_config['pgConnStrs'][pgSourceKey][database].copy()
        pgsql_params.pop('database', None)  # Remove 'database' key if it exists
        #pgsql_params['password'] = self.merged_config['pgPwds'][pgSourceKey][database]['password']
        return pgsql_params

    def get_target_psycopg2_params(self, database="postgres"):
        pgTargetKey = self.merged_config['pgServers']["target"]
        if pgTargetKey is None or pgTargetKey == '':
            raise ValueError('No targetPostgresDev key found in config.json')
        pgsql_params = self.merged_config['pgConnStrs'][pgTargetKey][database].copy()
        pgsql_params.pop('database', None)
        #pgsql_params['password'] = self._app_keys['pgPwds'][pgTargetKey][database]['password']
        return pgsql_params


# For backward compatibility
def create_env_config(project_root=None, additional_config=None):
    """
    Create an EnvConfigSingleton instance with specified parameters.
    If no parameters are provided, it works like the old behavior.
    
    Args:
        project_root (str, optional): Path to project root directory
        additional_config (str, optional): Path to additional config file
        
    Returns:
        EnvConfigSingleton: The singleton instance
    """
    return EnvConfigSingleton(project_root, additional_config)

if __name__ == "__main__":
    # Set up logging to see the warnings
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    # Reset the singleton for testing purposes (normally you wouldn't do this)
    EnvConfigSingleton._instance = None
    
    print("\n=== Test 1: Default initialization ===")
    config1 = EnvConfigSingleton()
    print(f"Project root: {config1.project_root}")
    
    # Reset the singleton for testing purposes
    EnvConfigSingleton._instance = None
    
    print("\n=== Test 2: With non-existent additional config ===")
    # This should trigger warning about additional_config.json not found
    config2 = EnvConfigSingleton(EnvTools.find_repo_root(), additional_config="additional_config.json")
    
    print("\n=== Test 3: Manually loading non-existent config ===")
    # This should trigger warning about custom_settings.json not found
    config2.load_additional_config("custom_settings.json")
    
    print("\n=== Test 4: After modifications ===")
    # Setting a value to demonstrate it's the same instance
    config2.set("NEW_SETTING", "value")
    print(f"NEW_SETTING: {config2.get('NEW_SETTING')}")
    
    # Reset one more time to test backward compatibility
    EnvConfigSingleton._instance = None
    
    print("\n=== Test 5: With backward compatibility helper ===")
    config3 = create_env_config(additional_config="another_non_existent_config.json")
    print(f"NEW_SETTING: {config3.get('NEW_SETTING')}") # Should be None since we reset
    
    if (config3.get("keys") is not None):
        print("\nKeys available")
    else:
        print("\nNo keys in configuration")
        
    print("\nConfiguration keys:", list(config3.merged_config.keys()))
