from dotenv import load_dotenv
from os import getenv


load_dotenv()

class Config:
    SECRET_KEY = getenv('SECRET_KEY', 'customSecretKey')
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    JWT_SECRET_KEY = getenv('JWT_SECRET_KEY')
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    REDIS_URL = getenv("REDIS_URL", 'redis://localhost:6379/9')
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = getenv("REDIS_URL", 'redis://localhost:6379/9')
    CACHE_DEFAULT_TIMEOUT = 300
