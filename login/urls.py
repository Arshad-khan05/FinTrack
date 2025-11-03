from . import views
from django.urls import path

urlpatterns = [
    path('', views.render_homepage, name='homepage')
]