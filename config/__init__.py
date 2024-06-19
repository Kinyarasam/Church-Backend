from dotenv import load_dotenv
from os import getenv


load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL')