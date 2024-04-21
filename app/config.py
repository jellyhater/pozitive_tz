import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self):
        self.db_port = int(os.getenv("DB_PORT"))
        self.server_port = int(os.getenv("SERVER_PORT"))
        self.server_host = os.getenv("SERVER_HOST")

        self.postgres_user = os.getenv("POSTGRES_USER")
        self.postgres_password = os.getenv("POSTGRES_PASSWORD")
        self.postgres_logging = os.getenv("POSTGRES_LOGGING") not in ["False", "false", 0, ""]

        self.model_path = os.getenv("MODEL_PATH")


