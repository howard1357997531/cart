from django.urls import path
from mainapp.controller import auth, cart, wishlist, checkout, order
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('collections/', views.collections, name='collections'),
    path('collections/<slug:slug>/', views.collectionsview, name='collectionsview'),
    path('collections/<slug:cate_slug>/<slug:prod_slug>/',
         views.productview, name='productview'),
    path('product_list', views.productlistAjax, name='productlistAjax'),
    path('search_product', views.search_product, name='search_product'),

    path('register/', auth.register, name='register'),

    # name='login',name='logout'為django內建方法(早已在urls.py自己設定)
    path('login/', auth.login, name='login2'),
    path('logout/', auth.logout, name='logout2'),
    path('profile', auth.profile, name='profile'),
    path('profile_setting', auth.profile_setting, name='profile_setting'),

    path('cart', cart.cart, name='cart'),
    path('add_to_cart', cart.addtocart, name='addtocart'),  # 後面不能加 /
    path('update_cart', cart.updatecart, name='updatecart'),
    path('delete_cart_item', cart.deletecartitem, name='deletecartitem'),

    path('wishlist', wishlist.wishlist, name='wishlist'),
    path('add_to_wishlist', wishlist.addtowishlist, name='addtowishlist'),
    path('delete_wishlist_item', wishlist.deletewishlistitem,
         name='deletewishlistitem'),

    path('checkout/', checkout.checkout, name='checkout'),
    path('placeorder', checkout.placeorder, name='placeorder'),

    path('month_chart', views.month_chart, name='month_chart'),
    path('address_book', views.address_book, name='address_book'),
    path('add_address_book', views.add_address_book, name='add_address_book'),
    path('acticate_address', views.acticate_address, name='acticate_address'),
    path('edit_address', views.edit_address, name='edit_address'),
    path('save_address/<int:pk>', views.save_address, name='save_address'),
    path('my_order', order.my_order, name='my_order'),
    path('orderview/<str:tracking_num>', order.orderview, name='orderview'),


]
