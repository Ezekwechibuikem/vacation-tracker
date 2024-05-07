from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.home, name='index'),
    path('dashboard/', views.dash_board, name='dashboard'),
    path('profile/', views.pro_file, name='profile'),
    path('update-emp/<int:user_id>/update/', views.update_employee, name='update-emp'),
    path('create-leave/', views.create_leave, name='create-leave'),
    path('leave-detail/<int:leave_id>/', views.leave_detail, name='leave-detail'),
    path('', views.login_staff, name='login'),
    path('logout/', views.logout_staff, name='logout'),
    path('register/', views.register_staff, name='register'),
    # path('approve-reject/', views.approve_reject_leave, name='approve_reject'),
    path('leave-requests/', views.view_leave_requests, name='leave_requests'),
    path('leave-requests/<int:leave_request_id>/approve-reject/', views.approve_reject_leave, name='approve_reject_leave'),
]