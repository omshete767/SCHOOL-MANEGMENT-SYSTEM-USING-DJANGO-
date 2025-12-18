from django.urls import path
from . import views

urlpatterns = [
    path('take/<int:course_id>/', views.take_attendance, name='take_attendance'),
]
