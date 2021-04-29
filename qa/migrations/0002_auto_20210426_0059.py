# Generated by Django 3.1.7 on 2021-04-26 00:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='organization_title',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='clients_organization', to='qa.organization', to_field='title'),
        ),
    ]
