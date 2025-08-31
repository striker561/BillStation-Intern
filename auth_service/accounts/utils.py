from django.core.cache import cache
import uuid


def generate_reset_token(user_id):
    token = str(uuid.uuid4())
    cache.set(token, user_id, timeout=3600)
    return token


def validate_reset_token(token):
    return cache.get(token)
