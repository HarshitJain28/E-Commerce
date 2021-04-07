from django.db import models
from PIL import Image
from user.models import User
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_category = models.CharField(max_length=100)
    product_description = models.CharField(max_length=500)
    product_price = models.IntegerField()
    product_image = models.ImageField(upload_to='images', default='default.png') 

    def __str__(self):
        return (self.product_name[:15] + ' | Category: ' + self.product_category)

    def get_absolute_url(self):
        return reverse("detail-product", kwargs={"id": self.id})

    def add_to_cart(self):
        return reverse('add-to-cart', kwargs={"id": self.id})
    
    def remove_from_cart(self):
        return reverse('remove-from-cart', kwargs={"id": self.id})

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)

        img = Image.open(self.product_image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.product_image.path)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_status = models.BooleanField(default=False)
    cart_date = models.DateField(blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def total_price(self):
        return self.quantity * self.product.product_price

    def __str__(self):
        return f"{self.user.username} | cartID: {self.id} | cartProduct: {self.product}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Cart)
    order_date = models.DateField(blank=True, null=True)
    order_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} | OrderId: {self.id}"