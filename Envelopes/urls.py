from django.urls import path
from . import views

urlpatterns = [
    path('addenvelope/', views.display_addenvelope, name='addenvelope'),
    path('displayenvelopes/', views.display_envelopes, name='envelopes'),
    path('updateenvelope/', views.display_update_envelope, name='updateenvelope'),
    path('updateenvelope/update/<int:envelope_id>/', views.update_envelope, name='update_envelope'),
    path('updateenvelope/delete/<int:envelope_id>/', views.delete_envelope, name='delete_envelope')
]