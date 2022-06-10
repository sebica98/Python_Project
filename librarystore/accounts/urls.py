from django.urls import path
from . import views

urlpatterns = [
    path('accounts/', views.dashboard, name='dashboard'),
    path('change_password/', views.change_password, name='change_password'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]