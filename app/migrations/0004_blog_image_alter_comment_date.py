# Generated by Django 4.2.17 on 2024-12-12 15:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='image',
            field=models.FileField(default='temp.jpg', upload_to='', verbose_name='Путь к картинке'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2024, 12, 12, 18, 58, 40, 988236), verbose_name='Дата комментария'),
        ),
    ]