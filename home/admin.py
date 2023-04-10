from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Category)


@admin.register(models.Product)
class ArtAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created', 'price']
    search_fields = ('name', 'body', 'slug')
    list_editable = ['price']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 10





# admin.site.register(models.Product)