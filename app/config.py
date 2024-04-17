import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self):
        self.db_port = int(os.getenv("DB_PORT"))
        self.server_port = int(os.getenv("SERVER_PORT"))
