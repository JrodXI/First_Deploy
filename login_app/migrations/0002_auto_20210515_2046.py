# Generated by Django 2.2 on 2021-05-15 20:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trip',
            old_name='date_end',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='trip',
            old_name='date_start',
            new_name='start_date',
        ),
    ]
