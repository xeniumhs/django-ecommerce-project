# Generated by Django 5.1.4 on 2025-01-27 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(default='profile_images/default.png', upload_to='profile_images/'),
        ),
    ]
