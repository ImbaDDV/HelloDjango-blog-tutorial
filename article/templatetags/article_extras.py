from django import template
from article.models import ArticlePost, Category, Tag

register = template.Library()


@register.inclusion_tag('article/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_post_list': ArticlePost.objects.all()[:num]
    }


@register.inclusion_tag('article/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    return {
        'date_list': ArticlePost.objects.dates('created_time', 'month', order='DESC'),
    }


@register.inclusion_tag('article/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    return {
        'category_list': Category.objects.all(),
    }


@register.inclusion_tag('article/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    return {
        'tag_list': Tag.objects.all(),
    }