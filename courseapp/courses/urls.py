from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

r = DefaultRouter()
r.register('categories', views.CategoryView, basename='category')
r.register("courses", views.CourseView, basename='course')
r.register("lessons", views.LessonView, basename='lesson')
r.register("users", views.UserView, basename='user')
r.register('comments', views.CommentView, basename='comment')

urlpatterns = [
    path('', include(r.urls))
]