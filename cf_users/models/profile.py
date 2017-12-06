from django.conf import settings
from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField

from cf_core.models import BaseModerateModel
from cf_core.managers import PROFILE_TYPE_CHOICES

__all__ = [
    'Profile'
]


class Profile(BaseModerateModel):

    TYPE_CHOICES = PROFILE_TYPE_CHOICES

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        related_name='profile'
    )

    contact_phone = models.CharField(
        verbose_name=_('contact phone number'),
        max_length=22,
        default='',
        blank=True
    )

    contact_email = models.EmailField(
        verbose_name=_('contact email'),
        default='',
        blank=True
    )

    title = models.CharField(
        verbose_name=_('title'),
        max_length=512,
        default='',
        blank=True
    )

    base_type = models.CharField(
        verbose_name=_('type'),
        default=TYPE_CHOICES.REGULAR,
        choices=TYPE_CHOICES,
        max_length=32
    )

    ref_points = models.IntegerField(
        verbose_name=_('referral points'),
        default=0,
        help_text=_('approve referral point')
    )

    avatar = ThumbnailerImageField(verbose_name=_('avatar'), default='')
    notes = models.TextField(verbose_name=_('notes'), default='', blank=True)
    web_link = models.URLField(verbose_name=_('site url'), default="", blank=True)

    company_name = models.CharField(
        verbose_name=_('company name'),
        max_length=1048,
        default='',
        blank=True
    )

    legal_address = models.TextField(verbose_name=_('legal person'), blank=True,
                                     default='')

    postal_address = models.TextField(verbose_name=_('postal address'),
                                      default='', blank=True)

    tin = models.CharField(
        verbose_name=_('taxpayer identification number'),
        max_length=32,
        default='',
        blank=True
    )

    rrc = models.CharField(
        verbose_name=_('reason code of registration'),
        max_length=512,
        default='',
        blank=True
    )

    rce = models.CharField(
        verbose_name=_('All-Russian classifier of enterprises and organizations'),
        max_length=512,
        default='',
        blank=True,
    )

    name_bank = models.CharField(
        verbose_name=_('bank'),
        max_length=2048,
        default='',
        blank=True
    )

    checking_account = models.CharField(
        verbose_name=_('checking account'),
        max_length=512,
        default='',
        blank=True
    )

    correspondent_account = models.CharField(
        verbose_name=_('correspondent account'),
        max_length=512,
        default='',
        blank=True
    )

    bic = models.CharField(
        verbose_name=_('bic'),
        max_length=512,
        default='',
        blank=True
    )

    head_full_name = models.CharField(
        verbose_name=_('head full name'),
        max_length=1048,
        default='',
        blank=True
    )

    accountant_full_name = models.CharField(
        verbose_name=_('accountant full name'),
        max_length=1048,
        default='',
        blank=True
    )

    def __init__(self, *args, **kwargs):
        super(Profile, self).__init__(*args, **kwargs)
        self.old_base_type = getattr(self, 'base_type', None)

    def save(self, *args, **kwargs):
        adding = self._state.adding

        if not adding and self.old_base_type != self.base_type:
            self.is_available = None
            self.old_base_type = self.base_type

        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.get_full_name()

    def get_avatar_preview(self):
        if self.avatar:
            return self.avatar['preview'].url

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')
