import redis
from config import Config
from flask import current_app


class RedisClient:
    BLACKLIST = set()
    
    def __init__(self) -> None:
        self.url = current_app.config['REDIS_URL']
        self.cache = redis.StrictRedis.from_url(self.url)
    
    def add_to_blacklist(self, jti):
        self.BLACKLIST.add(jti)
        self.cache.set(jti, 'true', ex=3600)
        
    def is_token_blacklisted(self, jti) -> bool:
        exists = False
        try:
            exists = self.cache.exists(jti) == 1
        except Exception:
            ...
        return jti in self.BLACKLIST or exists
