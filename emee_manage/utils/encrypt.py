import hashlib

from django.conf import settings


def md5(dada_string):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))  # yan
    obj.update(dada_string.encode('utf-8'))
    return obj.hexdigest()
