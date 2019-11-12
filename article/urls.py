from django.urls import path

from article import views

app_name = 'article'
urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('article-detail/<int:pk>/', views.article_detail, name='article_detail'),
    path('article-create/', views.article_create, name='article_create'),
    path('article-update/<int:pk>/', views.article_update, name='article_update'),
    path('archives/<int:year>/<int:month>/', views.archive, name='archive'),
    path('categories/<int:pk>/', views.category, name='category'),
    path('tags/<int:pk>/', views.tag, name='tag'),
]
