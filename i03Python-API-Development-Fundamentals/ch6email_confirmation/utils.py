from passlib.hash import pbkdf2_sha256
from itsdangerous import URLSafeTimedSerializer

from flask import current_app


def hash_password(pasword):
    return pbkdf2_sha256.hash(pasword)


def check_password(pasword, hashed):
    return pbkdf2_sha256.verify(pasword, hashed)

def generate_token(email, salt=None):
    serializer = URLSafeTimedSerializer(current_app.config.get('SECRET_KEY'))
    return serializer.dumps(email, salt=salt)


def verify_token(token, max_age=(30 * 60), salt=None):
    # 30 * 60 seconds
    serializer = URLSafeTimedSerializer(current_app.config.get('SECRET_KEY'))
    try:
        email = serializer.loads(token, max_age=max_age, salt=salt)
    except:
        return False
    return email