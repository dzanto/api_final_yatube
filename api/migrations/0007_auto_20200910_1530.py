# Generated by Django 3.1.1 on 2020-09-10 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_group_description'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together=set(),
        ),
    ]
