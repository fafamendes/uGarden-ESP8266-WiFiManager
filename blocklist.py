from os import environ
from redis import Redis
from dotenv import load_dotenv

load_dotenv()

url = ''

r = Redis.from_url(environ['REDIS_URL'])


class BLOCKLIST():

  def add_to_blocklist(jti):
    """Add a JTI to the blocklist"""
    r.set(jti, "", ex=3600)

  def get_from_blocklist(jti):
    """Check if a JTI is in the blocklist"""
    return r.get(jti)
