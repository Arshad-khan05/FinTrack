from . import views
from django.urls import path

urlpatterns = [
    path('', views.render_homepage, name='homepage'),
    path('login/', views.render_login_page, name='login'),
    path('signup/', views.render_signup_page, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('reset-password/', views.render_reset_password_page, name='reset_password'),
]