# Generated by Django 3.2.8 on 2021-10-12 08:23

import accounts.models
from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=100, unique=True, validators=[accounts.models.EmailValidator()])),
                ('nickname', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=11, unique=True, validators=[accounts.models.PhoneValidator()])),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SmsAuthentication',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('phone', models.CharField(max_length=11, primary_key=True, serialize=False, validators=[accounts.models.PhoneValidator()])),
                ('auth_number', models.CharField(max_length=4)),
                ('auth_key', models.CharField(max_length=4)),
            ],
            options={
                'db_table': 'sms_auth',
            },
        ),
    ]
