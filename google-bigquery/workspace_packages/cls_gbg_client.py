from google.cloud import bigquery
from threading import Lock

from cls_env_config import EnvConfigSingleton as EnvConfig

class GBGClientHelperSingleton:
    _instance = None
    _lock = Lock()

    def __new__(cls, key_file_path=None):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(GBGClientHelperSingleton, cls).__new__(cls)
                if key_file_path:
                    cls._instance.client = bigquery.Client.from_service_account_json(key_file_path)
                else:
                    raise ValueError("A key file path must be provided to initialize GCS client.")
        return cls._instance

    def get_client(self):
        return self.client

def main():
    config = EnvConfig()

    key_file_path = config.get('GoogleCloudCredentials')['GoogleBigQuery']['keyfile_path']

    # Append the repo path to the key file path
    key_file_path = f"{config.repo_root}/{key_file_path}"

    print(f"Using key file: {key_file_path}")

    gbg_client_singleton = GBGClientHelperSingleton(key_file_path)
    gbg_client = gbg_client_singleton.get_client()

    query = "SELECT current_date() AS today"
    query_job = gbg_client.query(query)
    for row in query_job:
        print(f"Today's date is: {row['today']}")

if __name__ == '__main__':
    main()
