# Generated by Django 5.1 on 2024-09-27 16:37

import django.core.validators
import shop.models.shop
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Shop ID')),
                ('shop_name', models.CharField(blank=True, max_length=50, verbose_name='Shop Name')),
                ('description', models.TextField(blank=True, help_text='A brief description of the shop.', null=True)),
                ('follower_count', models.PositiveIntegerField(default=0, verbose_name='Followers Count')),
                ('legal_id', models.FileField(blank=True, help_text='Upload a legal ID for shop owner verification. (Allowed Types: ".pdf", ".jpg", ".jpeg", ".png")', null=True, upload_to=shop.models.shop.legal_id_upload_to, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])], verbose_name='Legal ID')),
                ('verification_document', models.FileField(blank=True, help_text='Upload a PDF document for shop verification. (e.g., DTI Permit)', null=True, upload_to=shop.models.shop.document_upload_to, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name='Verification Document')),
                ('is_active', models.BooleanField(default=False, help_text='Indicates whether the shop is verified and active.', verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified At')),
            ],
            options={
                'verbose_name': 'Shop',
                'verbose_name_plural': 'Shops',
                'ordering': ['-created_at', '-modified_at'],
            },
        ),
        migrations.CreateModel(
            name='ShopFollower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_followed', models.DateTimeField(auto_now_add=True, verbose_name='Date Followed')),
            ],
            options={
                'ordering': ['-date_followed'],
            },
        ),
    ]
