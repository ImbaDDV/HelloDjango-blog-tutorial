from django.contrib import admin
from .models import Comment

# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'url', 'article', 'created_time']
    fields = ['name', 'email', 'url', 'text', 'article']
 
 
admin.site.register(Comment, CommentAdmin)