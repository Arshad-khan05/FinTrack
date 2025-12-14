from django.urls import path
from . import views

urlpatterns = [
    path('', views.addEnvelopeDescription, name='homepage'),
    path('showenvelopedescription/', views.displayEnvelopeDescriptions, name='display_envelope_descriptions'),
]