# Generated by Django 2.1.5 on 2019-02-13 23:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20190209_1929'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='question_text',
            new_name='text',
        ),
    ]
