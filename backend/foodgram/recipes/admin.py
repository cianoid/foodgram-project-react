from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin

from recipes.models import Ingredient, IngredientRecipeRelation, Recipe, Tag


class IngredientRecipeRelationAdminInline(admin.TabularInline):
    model = IngredientRecipeRelation
    extra = 3


class RecipeAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('name', 'author')
    search_fields = ('name', 'author__username', 'author__last_name', 'tags',
                     'author__first_name')
    inlines = (IngredientRecipeRelationAdminInline,)


class IngredeintAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'measurement_unit')


admin.site.register(Ingredient, IngredeintAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
