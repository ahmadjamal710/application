from django.contrib import admin
from .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user_id', 'completed', 'created_at')
    list_filter = ('completed', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        (None, {
            'fields': ('user_id', 'title', 'description', 'completed')
        }),
        ('Dates', {
            'fields': ('created_at',)
        }),
    )
