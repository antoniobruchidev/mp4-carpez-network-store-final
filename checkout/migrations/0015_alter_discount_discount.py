# Generated by Django 5.1.2 on 2024-12-05 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0014_discount_max_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='discount',
            field=models.IntegerField(),
        ),
    ]