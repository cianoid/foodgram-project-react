# Generated by Django 2.2.27 on 2022-02-22 13:28

import core.images
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingridients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название ингридиента')),
                ('measurement_unit', models.CharField(max_length=32, verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'ингридиент',
                'verbose_name_plural': 'ингридиенты',
            },
        ),
        migrations.CreateModel(
            name='ReceiptIngridientsRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField()),
                ('ingridient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='receipts.Ingridients')),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Имя тега')),
                ('color', models.CharField(help_text='Введите код цвета в шестнадцетиричном формате', max_length=7, validators=[django.core.validators.RegexValidator(code='wrong_hex_code', message='Неправильный формат цвета', regex='^#[a-eA-E0-9]{6}$')], verbose_name='Цвет')),
                ('slug', models.SlugField(help_text='Введите slug тега', verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'тег',
                'verbose_name_plural': 'теги',
            },
        ),
        migrations.CreateModel(
            name='Receipts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('image', sorl.thumbnail.fields.ImageField(upload_to=core.images.upload_to, verbose_name='Картинка')),
                ('name', models.CharField(max_length=200, verbose_name='Название рецепта')),
                ('text', models.TextField(verbose_name='Описание рецепта')),
                ('cooking_time', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator], verbose_name='Время приготовления')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='receipts', to=settings.AUTH_USER_MODEL, verbose_name='Автор рецепта')),
                ('ingridients', models.ManyToManyField(related_name='ingridients', through='receipts.ReceiptIngridientsRelation', to='receipts.Ingridients', verbose_name='Ингридиенты')),
                ('tags', models.ManyToManyField(related_name='receipts', to='receipts.Tags', verbose_name='Теги')),
            ],
            options={
                'verbose_name': 'рецепт',
                'verbose_name_plural': 'рецепты',
            },
        ),
        migrations.AddField(
            model_name='receiptingridientsrelation',
            name='receipt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='receipts.Receipts'),
        ),
    ]
