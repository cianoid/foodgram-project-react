from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from sorl.thumbnail import ImageField

from core.images import upload_to

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        'Имя тега', max_length=150)
    color = models.CharField(
        'Цвет', help_text='Введите код цвета в шестнадцетиричном формате',
        max_length=7, validators=(
            RegexValidator(
                regex='^#[a-eA-E0-9]{6}$', code='wrong_hex_code',
                message='Неправильный формат цвета'), ))
    slug = models.SlugField(
        'Slug', help_text='Введите slug тега')

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.name


class Ingridient(models.Model):
    name = models.CharField(
        'Название ингридиента', max_length=200)
    measurement_unit = models.CharField(
        'Единица измерения', max_length=32)

    class Meta:
        verbose_name = 'ингридиент'
        verbose_name_plural = 'ингридиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Receipt(models.Model):
    """Модель рецептов."""
    author = models.ForeignKey(
        User, verbose_name='Автор рецепта', on_delete=models.PROTECT,
        related_name='receipts', )
    created = models.DateTimeField(
        verbose_name='Дата создания', auto_now_add=True)
    image = ImageField(
        'Картинка', upload_to=upload_to, blank=False)
    name = models.CharField(
        'Название рецепта', max_length=200)
    text = models.TextField(
        'Описание рецепта')
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления', validators=(MinValueValidator,))
    tags = models.ManyToManyField(
        Tag, verbose_name='Теги', related_name='receipts')
    ingridients = models.ManyToManyField(
        Ingridient, verbose_name='Ингридиенты', related_name='ingridients',
        through='IngridientReceiptRelation')

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self):
        return self.name


class IngridientReceiptRelation(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)
    ingridient = models.ForeignKey(Ingridient, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField()
