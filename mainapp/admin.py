from unicodedata import category
from django.contrib import admin
from .models import *

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','tracking_num','create_at','update_at')

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)
