from django.db import models
from django.contrib.auth.models import User

# Create your models here.
CATEGORY_CHOICES = (
    ('CR', 'CURD'),
    ('ML', 'MILK'),
    ('LS', 'LASSI'),
    ('MS', 'MILKSHAKE'),
    ('PN', 'PANEER'),
    ('GH', 'GHEE'),
    ('CZ', 'CHEESE'),
    ('IC', 'ICE-CREAM'),
)
STATE_CHOICES = [
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jammu & Kashmir', 'Jammu & Kashmir'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odisha', 'Odisha'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ('West Bengal', 'West Bengal'),
    ('Andaman & Nicobar Islands', 'Andaman & Nicobar Islands'),
    ('Chandigarh', 'Chandigarh'),
    ('Dadra & Nagar Haveli and Daman & Diu', 'Dadra & Nagar Haveli and Daman & Diu'),
    ('Lakshadweep', 'Lakshadweep'),
    ('Delhi', 'Delhi'),
    ('Puducherry', 'Puducherry')
]
class  Product(models.Model):
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discounted_price=models.FloatField()
    description=models.TextField()
    composition=models.TextField(default="")
    prodapp=models.TextField(default="")
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    product_image=models.ImageField( upload_to='Product/')
    def __str__(self):
        return self.title
    
class Customer(models.Model):  
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    name = models.CharField(max_length=200)  
    locality = models.CharField(max_length=200)  
    city = models.CharField(max_length=50)  
    mobile = models.IntegerField(default=0)  
    zipcode = models.IntegerField()  
    state = models.CharField(choices=STATE_CHOICES,max_length=100)  
    
    def __str__(self):  
        return self.name  
    
    
    
class Cart(models.Model):  
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    quantity = models.PositiveIntegerField(default=1)  

    @property  
    def total_cost(self):  
        return self.quantity * self.product.discounted_price      
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.title} (Wishlist)"    