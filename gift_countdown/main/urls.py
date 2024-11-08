from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('countdown/', views.user_countdown, name='user_countdown'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.login_view, name='login'),
    path('gift/<int:gift_id>/', views.view_gift, name='view_gift'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('delete_gift/<int:gift_id>/', views.delete_gift, name='delete_gift'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)