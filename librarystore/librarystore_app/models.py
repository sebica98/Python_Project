from distutils.command.upload import upload
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()


class Book(models.Model):
    name = models.CharField(max_length=50)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, related_name="books")
    is_bestselling = models.BooleanField(default=False)
    stock = models.IntegerField(default=10)
    price = models.FloatField(default=4.99)
    slug = models.SlugField(default="", null=False, blank=True, db_index = True)
    image = models.ImageField(upload_to='products/', null=True)

    def __str__(self):
        return self.name


class Navbar(models.Model):
    title = models.CharField(max_length=20)
    path_name = models.CharField(max_length=20, default="")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["id"]