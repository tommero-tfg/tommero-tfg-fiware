# Generated by Django 2.2.19 on 2021-07-03 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0007_auto_20210703_1639'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carmodel',
            name='images',
        ),
    ]
