import os
import uuid

from PIL import Image
from flask_uploads import extension

from passlib.hash import pbkdf2_sha256
from itsdangerous import URLSafeTimedSerializer

from flask import current_app

from extensions import image_set


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


def save_image(image, folder):
    filename = '{}.{}'.format(uuid.uuid4(), extension(image.filename))
    image_set.save(image, folder=folder, name=filename)

    filename = compress_image(filename=filename, folder=folder)

    return filename


def compress_image(filename, folder):

    file_path = image_set.path(filename=filename, folder=folder)

    image = Image.open(file_path)

    if image.mode != "RGB":
        image = image.convert("RGB")

    if max(image.width, image.height) > 1600:
        maxsize = (1600, 1600)
        image.thumbnail(maxsize)

    compressed_filename = '{}.jpg'.format(uuid.uuid4())
    compressed_file_path = image_set.path(filename=compressed_filename, folder=folder)

    image.save(compressed_file_path, optimize=True, quality=85)

    original_size = os.stat(file_path).st_size
    compressed_size = os.stat(compressed_file_path).st_size
    percentage = round((original_size - compressed_size) / original_size * 100)

    print("The file size is reduced by {}%, from {} to {}.".format(percentage, original_size, compressed_size))

    os.remove(file_path)

    return compressed_filename




