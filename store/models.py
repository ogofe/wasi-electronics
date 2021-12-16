from django.db import models
from os import urandom

def generate_product_id():
    return str(urandom(6).hex())[:6].upper()

def generate_invoice():
    return str(urandom(6).hex())[:6].upper()

def get_categories():
    from .models import Product
    cat_list = [product.category for product in Product.objects.all()]
    return cat_list

class Product(models.Model):
    product_id = models.CharField(default=generate_product_id, max_length=7, blank=True)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=1000, decimal_places=2)
    quantity = models.IntegerField(blank=True, null=True)
    images = models.ManyToManyField("ProductImage", blank=True, related_name='images')
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class ProductImage(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="shop/")

    def __str__(self):
        return self.product.name


class Customer(models.Model):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.fullname
    
    @property
    def fullname(self):
        return self.first_name + ' ' + self.last_name

class Cart(models.Model):
    owner = models.OneToOneField(Customer, on_delete=models.CASCADE)
    items = models.ManyToManyField("OrderItem", blank=True)


class OrderItem(models.Model):
    item = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.item.name

    def total(self):
        amt = self.quantity * self.item.price
        return amt


class CheckoutOrder(models.Model):
    ORDER_STATUS = (
        ('pending', "Pending"),
        ('delivered', "Delivered"),
        ('moving', "In Transit"),
        ('resolved', "Resolved"),
    )
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    items = models.ManyToManyField("OrderItem", blank=True)
    invoice = models.CharField(max_length=6, blank=True, default=generate_invoice)
    paid = models.BooleanField(default=False)
    status = models.CharField(default="pending", choices=ORDER_STATUS, max_length=50)
    delivery_on = models.BooleanField(default=False)
    delivery_logs = models.ManyToManyField("DeliveryLog", blank=True, related_name='logs')

    def __str__(self):
        return self.invoice

    def total(self):
        amt = 0
        for item in self.items.all():
            amt += item.item.price * item.quantity
        return amt
    
class DeliveryLog(models.Model):
    order = models.ForeignKey(CheckoutOrder, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    details = models.CharField(max_length=500)

    def __str__(self):
        return self.order.invoice
    
