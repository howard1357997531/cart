from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from mainapp.models import Product, Wishlist, Profile
from django.contrib import messages

@login_required
def wishlist(request):
    profile = Profile.objects.get(user=request.user)
    wishlist = Wishlist.objects.filter(user=request.user.profile)  #如果 return 的東西超過1個就要用filter，不能用 get
    return render(request,'store/wishlist.html',locals())  #filter是回傳一個 <QuerySet [<Wishlist: Wishlist object (1)>, <Wishlist: Wishlist object (2)>]>

def addtowishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if product_check:
                if Wishlist.objects.filter(user=request.user.profile,product_id=prod_id):
                    return JsonResponse({'status':'商品已經在願望清單裡'})
                else:
                    Wishlist.objects.create(user=request.user.profile,product_id=prod_id)
                    return JsonResponse({'status':'成功加入願望清單'})
            else:
                return JsonResponse({'status':'沒有此商品'})
        else:
            return JsonResponse({'status':'請登入'})
    return redirect('home')

@login_required
def deletewishlistitem(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if Wishlist.objects.filter(user=request.user.profile,product_id=prod_id):
            wishlist_item = Wishlist.objects.get(user=request.user.profile,product_id=prod_id)
            wishlist_item.delete()
            return JsonResponse({'status':'已從願望清單移除'})
        else:
            return JsonResponse({'status':'在願望清單中找不到此商品'})
    else:
        return JsonResponse({'status':'請登入'})
    return redirect('home')