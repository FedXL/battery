from django.contrib import admin
from export.models import Export


# Register your models here.

@admin.register(Export)
class ExportAdmin(admin.ModelAdmin):
    list_display = ('name','created_at')