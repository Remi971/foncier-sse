from dotenv import load_dotenv
import os
import redis
load_dotenv()

class EnvConfig:
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = int(os.getenv("REDIS_PORT"))
    REDIS_DB = int(os.getenv("REDIS_DB"))
    REDIS_CHANNEL = os.getenv("REDIS_CHANNEL")
    BASE_URL = os.getenv("BASE_URL")

env = EnvConfig()

class Publisher:
    def __init__(self):
        self.r = redis.Redis(host=env.REDIS_HOST, port=env.REDIS_PORT, db=env.REDIS_DB)
        self.channel = env.REDIS_CHANNEL

    def publish(self, message):
        self.r.publish(self.channel, message)
        
    def subscribe(self):
        pubsub = self.r.pubsub()
        pubsub.subscribe(self.channel)
        return pubsub