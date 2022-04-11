from django.contrib import admin
from .models import Navbar, Book, Author

# Register your models here.
admin.site.register(Navbar)
admin.site.register(Book)
admin.site.register(Author)