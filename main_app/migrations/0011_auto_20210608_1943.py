# Generated by Django 3.2.1 on 2021-06-08 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_auto_20210608_1938'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='labor',
            options={'ordering': ['-date']},
        ),
        migrations.AlterModelOptions(
            name='rental',
            options={'ordering': ['-start_date']},
        ),
    ]