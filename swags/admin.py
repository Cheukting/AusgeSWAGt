from django.contrib import admin
from .models import Swag, SwagComment, SwagRating

# Register your models here.
@admin.register(Swag)
class SwagAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'conference', 'rating', 'user', 'created_at')
    list_filter = ('rating', 'conference', 'company')
    search_fields = ('name', 'company', 'conference', 'comments')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'

@admin.register(SwagComment)
class SwagCommentAdmin(admin.ModelAdmin):
    list_display = ('swag', 'user', 'text', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('text', 'swag__name', 'user__username')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'

@admin.register(SwagRating)
class SwagRatingAdmin(admin.ModelAdmin):
    list_display = ('swag', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'user')
    search_fields = ('swag__name', 'user__username')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
