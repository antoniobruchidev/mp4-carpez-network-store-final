# Generated by Django 5.1.2 on 2024-12-10 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='friendly_tag',
            field=models.CharField(default='', max_length=16, unique=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='tag',
            field=models.CharField(default='', max_length=10, unique=True),
        ),
    ]
