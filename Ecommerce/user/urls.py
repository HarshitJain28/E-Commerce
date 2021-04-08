from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('profile', views.profile, name='user-profile'),
    path('register/', views.register, name='user-register'),
    path('past-orders/', views.past_orders, name='past-orders'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'),
         name='user-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'),
         name="user-logout"),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='user/password_reset.html'), name='password_reset'),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(
        template_name='user/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='user/password_reset_complete.html'), name='password_reset_complete'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='user/password_reset_confirm.html'), name='password_reset_confirm'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
