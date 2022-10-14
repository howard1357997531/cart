from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from mainapp.models import Addressbook, Cart, Order, OrderItem, Product, Profile
from django.contrib import messages
from smtplib import SMTP, SMTPAuthenticationError, SMTPException
from email.mime.text import MIMEText
import random


@login_required
def checkout(request):
    profile = Profile.objects.get(user=request.user)
    address = Addressbook.objects.filter(
        user=request.user.profile, status=True).first()
    cart = Cart.objects.filter(user=request.user.profile)
    for item in cart:
        if item.product_qty > item.product.quantity:
            delete_item = Cart.objects.get(id=item.id)
            delete_item.delete()

    cartitems = Cart.objects.filter(user=request.user.profile)

    total_price = 0
    for item in cartitems:
        total_price += item.product.selling_price * item.product_qty
    return render(request, 'store/checkout.html', locals())


@login_required
def placeorder(request):
    if request.method == 'POST':
        neworder = Order()
        neworder.user = request.user.profile
        neworder.first_name = request.POST.get('first_name')
        neworder.last_name = request.POST.get('last_name')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.address = request.POST.get('address')
        neworder.payment_mode = request.POST.get('payment_mode')

        cart = Cart.objects.filter(user=request.user.profile)
        total_price = 0
        for item in cart:
            total_price += item.product.selling_price * item.product_qty

        neworder.total_price = total_price
        tracknum = 'howard' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_num=tracknum) is None:
            tracknum = 'howard' + str(random.randint(1111111, 9999999))
        neworder.tracking_num = tracknum
        neworder.save()

        cartitem = Cart.objects.filter(user=request.user.profile)
        for item in cartitem:
            OrderItem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.selling_price,
                quantity=item.product_qty
            )

            # 賣出後要清庫存
            orderproduct = Product.objects.filter(id=item.product_id).first()
            orderproduct.quantity -= item.product_qty
            orderproduct.save()

        mailfrom = 'gary8211213@gmail.com'
        mailpw = 'pjfkvlpzftpcamus'
        mailto = request.POST.get('email')
        mailsubject = '購物數位通知網 - 訂單通知'
        mailcontent = '感謝您的光臨，您已經成功完成訂單程序。\n我們將盡快把您選購的商品郵寄給您! 再次感謝您的支持  \
                    \n您的訂單編號為 ' + tracknum + ' 您可以使用這個編號回到網站中查詢訂單的詳細內容。\n購物網'
        send_simple_mail(mailfrom, mailpw, mailto, mailsubject, mailcontent)

        Cart.objects.filter(user=request.user.profile).delete()
        messages.success(request, '下定成功 ! !')
    return redirect('my_order')


def send_simple_mail(mailfrom, mailpw, mailto, mailsubject, mailcontent):
    strSmtp = 'smtp.gmail.com:587'
    strAccount = mailfrom
    strPassword = mailpw
    emailmsg = MIMEText(mailcontent)
    emailmsg['subject'] = mailsubject
    mailto1 = mailto
    server = SMTP(strSmtp)
    server.ehlo()
    server.starttls()
    try:
        server.login(strAccount, strPassword)
        server.sendmail(strAccount, mailto1, emailmsg.as_string())
    except SMTPAuthenticationError:
        msg = '無法登入!'
    except:
        msg = '郵件發送產生錯誤!'
    server.quit()
