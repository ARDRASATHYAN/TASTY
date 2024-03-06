from django.db import models
from homeapp.models import *
from django.contrib.auth.models import User

# Create your models here.
class cartlist(models.Model):
    cartid=models.CharField(max_length=100,unique=True)
    date_addedd=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cartid

class items(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prodt=models.ForeignKey(product, on_delete=models.CASCADE)
    cart=models.ForeignKey(cartlist, on_delete=models.CASCADE)
    quantity=models.IntegerField()
    active=models.BooleanField(default=True)
    def __str__(self):
        return str(self.prodt)
    def total(self):
        return self.prodt.price * self.quantity
    # def total(self):
    #     return self.prodt.price*self.quantity 


#like btn
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_order_total(self):
        return sum(item.total for item in self.orderitem_set.all())

    def __str__(self):
        return f"{self.user.username}'s order - {self.created_at}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order.user.username}'s order item - {self.product.name}"
