# Generated by Django 2.2.13 on 2021-01-15 06:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='creatd_time',
            new_name='created_time',
        ),
    ]