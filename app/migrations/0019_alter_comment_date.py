# Generated by Django 4.2.17 on 2024-12-26 18:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_alter_order_options_alter_comment_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2024, 12, 26, 21, 51, 47, 27716), verbose_name='Дата комментария'),
        ),
    ]
