from django.urls import path
from . import views

urlpatterns = [
    path('', views.addEnvelopeDescription, name='homepage'),
    path('showenvelopedescription/', views.displayEnvelopeDescriptions, name='display_envelope_descriptions'),
    path('delete/<int:id>/', views.deleteEnvelopeDescription, name='envelopedescription_delete'),
    path('update/<int:id>/', views.updateEnvelopeDescription, name='envelopedescription_update'),
]