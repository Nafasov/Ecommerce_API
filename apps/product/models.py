from django.db import models
from apps.account.models import User
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    views = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField(Tag)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def get_quantity(self):
        incomes = self.trades.filter(quantity=1).count()
        outcomes = self.trades.filter(quantity=2).count()
        return incomes - outcomes

    @property
    def get_available(self):
        return self.get_quantity > 0


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products')

    def __str__(self):
        return self.product.name


class Trade(models.Model):
    ACTION = (
        (1, _('Income')),
        (2, _('Outcome')),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='trades')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.IntegerField(choices=ACTION, default=1)
    quantity = models.PositiveIntegerField(default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name


