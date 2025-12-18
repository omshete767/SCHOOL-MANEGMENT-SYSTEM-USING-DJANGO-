from django.urls import path
from . import views

urlpatterns = [
    # ADMIN CRUD
    path('', views.teacher_list, name='teacher_list'),
    path('add/', views.teacher_add, name='teacher_add'),
    path('edit/<int:id>/', views.teacher_edit, name='teacher_edit'),
    path('delete/<int:id>/', views.teacher_delete, name='teacher_delete'),

    # TEACHER DASHBOARD
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
]
