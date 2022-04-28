from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers

router = routers.DefaultRouter()
router.register('books', views.BookView)
router.register('authors', views.AuthorView)

urlpatterns = [

    path('', views.index, name="home"),
    path('books/', views.BookListView.as_view(), name="books"),
    path('cart/', views.show_cart, name='cart'),
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('login/', views.login_view, name="login"),
    path('register/', views.signup_view, name="register"),
    path('checkout/', views.purchase_view, name="checkout"),
    path('logout/', views.logout_view, name="logout"),
    path('api/', include(router.urls)),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)