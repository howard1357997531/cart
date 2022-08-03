from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from mainapp.models import Order, OrderItem, Profile
from django.contrib import messages

@login_required
def my_order(request):
    profile = Profile.objects.get(user=request.user)
    orders = Order.objects.filter(user=request.user.profile).order_by('-create_at')
    return render(request,'store/order.html',locals())

@login_required
def orderview(request,tracking_num):
    profile = Profile.objects.get(user=request.user)
    order = Order.objects.filter(user=request.user.profile,tracking_num=tracking_num).first()
    orderitems = OrderItem.objects.filter(order=order) #order不能傳入quaryset，必須是值，因此上面用first()取出
    return render(request,'store/orderview.html',locals())