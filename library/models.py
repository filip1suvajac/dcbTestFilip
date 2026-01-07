from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=120)
    year = models.PositiveIntegerField()
    rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="books")
    desc = models.TextField(max_length=1000)

    def __str__(self):
        return self.name
