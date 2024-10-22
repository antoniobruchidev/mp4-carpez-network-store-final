# Generated by Django 5.1.2 on 2024-10-21 23:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('checkout', '0007_order_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('rating', models.IntegerField()),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='checkout.orderlineitem')),
            ],
        ),
    ]
