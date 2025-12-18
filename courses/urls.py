from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('add/', views.course_add, name='course_add'),
    path('edit/<int:id>/', views.course_edit, name='course_edit'),
    path('delete/<int:id>/', views.course_delete, name='course_delete'),
    
]
