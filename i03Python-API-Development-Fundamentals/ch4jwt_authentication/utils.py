from passlib.hash import pbkdf2_sha256


def hash_password(pasword):
    return pbkdf2_sha256.hash(pasword)


def check_password(pasword, hashed):
    return pbkdf2_sha256.verify(pasword, hashed)