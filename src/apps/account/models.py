from datetime import datetime,timedelta
from secrets import token_hex

from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.db import models
from django.shortcuts import reverse
from django.templatetags.static import static
from django.utils.translation import gettext as _

from .enums import UserAccessEnum,UserGenderEnum
from .managers import UserManager, AccessManager
from .validators import validate_digit_type
from apps.core.models import BaseModel


class AccessModel(BaseModel):
    ACCESSES = UserAccessEnum

    title = models.CharField(_('Access Title'),max_length=40,choices=ACCESSES.choices,default=ACCESSES.VIEWER,unique=True)
    object = AccessManager()

    class Meta:
        verbose_name = _('Access')
        verbose_name_plural = _('Accesses')

    def __str__(self):
        return self.title

    def get_title_labels(self):
        return self.get_title_display()

class UserModel(AbstractBaseUser,PermissionsMixin):
    ACCESSES = UserAccessEnum

    phone_number = models.CharField(_('Phone number'),max_length=11,unique=True)
    email = models.EmailField(_('Email'),max_length=225,null=True,blank=True)
    first_name = models.CharField(_('First name'), max_length=128,null=True,blank=True)
    last_name = models.CharField(_('Last name'), max_length=128,null=True,blank=True)
    accesses = models.ManyToManyField(verbose_name=_('Accesses'), to=AccessModel, related_name='user', blank=True)
    is_active = models.BooleanField(_('Active'),default=True)
    is_admin = models.BooleanField(_('Admin'),default=False)
    is_verified = models.BooleanField(_('Verify'), default=False)
    is_used_free_subs = models.BooleanField(_('Is used free subs'),default=False)
    token = models.CharField(_("Secret token"), max_length=64, null=True, blank=True, editable=False)
    created_at = models.DateTimeField(_('Creation time'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Update time'), auto_now=True)
    objects = UserManager()
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.phone_number

    def full_name(self):
        """Returns the user's full name."""
        return f"{self.first_name or ''} {self.last_name or ''}".strip() or _('No Name')

    def generate_token(self,byte_size=32):
        """Generates and assigns a secret token to the user."""
        self.token = token_hex(byte_size)
        self.save(update_fields=['token'])
        return self.token

    def check_token(self, token):
        """Checks if the provided token matches the user's token."""
        return self.token == token

    def last_login_within(self, days):
        """Checks if the user has logged in within the last 'n' days based on local time."""
        if self.last_login:
            local_time = timezone.localtime(self.last_login)
            return local_time >= timezone.now() - timedelta(days=days)
        return False

    @property
    def is_profile_completed(self):
        profile = self.profile
        province = profile.province
        city = profile.city
        # melli_cde = profile.melli_code
        place_name = profile.place_name

        if place_name and (province or city):
            return True
        return False

    @property
    def is_staff(self):
        """ Is the user a member of staff? """
        return self.is_admin

    @property
    def has_admin_access(self):
        """ Does the user have admin access? """
        if self.accesses.filter(title=self.ACCESSES.GENERAL_ADMIN).exists():
            return True
        return False

    def has_specific_access(self, access=None):
        """ Does the user have a specific access? """
        if self.accesses.filter(title=access).exists():
            return True
        return False

class UserProfileModel(BaseModel):
    GENDERS = UserGenderEnum

    user = models.OneToOneField(UserModel,on_delete=models.CASCADE,related_name='profile',verbose_name=_('User'))
    melli_code = models.CharField(_('Melli code'), max_length=10, validators=[validate_digit_type], null=True,
                                  blank=True)
    gender = models.CharField(_('Gender'), max_length=8, choices=GENDERS.choices, null=True, blank=True)
    date_of_birth = models.DateField(_('Date of birth'), null=True, blank=True)
    place_name = models.CharField(_('Place name'), max_length=128, null=True, blank=True)
    province = models.CharField(_('Province'), max_length=64, null=True, blank=True)
    city = models.CharField(_('City'), max_length=64, null=True, blank=True)
    image = models.ImageField(_('Picture'), upload_to='images/profiles/', null=True, blank=True)

    class Meta:
        verbose_name = _('User profile')
        verbose_name_plural = _('Users profile')

    def __str__(self):
        return f'{self.user}'

    def get_absolute_url(self):
        return reverse('account:profile_details', kwargs={'pk': self.pk})

    def get_gender_label(self):
        return self.get_gender_display()

    def get_image_url(self):
        if self.image:
            return self.image.url
        return static('images/defaults/user-profile-3.webp')

