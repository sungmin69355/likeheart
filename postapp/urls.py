from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('<int:post_id>/', views.detail, name='detail'),
    path('new/', views.new, name='new'),
    path('create/', views.create, name='create'),
    path('<int:post_pk>/comment_write/', views.comment_write, name='comment_write'),
    path('<int:post_pk>/delete', views.delete, name='delete'), 
    path('<int:post_pk>/edit', views.edit, name='edit'),
    path('like', views.like, name='like'),
    path('<int:post_pk>/<int:pk>/comment_delete/', views.comment_delete, name='comment_delete'),
    path('search', views.search, name='search'),
]
