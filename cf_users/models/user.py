import hashlib

from django.db.models.signals import post_save
from django.conf import settings
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .profile import Profile
from ..tasks import send_email_message

__all__ = [
    'User',
    'UserManager'
]


def handle_after_create_user(**kwargs):
    if not Profile.objects.filter(user=kwargs['instance']).exists():
        Profile.objects.create(user=kwargs['instance'])


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not email and not extra_fields.get('username', None):
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField("имя", max_length=512, default='')
    last_name = models.CharField("фамилия", max_length=512, default='')
    middle_name = models.CharField("отчество", max_length=512,
                                   default='')
    email = models.EmailField("email", db_index=True, unique=True)
    phone_number = PhoneNumberField("номер телефона", db_index=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return '{first_name} {last_name}'.format(
            first_name=self.first_name,
            last_name=self.last_name
        ).strip()

    def get_short_name(self):
        if self.first_name and self.last_name:
            return '{first_name} {last_name_char}.'.format(
                first_name=self.first_name,
                last_name_char=self.last_name[0]
            ).title()
        if self.first_name:
            return self.first_name.title()
        if self.last_name:
            return self.last_name.title()
        return ''

    def get_initials(self):
        if self.first_name and self.last_name:
            return '{}{}'.format(
                self.first_name[0],
                self.last_name[0]
            )

    def get_registration_token(self):
        token_str = 'SaltString{id}{email}{date}'.format(
            id=self.id,
            email=self.email,
            date=self.date_joined.timestamp()
        )
        hash_obj = hashlib.sha256(token_str.encode('utf-8'))
        return hash_obj.hexdigest()

    def get_password_recover_token(self):
        pattern_str = 'SaltString{id}{email}{date}{first_name}{last_name}'\
                      '{last_login}'
        token_str = pattern_str.format(
            id=self.id,
            email=self.email,
            date=self.date_joined.timestamp(),
            first_name=self.first_name,
            last_name=self.last_name,
            last_login=self.last_login.timestamp() if self.last_login else None
        )
        hash_obj = hashlib.sha256(token_str.encode('utf-8'))
        return hash_obj.hexdigest()

    def send_email(self, subject, html, text):
        send_email_message.delay(self.email, subject, html, text)

    class Meta:
        abstract = True


class User(AbstractUser):
    is_subscribed = models.BooleanField("согласие на подписку", default=False)

    REQUIRED_FIELDS = ['first_name', 'last_name']

    @classmethod
    def autocomplete_search_fields(cls):
        return 'email', 'first_name', 'last_name'

    def get_referral_link(self):
        """
        Генерация реферальной ссылки пользователя.
        """
        return '{url}?{param_name}={user_id}'.format(
            url=reverse('dashboard:referral-user'),
            param_name=settings.REFERRAL_PARAM_NAME,
            user_id=self.id
        )

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"


post_save.connect(handle_after_create_user, sender=User)
