from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.account.models import User
from apps.product.models import Product


class Promo(models.Model):
    name = models.CharField(max_length=8)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    expire_date = models.DateField(null=True, blank=True)
    discount = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    min_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(250000.00)])
    is_expired = models.BooleanField(default=False)
    members = models.ManyToManyField(User, related_name='promos', blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_ordered = models.BooleanField(default=False)
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    @property
    def get_amount(self):
        return self.unit_price * self.quantity


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    promo = models.CharField(max_length=8, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_delivered = models.BooleanField(default=False)
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def get_amount(self):
        return sum(self.items.values_list('get_amount', flat=True))

