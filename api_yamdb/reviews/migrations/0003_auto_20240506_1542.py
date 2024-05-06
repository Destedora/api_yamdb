# Generated by Django 3.2 on 2024-05-06 12:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, db_index=True, help_text='Дата публикации отзыва/комментария', verbose_name='Дата публикации'),
        ),
        migrations.AlterField(
            model_name='review',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, db_index=True, help_text='Дата публикации отзыва/комментария', verbose_name='Дата публикации'),
        ),
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.PositiveSmallIntegerField(db_index=True, help_text='Укажите рейтинг произведения от 1 до 10', validators=[django.core.validators.MinValueValidator(1, message='Рейтинг ниже допустимого значения: 1'), django.core.validators.MaxValueValidator(10, message='Рейтинг выше допустимого значения: 10')], verbose_name='Рейтинг'),
        ),
    ]
