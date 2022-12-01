from django.conf import settings
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser as DjangoAbstractUser
from django.contrib.auth.models import BaseUserManager
from django.utils.crypto import get_random_string

from smart_tracker.library import get_file_path, encode


class CustomUserManager(BaseUserManager):

    """ Define a model manager for User model with no username field."""

    def _create_user(self, phone, password=None, **extra_fields):
        """Create and save a User with the given phone and password."""
        if not phone:
            raise ValueError('The given phone must be set')
        phone = self.normalize_email(phone)
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password=None, **extra_fields):
        """Create and save a SuperUser with the given phone and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)


class ProjectUser(DjangoAbstractUser):
    """
    User Model.
    Attribs:
        user (obj): Django user model.
        phone(str): phone number of the user.
    """
    username = None
    phone = models.CharField(max_length=20, unique=True)
    dob = models.DateField(default=None, null=True, blank=True)
    image = models.ImageField(
        default=None, upload_to=get_file_path, null=True, blank=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        """Object name in django admin."""
        return '%s : %s' % (self.name, self.id)

    @property
    def name(self):
        """Get user full name."""
        return '%s' % (self.get_full_name())

    @property
    def image_url(self):
        """Get file url ."""
        try:
            return self.image.url
        except:
            return None

    def issue_access_token(self):
        """Function to get or create user access token."""
        token, created = AccessToken.objects.get_or_create(user=self)
        self.last_login = timezone.now()
        self.save()
        return token.key

    @property
    def idencode(self):
        """To return encoded id."""
        return encode(self.id)


class AccessToken(models.Model):
    """
    The default authorization model.

    This model is overriding the DRF Token
    Attribs:
        user(obj): user object
        Key(str): token
        created(datetime): created date and time.
    """
    user = models.ForeignKey(
        ProjectUser, related_name='auth_token', on_delete=models.CASCADE)
    key = models.CharField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Function to return value in django admin."""
        return self.key

    def save(self, *args, **kwargs):
        """Overriding the save method to generate key."""
        if not self.key:
            self.key = self.generate_unique_key()
        return super(AccessToken, self).save(*args, **kwargs)

    def generate_unique_key(self):
        """Function to generate unique key."""
        key = get_random_string(settings.ACCESS_TOKEN_LENGTH)
        if AccessToken.objects.filter(key=key).exists():
            self.generate_unique_key()
        return key

    def refresh(self):
        """Function  to change token."""
        self.key = self.generate_unique_key()
        self.save()

    @property
    def idencode(self):
        """To return encoded id."""
        return encode(self.id)
