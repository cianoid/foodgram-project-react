from django.contrib import admin

from .models import Ingredient, Receipt, Tag, IngredientReceiptRelation

from sorl.thumbnail.admin import AdminImageMixin


class ReceiptIngredientsRelationAdminInline(admin.TabularInline):
    model = IngredientReceiptRelation
    extra = 3


class ReceiptAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('name', 'author')
    search_fields = ('name', 'author__username', 'author__last_name', 'tags',
                     'author__first_name')
    inlines = (ReceiptIngredientsRelationAdminInline,)


class IngredeintAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'measurement_unit')


admin.site.register(Ingredient, IngredeintAdmin)
admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(Tag)
