# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-06 08:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import easy_thumbnails.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('cf_users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'profile', 'verbose_name_plural': 'profiles'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.RemoveField(
            model_name='profile',
            name='lfb',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='okved',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='rcf',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='rcg',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='rco',
        ),
        migrations.AlterField(
            model_name='profile',
            name='accountant_full_name',
            field=models.CharField(blank=True, default='', max_length=1048, verbose_name='accountant full name'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='approved_at',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='approved at'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='approved_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profiles_granted_list', to=settings.AUTH_USER_MODEL, verbose_name='approved by'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=easy_thumbnails.fields.ThumbnailerImageField(default='', upload_to='', verbose_name='avatar'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='base_type',
            field=models.CharField(choices=[('REGULAR', 'regular'), ('NCO', 'non commerce organization'), ('ORGANIZATION', 'LLO/OSC')], default='REGULAR', max_length=32, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bic',
            field=models.CharField(blank=True, default='', max_length=512, verbose_name='bic'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='checking_account',
            field=models.CharField(blank=True, default='', max_length=512, verbose_name='checking account'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='company_name',
            field=models.CharField(blank=True, default='', max_length=1048, verbose_name='company name'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='contact_email',
            field=models.EmailField(blank=True, default='', max_length=254, verbose_name='contact email'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='contact_phone',
            field=models.CharField(blank=True, default='', max_length=22, verbose_name='contact phone number'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='correspondent_account',
            field=models.CharField(blank=True, default='', max_length=512, verbose_name='correspondent account'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='head_full_name',
            field=models.CharField(blank=True, default='', max_length=1048, verbose_name='head full name'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='is_available',
            field=models.NullBooleanField(choices=[(None, 'wait'), (True, 'allowed'), (False, 'banned')], default=None, verbose_name='moderation status'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='legal_address',
            field=models.TextField(blank=True, default='', verbose_name='legal person'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='name_bank',
            field=models.CharField(blank=True, default='', max_length=2048, verbose_name='bank'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='notes',
            field=models.TextField(blank=True, default='', verbose_name='notes'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='postal_address',
            field=models.TextField(blank=True, default='', verbose_name='postal address'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='process_status',
            field=models.CharField(blank=True, choices=[('', 'wait'), ('CHECK', 'checking'), ('APPLY', 'applying')], default='', max_length=8, verbose_name='moderation status'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='rce',
            field=models.CharField(blank=True, default='', max_length=512, verbose_name='All-Russian classifier of enterprises and organizations'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='ref_points',
            field=models.IntegerField(default=0, help_text='approve referral point', verbose_name='referral points'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='rrc',
            field=models.CharField(blank=True, default='', max_length=512, verbose_name='reason code of registration'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='tin',
            field=models.CharField(blank=True, default='', max_length=32, verbose_name='taxpayer identification number'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='title',
            field=models.CharField(blank=True, default='', max_length=512, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='web_link',
            field=models.URLField(blank=True, default='', verbose_name='site url'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(default='', max_length=512, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_subscribed',
            field=models.BooleanField(default=False, verbose_name='subscribed'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(default='', max_length=512, verbose_name='last name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='middle_name',
            field=models.CharField(default='', max_length=512, verbose_name='middle name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(db_index=True, max_length=128, verbose_name='phone number'),
        ),
    ]
