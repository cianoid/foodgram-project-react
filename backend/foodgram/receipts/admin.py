from django.contrib import admin

from .models import Ingridient, Receipt, Tag, IngridientReceiptRelation

from sorl.thumbnail.admin import AdminImageMixin


class ReceiptIngridientsRelationAdminInline(admin.TabularInline):
    model = IngridientReceiptRelation
    extra = 3


class ReceiptAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('name', 'author')
    search_fields = ('name', 'author__username', 'author__last_name', 'tags',
                     'author__first_name')
    inlines = (ReceiptIngridientsRelationAdminInline, )


class IngrideintAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'measurement_unit')


admin.site.register(Ingridient, IngrideintAdmin)
admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(Tag)
