from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from mainapp.models import Profile ,Product, Cart
from django.contrib import messages

@login_required
def cart(request):
    profile = Profile.objects.get(user=request.user)
    cart = Cart.objects.filter(user=request.user.profile)
    total = 0
    for item in cart:
        total += item.product.selling_price * item.product_qty
    return render(request,'store/cart.html',locals())

def addtocart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))  #抓到 jqajax 裡面 data 裡的 product_id,回傳值是字串
            product_check = Product.objects.get(id=prod_id)
            if product_check:
                if Cart.objects.filter(user=request.user.profile,product_id=prod_id):
                    return JsonResponse({'status':'商品已經在購物車裡'})
                else:
                    prod_qty = int(request.POST.get('product_qty'))
                    if product_check.quantity >= prod_qty:
                        Cart.objects.create(user=request.user.profile,product_id=prod_id,product_qty=prod_qty)
                        return JsonResponse({'status':'商品加入成功'})
                    else:
                        return JsonResponse({'status':'只剩' + str(product_check.quantity) + '個'})
            else:
                return JsonResponse({'status':'找不到此商品'})
        else:
            return JsonResponse({'status':'請登入'})
    return redirect('home')

@login_required
def updatecart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if Cart.objects.filter(user=request.user.profile,product_id=prod_id):
            prod_qty = int(request.POST.get('product_qty'))
            cart = Cart.objects.get(user=request.user.profile,product_id=prod_id)
            cart.product_qty = prod_qty
            cart.save()
            return JsonResponse({'status':'更新成功'})
    return redirect('home')

@login_required
def deletecartitem(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if Cart.objects.filter(user=request.user.profile,product_id=prod_id):
            cart_item = Cart.objects.get(user=request.user.profile,product_id=prod_id)
            cart_item.delete()
        return JsonResponse({'status':'刪除成功'})
    return redirect('home')

    