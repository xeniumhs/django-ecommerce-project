import os
from django.db import models
from django.utils.text import slugify
from base.models import BaseModel
from django.utils.timezone import now
from django.contrib.auth.models import User
from accounts.models import Profile  # Import the Profile model
from django.core.exceptions import ValidationError


class Category(BaseModel):
    category_name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(unique=True, blank=True)
    category_image = models.ImageField(upload_to="categories/", default="default_category.jpg")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)  # Changed to auto_now_add
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)

class Product(BaseModel):
    product_ID = models.PositiveIntegerField(primary_key=True)  # If you really need custom primary key
    product_name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_in_stock = models.PositiveIntegerField(default=0)
    product_description = models.TextField()
    product_image = models.ImageField(upload_to="product_images/", null=True, blank=True, default="product_images/default.jpg")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)  # Changed to auto_now_add

    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.product_image and os.path.isfile(self.product_image.path):
            os.remove(self.product_image.path)
        super().delete(*args, **kwargs)


class Cart(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return f"Cart of {self.user.username}"
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.user.username}'s cart"

    def clean(self):
        if self.quantity > self.product.quantity_in_stock:
            raise ValidationError(f"Cannot add more than {self.product.quantity_in_stock} of {self.product.name} to the cart.")
    
    def save(self, *args, **kwargs):
        self.clean()  # Ensure validation is done before saving
        super().save(*args, **kwargs)


class Order(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    shipping_address = models.TextField(blank=True, null=True)  # Optional: Store address
    payment_status = models.CharField(max_length=20, default='unpaid')  # Optional: Payment status


    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"

    def save(self, *args, **kwargs):
        # Set the price_at_purchase to the current product price at the time of the order
        self.price_at_purchase = self.product.price
        super().save(*args, **kwargs)
