# Generated by Django 5.2.3 on 2025-06-12 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email_verified',
        ),
    ]
