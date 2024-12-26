# Generated by Django 4.2.17 on 2024-12-26 18:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_product_options_alter_comment_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'услуги', 'verbose_name_plural': 'услуга'},
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2024, 12, 26, 21, 11, 57, 8213), verbose_name='Дата комментария'),
        ),
    ]
