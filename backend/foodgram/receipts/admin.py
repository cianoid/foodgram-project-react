from django.contrib import admin

from .models import Ingridients, Receipts, Tags, ReceiptIngridientsRelation

from sorl.thumbnail.admin import AdminImageMixin


class ReceiptIngridientsRelationAdminInline(admin.TabularInline):
    model = ReceiptIngridientsRelation
    extra = 3


class ReceiptsAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('name', 'author')
    search_fields = ('name', 'author__username', 'author__last_name', 'tags',
                     'author__first_name')
    inlines = (ReceiptIngridientsRelationAdminInline, )


class IngrideintsAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'measurement_unit')


admin.site.register(Ingridients, IngrideintsAdmin)
admin.site.register(Receipts, ReceiptsAdmin)
admin.site.register(Tags)
