from django.contrib import admin
from .models import User

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('username',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Dates', {'fields': ('created_at',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
