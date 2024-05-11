from django.contrib import admin
from .models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    
    list_display = ('title', 'created_at', 'modified_at')

    
    search_fields = ('title', 'content')

    
    list_filter = ('created_at', 'modified_at')

    
    list_per_page = 50

    
    list_display_links = ('title',)


