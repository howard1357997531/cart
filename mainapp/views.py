from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

def home(request):
    trending_products = Product.objects.filter(trending=1)
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
    return render(request,'store/home.html',locals())

def collections(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
    category = Category.objects.filter(status=0)
    return render(request,'store/collections.html',locals())

def collectionsview(request,slug):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
    if Category.objects.filter(slug=slug,status=0):
        products = Product.objects.filter(category__slug=slug)
        category = Category.objects.filter(slug=slug).first()
        return render(request,'store/products/collectionsview.html',locals())
    else:
        messages.warning(request,'沒有相關類別')
        return redirect('collections')

def productview(request,cate_slug,prod_slug):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
    if Category.objects.filter(slug=cate_slug,status=0):
        if Product.objects.filter(slug=prod_slug,status=0):
            products = Product.objects.filter(slug=prod_slug,status=0).first()
            if request.user.is_authenticated:
                hasitem_in_cart = Cart.objects.filter(user=request.user.profile,product__slug=prod_slug).exists() 
        else:
            messages.error(request,'沒有相關產品')
            return redirect('collections')   
    else:
        messages.error(request,'沒有相關類別')
        return redirect('collections')
        
    
    return render(request,'store/products/productview.html',locals())

def productlistAjax(request):    #search_product用
    #products = Product.objects.filter(status=0)                                回傳 <QuerySet [<Product: 香蕉>, <Product: 蘋果>]>
    products = Product.objects.filter(status=0).values_list('name',flat=True)  #回傳 <QuerySet ['香蕉', '蘋果']>
    productslist = list(products)                                              #把 QuerySet 轉成 list
    return JsonResponse(productslist,safe=False)

def search_product(request):
    if request.method == 'POST':
        search_item = request.POST.get('search_product')
        if search_item == '':
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product = Product.objects.filter(name__contains=search_item).first()
            if product:
                return redirect('collections/' + product.category.slug + '/' + product.slug)
            else:
                messages.info(request,'找不到此商品')
                return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))   #回到上一頁


