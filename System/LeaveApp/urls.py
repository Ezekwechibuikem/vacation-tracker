from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('create-leave/', views.create_leave, name="create-leave"),
    path('leave-list/', views.leave_list, name="leave-list"),
    path('login/', views.login_staff, name='login'),
    path('logout/', views.logout_staff, name='logout'),
    path('register/', views.register_staff, name='register'),
]