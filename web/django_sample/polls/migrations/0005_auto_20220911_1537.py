# Generated by Django 2.2.28 on 2022-09-11 15:37

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20190315_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 11, 15, 37, 29, 14146, tzinfo=utc), verbose_name='date published'),
        ),
    ]