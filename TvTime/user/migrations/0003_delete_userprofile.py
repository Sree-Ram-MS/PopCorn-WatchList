# Generated by Django 4.2.1 on 2023-06-19 17:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_userprofile_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
