# Generated by Django 5.1.2 on 2024-10-20 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0005_alter_order_stripe_pid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='stripe_pid',
            field=models.CharField(default='before migration', editable=False, max_length=32),
        ),
    ]
