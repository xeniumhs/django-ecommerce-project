# Generated by Django 5.1.4 on 2025-01-24 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='product_images/'),
        ),
    ]
