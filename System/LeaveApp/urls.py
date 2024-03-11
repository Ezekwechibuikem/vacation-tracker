from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.home, name='index'),
    path('dashboard', views.dash_board, name='dashboard'),
    path('update-emp/', views.update_employee, name='update-emp'),
    path('create-leave/', views.create_leave, name='create-leave'),
    path('leave-detail/<int:leave_id>/', views.leave_detail, name='leave-detail'),
    path('', views.login_staff, name='login'),
    path('logout/', views.logout_staff, name='logout'),
    path('register/', views.register_staff, name='register'),
]
