# Generated by Django 4.0.6 on 2022-10-12 04:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0028_addressbook'),
    ]

    operations = [
        migrations.RenameField(
            model_name='addressbook',
            old_name='statue',
            new_name='status',
        ),
    ]
