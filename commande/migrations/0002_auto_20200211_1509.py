# Generated by Django 2.2.5 on 2020-02-11 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commande', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='nom',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='prenom',
            new_name='last_name',
        ),
    ]
