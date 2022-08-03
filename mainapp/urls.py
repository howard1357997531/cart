from django.urls import path
from mainapp.controller import auth, cart, wishlist, checkout, order
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('collections/',views.collections, name='collections'),
    path('collections/<slug:slug>/',views.collectionsview, name='collectionsview'),
    path('collections/<slug:cate_slug>/<slug:prod_slug>/',views.productview, name='productview'),
    path('product_list',views.productlistAjax, name='productlistAjax'),
    path('search_product',views.search_product, name='search_product'),

    path('register/',auth.register, name='register'),
    path('login/',auth.login, name='login'),
    path('logout/',auth.logout, name='logout'),
    path('profile/',auth.profile, name='profile'),
    path('profile_setting/',auth.profile_setting, name='profile_setting'),

    path('cart',cart.cart, name='cart'),
    path('add_to_cart',cart.addtocart, name='addtocart'),  #後面不能加 / 
    path('update_cart',cart.updatecart, name='updatecart'),
    path('delete_cart_item',cart.deletecartitem, name='deletecartitem'),

    path('wishlist',wishlist.wishlist, name='wishlist'),
    path('add_to_wishlist',wishlist.addtowishlist, name='addtowishlist'),
    path('delete_wishlist_item',wishlist.deletewishlistitem, name='deletewishlistitem'),
    
    path('checkout/',checkout.checkout,name='checkout'),
    path('placeorder',checkout.placeorder,name='placeorder'),

    path('my_order/',order.my_order, name='my_order'),
    path('orderview/<str:tracking_num>',order.orderview, name='orderview'),
]


