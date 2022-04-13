from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name="home"),
    path('books/', views.BookListView.as_view(), name="books"),
]