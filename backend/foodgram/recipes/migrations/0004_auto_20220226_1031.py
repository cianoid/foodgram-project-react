# Generated by Django 2.2.27 on 2022-02-26 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20220224_0407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', through='recipes.IngredientRecipeRelation', to='recipes.Ingredient', verbose_name='Ингридиенты'),
        ),
    ]
