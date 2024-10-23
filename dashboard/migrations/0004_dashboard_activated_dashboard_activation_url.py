# Generated by Django 5.1.2 on 2024-10-23 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_dashboard_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashboard',
            name='activated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='dashboard',
            name='activation_url',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]