# Generated by Django 3.1.7 on 2021-05-05 08:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0006_request_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='correspondence',
            old_name='request',
            new_name='req',
        ),
    ]