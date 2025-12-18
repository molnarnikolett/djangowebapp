from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    CATEGORY_CHOICES = [
        ('festmény', 'Festmény'),
        ('ékszer', 'Ékszer'),
        ('porcelán', 'Porcelán'),
    ]

    name = models.CharField("Megnevezés", max_length=100)
    starting_price = models.DecimalField("Induló ár (HUF)", max_digits=10, decimal_places=0)  # induló ár
    auction_time = models.DateTimeField("Árverés ideje")
    category = models.CharField("Kategória", max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='item_images/', null=True, blank=True)

    is_active = models.BooleanField(default=False)          # Fut-e az aukció?
    is_closed = models.BooleanField(default=False)  # végleg lezárult-e
    current_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    winner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
