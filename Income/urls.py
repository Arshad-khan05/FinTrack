from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_income, name='add_income'),
    path('list/', views.display_incomes, name='display_incomes'),
    path('update/', views.update_incomes, name='update_income'),
    path('update/<int:income_id>/', views.edit_income, name='edit_income'),
    path('delete/<int:income_id>/', views.delete_income, name='delete_income'),

    path('descriptions/add/', views.add_income_description, name='add_income_description'),
    path('descriptions/', views.display_income_descriptions, name='display_income_descriptions'),
    path('descriptions/delete/<int:id>/', views.delete_income_description, name='delete_income_description'),
    path('descriptions/update/<int:id>/', views.update_income_description, name='update_income_description'),
]
