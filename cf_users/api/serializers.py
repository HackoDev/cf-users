from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from cf_users.models import Profile, User


class UserSerializer(serializers.ModelSerializer):
    total_projects = serializers.IntegerField(
        source='get_total_project_counter',
        read_only=True
    )

    sponsor_project_counter = serializers.IntegerField(
        source='get_sponsor_project_counter',
        read_only=True
    )

    full_name = serializers.CharField(
        source='get_full_name',
        read_only=True
    )

    short_name = serializers.CharField(
        source='get_short_name',
        read_only=True
    )

    class Meta:
        model = User
        fields = (
            'email',
            'is_staff',
            'is_active',
            'short_name',
            'date_joined',
            'first_name',
            'last_name',
            'middle_name',
            'full_name',
            'total_projects',
            'sponsor_project_counter',
            'referral_link'
        )
        extra_kwargs = {
            'email': {'read_only': True},
            'ref_points': {'read_only': True},
            'is_active': {'read_only': True},
            'is_staff': {'read_only': True},
            'date_joined': {'read_only': True},
            'referral_link': {'read_only': True, 'source': 'get_referral_link'}
        }


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    middle_name = serializers.CharField(write_only=True, required=False)
    small_avatar = serializers.SerializerMethodField(read_only=True)

    def get_small_avatar(self, obj):
        return obj.get_avatar_preview()

    def update(self, instance, validated_data):

        user_data = validated_data.pop('user', {})
        for field in ['first_name', 'last_name', 'middle_name']:
            if field in validated_data:
                user_data.update({field: validated_data.get(field)})
        for field, value in user_data.items():
            setattr(instance.user, field, value)

        instance.user.save(update_fields=user_data.keys())
        return super(ProfileSerializer, self).update(instance, validated_data)

    class Meta:
        model = Profile
        fields = '__all__'
        extra_kwargs = {
            'is_available': {'read_only': True},
            'avatar': {'required': False, 'allow_null': False},
            'base_type': {'required': False},
            'ref_points': {'read_only': True},
            'contact_phone': {'required': False},
            'contact_email': {'required': False}
        }


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserChangePasswordSerializer, self).__init__(*args, **kwargs)

    def validate(self, attrs):
        if attrs['password1'] != attrs['password1']:
            raise serializers.ValidationError({
                'password1': _("password didn't match"),
                'password2': _("password didn't match")
            })
        if not self.user.check_password(attrs['old_password']):
            raise serializers.ValidationError({
                'old_password': _("current password isn't valid")
            })
        return attrs['password1']

    def update(self, *args, **kwargs):
        self.user.set_password(self.validated_data)
        self.user.save()
        return self.user


class ShareRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({
                'email': _("This email already registered")
            })
        return attrs


class ProfileListSerializer(serializers.ModelSerializer):
    small_avatar = serializers.SerializerMethodField(read_only=True)

    def get_small_avatar(self, obj):
        return obj.get_avatar_preview()

    class Meta:
        model = Profile
        fields = (
            'id', 'title', 'notes', 'avatar', 'web_link', 'small_avatar'
        )
