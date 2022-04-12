# Generated by Django 2.2.27 on 2022-03-30 05:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_auto_20220311_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(help_text='Введите код цвета в шестнадцетиричном формате (#ABCDEF)', max_length=7, validators=[django.core.validators.RegexValidator(code='wrong_hex_code', message='Неправильный формат цвета', regex='^#[a-fA-F0-9]{6}$')], verbose_name='Цвет'),
        ),
    ]
