from django.conf import settings
from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from model_utils import Choices

from cf_core.models import BaseModerateModel
from cf_core.managers import PROFILE_TYPE_CHOICES

__all__ = [
    'Profile'
]


class Profile(BaseModerateModel):

    TYPE_CHOICES = PROFILE_TYPE_CHOICES

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name="пользователь",
        related_name='profile'
    )

    contact_phone = models.CharField(
        verbose_name="контактный номер телефона",
        max_length=22,
        default='',
        blank=True
    )

    contact_email = models.EmailField(
        verbose_name="контактный email",
        default='',
        blank=True
    )

    title = models.CharField(
        verbose_name="название организации",
        max_length=512,
        default='',
        blank=True
    )

    base_type = models.CharField(
        verbose_name="тип профиля",
        default=TYPE_CHOICES.REGULAR,
        choices=TYPE_CHOICES,
        max_length=32
    )

    ref_points = models.IntegerField(
        verbose_name="баллы реферальной системы",
        default=0,
        help_text="баллы заработаные пользователем по реферальной системе"
    )

    avatar = ThumbnailerImageField("логотип", default='')
    notes = models.TextField("о себе", default='', blank=True)
    web_link = models.URLField("сайт", default="", blank=True)

    company_name = models.CharField(
        "название компании",
        max_length=1048,
        default='',
        blank=True
    )

    legal_address = models.TextField("юридический адрес", blank=True,
                                     default='')

    postal_address = models.TextField("почтовый адрес", default='', blank=True)

    tin = models.CharField(
        "идентификационный номер налогоплательщика",
        max_length=32,
        default='',
        blank=True
    )

    rrc = models.CharField(
        "код причины регистрации",
        max_length=512,
        default='',
        blank=True
    )

    rce = models.CharField(
        "общероссийский классификатор предприятий и организаций",
        max_length=512,
        default='',
        blank=True,
    )

    rcg = models.CharField(
        "общероссийский классификатор органов государственной власти и "
        "управления",
        max_length=512,
        default='',
        blank=True
    )

    rco = models.CharField(
        "общероссийский классификатор объектов "
        "административно-территориального деления",
        max_length=512,
        default='',
        blank=True
    )

    okved = models.CharField(
        "ОКВЭД",
        max_length=512,
        default='',
        blank=True
    )

    rcf = models.CharField(
        "общероссийский классификатор организационно-правовых форм",
        max_length=512,
        default='',
        blank=True
    )

    lfb = models.CharField(
        "организационно-правовые формы хозяйствующих субъектов",
        max_length=512,
        default='',
        blank=True
    )

    name_bank = models.CharField(
        verbose_name="наименование банка",
        max_length=2048,
        default='',
        blank=True
    )

    checking_account = models.CharField(
        verbose_name="рассчетный счет",
        max_length=512,
        default='',
        blank=True
    )

    correspondent_account = models.CharField(
        verbose_name="корреспондентский счет",
        max_length=512,
        default='',
        blank=True
    )

    bic = models.CharField("БИК банка", max_length=512, default='', blank=True)

    head_full_name = models.CharField(
        "полное имя руководителя",
        max_length=1048,
        default='',
        blank=True
    )

    accountant_full_name = models.CharField(
        "ФИО бухгалтера",
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
        verbose_name = "профиль"
        verbose_name_plural = "профили"
