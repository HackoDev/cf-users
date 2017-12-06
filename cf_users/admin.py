from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Profile
from cf_core.admin import ModerationNoteInLine, BaseModerationModelAdmin


class UserAdmin(BaseUserAdmin):

    fieldsets = (
        (None, {'fields': ('email', 'password', ('first_name', 'last_name'))}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Additions'), {'fields': ('is_subscribed',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'last_login', 'date_joined',
                    'is_active', 'is_staff')
    list_display_links = list_display
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name', 'middle_name')
    ordering = ('date_joined',)
    filter_horizontal = ('groups', 'user_permissions',)
    readonly_fields = ('date_joined',)


class ProfileAdmin(BaseModerationModelAdmin):

    list_filter = ('base_type',)
    list_display = ('get_full_name', 'get_avatar_preview', 'get_email',
                    'base_type', 'get_is_available')
    list_display_links = list_display
    readonly_fields = ('get_avatar_preview', )

    def get_avatar_preview(self, obj):
        if obj.avatar:
            return '<img src="{path}"/>'.format(path=obj.get_avatar_preview())
        return '-'
    get_avatar_preview.short_description = _('avatar')
    get_avatar_preview.allow_tags = True

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    def get_email(self, obj):
        return obj.user.email

    def get_is_available(self, obj):
        if obj.base_type == Profile.TYPE_CHOICES.REGULAR:
            return _('regular user')
        return obj.get_is_available_display()

    get_is_available.short_description = _('moderation status')

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProfileAdmin, self).get_form(request, obj=None, **kwargs)
        if obj and obj.base_type == 'REGULAR':
            form.base_fields['avatar'].required = False
        return form

    inlines = [
        ModerationNoteInLine
    ]


class ReferralUserAdmin(BaseModerationModelAdmin):

    inlines = [
        ModerationNoteInLine
    ]


class ProjectSubscriptionAdmin(admin.ModelAdmin):

    list_display = ('project', 'email')
    list_display_links = list_display


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
