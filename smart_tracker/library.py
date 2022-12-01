import enum
from django.utils.crypto import get_random_string
from hashids import Hashids
from django.conf import settings


def get_file_path(instance, filename):
    """
    Function to get filepath for a file to be uploaded
    Args:
        instance: instance of the file object
        filename: uploaded filename

    Returns:
        path: Path of file
    """
    type = instance.__class__.__name__.lower()
    path = '%s/%s/%s:%s' % (
        type, instance.id,
        get_random_string(10), filename)

    return path


class ChoiceAdapter(enum.IntEnum):
    @classmethod
    def choices(cls):
        return ((item.value, item.name.replace("_", " ")) for item in cls)


def encode(value):
    """
    Function to  hash hid the int value.

    Input Params:
        value(int): int value
    Returns:
        hashed string.
    """
    hasher = Hashids(
        min_length=settings.HASHID_MIN_LENGTH,
        salt=settings.HASHHID_SALT)
    try:
        value = int(value)
        return hasher.encode(value)
    except:
        return None


def decode(value):
    """
    Function to  decode hash hid value.

    Input Params:
        value(str): str value
    Returns:
        int value.
    """
    hasher = Hashids(
        min_length=settings.HASHID_MIN_LENGTH,
        salt=settings.HASHHID_SALT)
    try:
        return hasher.decode(value)[0]
    except:
        return None