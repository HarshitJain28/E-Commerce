from django.db import models
from PIL import Image

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=100)
    product_category = models.CharField(max_length=100)
    product_description = models.CharField(max_length=500)
    product_price = models.IntegerField()
    product_image = models.ImageField(upload_to='images', default='default.png') 

    def __str__(self):
        return (self.product_name[:15] + ' | Category: ' + self.product_category)

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)

        img = Image.open(self.product_image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.product_image.path)