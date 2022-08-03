from django.db import models
from django.contrib.auth.models import User
import datetime
import uuid
import os 

def get_profile_file_path(request,filename):
    original_filename = filename
    nowtime = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = f'{nowtime}-{original_filename}'
    return os.path.join('profile/',filename)

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    first_name = models.CharField(max_length=150,null=True,blank=True)
    last_name = models.CharField(max_length=150,null=True,blank=True)
    phone = models.CharField(max_length=150,null=True,blank=True)
    address = models.CharField(max_length=150,null=True,blank=True)
    email = models.EmailField(max_length=150,null=True,blank=True)
    profile_image = models.ImageField(upload_to=get_profile_file_path,null=True,blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    @property
    def cart_item_total(self):
        total = len(self.cart_set.all())
        return total
    
    @property
    def wishlist_item_total(self):
        total = len(self.wishlist_set.all())
        return total

    @property
    def profile_imageURL(self):
        try:
            url = self.profile_image.url
        except:
            url = 'images/profile.jpg'
        return url

    def __str__(self):
        return str(self.user)
    
def get_file_path(request,filename):
    original_filename = filename
    nowtime = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = f'{nowtime}-{original_filename}'
    return os.path.join('uploads/',filename)

class Category(models.Model):                                        #editable 不可修改(會直接不顯示)
    slug = models.SlugField(null=False,unique=True,default=uuid.uuid1,editable=False)  
    name = models.CharField(max_length=150,null=False,blank=False)
    image = models.ImageField(upload_to=get_file_path,null=True,blank=True)
    description = models.TextField(max_length=500,null=False,blank=False)
    status = models.BooleanField(default=False,help_text='0=default,1=Hidden')
    trending = models.BooleanField(default=False,help_text='0=default,1=Trending') #趨勢
    meta_title = models.CharField(max_length=150,null=False,blank=False)
    meta_keywords = models.CharField(max_length=150,null=False,blank=False)
    meta_description = models.TextField(max_length=150,null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    slug = models.SlugField(null=False,unique=True,default=uuid.uuid1) 
    name = models.CharField(max_length=150,null=False,blank=False)
    product_image = models.ImageField(upload_to=get_file_path,null=True,blank=True)
    small_description = models.CharField(max_length=150,null=False,blank=False)
    description = models.TextField(max_length=500,null=False,blank=False)
    quantity = models.IntegerField(null=False,blank=False)
    original_price = models.IntegerField(null=False,blank=False)
    selling_price = models.IntegerField(null=False,blank=False)
    status = models.BooleanField(default=False,help_text='0=default,1=Hidden')
    trending = models.BooleanField(default=False,help_text='0=default,1=Trending')
    tag = models.CharField(max_length=150,null=True,blank=True)
    meta_title = models.CharField(max_length=150,null=True,blank=True)
    meta_keywords = models.CharField(max_length=150,null=True,blank=True)
    meta_description = models.CharField(max_length=150,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def product_imageURL(self):
        try:
            url = self.product_image.url
        except:
            url = ''
        return url
    
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False,blank=False)
    create_at = models.DateTimeField(auto_now_add=True)

    @property
    def item_totalprice(self):
        total = self.product.selling_price * self.product_qty
        return total

    def __str__(self):
        return f'{self.user}- {self.product}'

class Wishlist(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150,null=False)
    last_name = models.CharField(max_length=150,null=False)
    email = models.CharField(max_length=150,null=False)
    phone = models.CharField(max_length=150,null=False)
    address = models.CharField(max_length=150,null=False)
    total_price = models.IntegerField(null=False)
    payment_mode = models.CharField(max_length=150,null=True,blank=True)
    payment_id = models.CharField(max_length=150,null=True,blank=True)
    orderstatus = (
        ('運送中','運送中'),
        ('完成','完成')
    )
    status = models.CharField(max_length=150,default='運送中',choices=orderstatus)
    message = models.TextField(null=True,blank=True)
    tracking_num = models.CharField(max_length=150,null=True,blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} - {self.tracking_num}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.IntegerField(null=False)
    quantity = models.IntegerField(null=False)

    @property
    def item_totalprice(self):
        total = self.product.selling_price * self.quantity
        return total
        
    def __str__(self):
        return f'{self.order.id} - {self.order.tracking_num}'


    


