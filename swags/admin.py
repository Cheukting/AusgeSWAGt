from django.contrib import admin
from .models import Swag

# Register your models here.
@admin.register(Swag)
class SwagAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'conference', 'rating', 'user', 'created_at')
    list_filter = ('rating', 'conference', 'company')
    search_fields = ('name', 'company', 'conference', 'comments')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
