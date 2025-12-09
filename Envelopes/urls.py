from django.urls import path
from . import views

urlpatterns = [
    path('addenvelope/', views.display_index, name='index'),
    path('displayenvelopes/', views.display_envelopes, name='envelopes'),
    path('updateenvelope/', views.update_envelope, name='updateenvelope'),
]
