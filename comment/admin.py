from django.contrib import admin
from .models import Comment

# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'author', 'created_at', 'activate']
    list_filter = ['activate', 'created_at', 'updated_at']
    search_fields = ['author', 'body']
    list_editable = ['activate']
