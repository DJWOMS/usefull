import base64

from PIL import Image
from django.core.files.base import ContentFile
from rest_framework.exceptions import APIException


def decode_avatar(avatar):
    """Decoding avatar with base64 format to .jpg"""
    if 'data:' in avatar and ';base64,' in avatar:
        header, avatar = avatar.split(';base64,')
    data = base64.b64decode(avatar)
    return ContentFile(data)


def check_avatar(avatar, max_weight, min_size, max_size):
    """Check avatar size and weight"""
    image = Image.open(avatar)
    (width, height) = image.size
    if avatar.size > max_weight:
        raise APIException("Please upload a picture smaller than 1 MB.")

    elif width and height < min_size:
        raise APIException("Please upload a picture bigger than {}x{}.")

    elif width and height > max_size:
        raise APIException("Please upload a picture smaller than {}x{}.")
