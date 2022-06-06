from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers

router = routers.DefaultRouter()
router.register('books', views.BookView)
router.register('authors', views.AuthorView)

urlpatterns = [

    path('', views.index, name='home'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('login/', views.login_view, name='login'),
    path('register/', views.signup_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('api/', include(router.urls)),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('profile/', views.user_profile, name='profile'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)