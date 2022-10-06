# Generated by Django 4.0 on 2022-08-29 05:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sssauth', '0003_alter_myuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='username',
            field=models.CharField(help_text='Required. Address in the format containing "-" are also allowed.', max_length=45, unique=True, validators=[django.core.validators.MinLengthValidator(39), django.core.validators.RegexValidator('^[a-zA-Z0-9]*$')], verbose_name='address'),
        ),
    ]
