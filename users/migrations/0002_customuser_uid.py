# Generated by Django 5.1 on 2024-09-28 13:03

import users.models.user
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='uid',
            field=models.BigIntegerField(default=users.models.user.generate_uid, editable=False, unique=True),
        ),
    ]
