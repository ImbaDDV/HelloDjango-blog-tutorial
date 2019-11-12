from django.contrib import admin
from .models import ArticlePost, Category, Tag


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']
    fields = ['title', 'body', 'excerpt', 'category', 'tags']

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(ArticlePost, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Tag)