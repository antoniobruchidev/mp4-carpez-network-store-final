# Generated by Django 5.1.2 on 2024-11-28 18:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0010_orderlineitem_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderlineitem',
            name='review',
        ),
    ]
