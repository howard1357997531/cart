from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.db.models.functions import ExtractMonth
from django.db.models import Count, Sum
import calendar
from django.contrib import messages
from .models import *
from .forms import AddressForm


def home(request):
    trending_products = Product.objects.filter(trending=1)
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
    return render(request, 'store/home.html', locals())


def collections(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
    category = Category.objects.filter(status=0)
    return render(request, 'store/collections.html', locals())


def collectionsview(request, slug):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
    if Category.objects.filter(slug=slug, status=0):
        products = Product.objects.filter(category__slug=slug)
        category = Category.objects.filter(slug=slug).first()
        return render(request, 'store/products/collectionsview.html', locals())
    else:
        messages.warning(request, '沒有相關類別')
        return redirect('collections')


def productview(request, cate_slug, prod_slug):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
    if Category.objects.filter(slug=cate_slug, status=0):
        if Product.objects.filter(slug=prod_slug, status=0):
            products = Product.objects.filter(slug=prod_slug, status=0).first()
            if request.user.is_authenticated:
                hasitem_in_cart = Cart.objects.filter(
                    user=request.user.profile, product__slug=prod_slug).exists()
        else:
            messages.error(request, '沒有相關產品')
            return redirect('collections')
    else:
        messages.error(request, '沒有相關類別')
        return redirect('collections')

    return render(request, 'store/products/productview.html', locals())


def productlistAjax(request):  # search_product用
    # products = Product.objects.filter(status=0)                                回傳 <QuerySet [<Product: 香蕉>, <Product: 蘋果>]>
    products = Product.objects.filter(status=0).values_list(
        'name', flat=True)  # 回傳 <QuerySet ['香蕉', '蘋果']>
    productslist = list(products)  # 把 QuerySet 轉成 list
    return JsonResponse(productslist, safe=False)


def search_product(request):
    if request.method == 'POST':
        search_item = request.POST.get('search_product')
        if search_item == '':
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product = Product.objects.filter(
                name__contains=search_item).first()
            # contains 只會找到第一個符合條件的
            # icontains 會找到所有符合條件的
            # print(Product.objects.filter(name__icontains=search_item))
            if product:
                return redirect('collections/' + product.category.slug + '/' + product.slug)
            else:
                messages.info(request, '找不到此商品')
                return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))  # 回到上一頁


@login_required
def month_chart(request):
    profile = Profile.objects.get(user=request.user)
    order = Order.objects.filter(user=request.user.profile).annotate(
        month=ExtractMonth('create_at')).values('month').annotate(count=Count('id')).values('month', 'count')
    # print(order)
    months = []
    order_count = []
    for ord in order:
        months.append(calendar.month_name[ord['month']])
        order_count.append(ord['count'])
    #print(months, order_count)
    month_cost = Order.objects.filter(user=request.user.profile).annotate(
        month=ExtractMonth('create_at')).values('month').annotate(total=Sum('total_price'))
    print(month_cost)
    total_cost = [cost['total'] for cost in month_cost]
    return render(request, 'store/auth/month_chart.html', locals())


@login_required
def address_book(request):
    profile = Profile.objects.get(user=request.user)
    address = Addressbook.objects.filter(
        user=request.user.profile)

    return render(request, 'store/auth/address_book.html', locals())


@login_required
def add_address_book(request):
    profile = Profile.objects.get(user=request.user)
    form = AddressForm()
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            saveform = form.save(commit=False)
            saveform.user = request.user.profile
            if 'status' in request.POST:
                Addressbook.objects.filter(
                    user=request.user.profile).update(status=False)
            saveform.save()
            return redirect('address_book')

    return render(request, 'store/auth/add_address_book.html', locals())


@login_required
def acticate_address(request):
    address_id = request.GET.get('id')
    Addressbook.objects.update(status=False)
    Addressbook.objects.filter(id=int(address_id)).update(status=True)

    return JsonResponse({'bool': True})


@login_required
def edit_address(request):
    card_id = request.GET.get('id')
    address = Addressbook.objects.get(id=int(card_id))
    form = AddressForm(instance=address)
    t = render_to_string('store/auth/ajax/edit_address.html', locals())
    return JsonResponse({'data': t})


@login_required
def save_address(request, pk):
    address = Addressbook.objects.get(id=pk)
    print(address)
    address.first_name = request.POST.get('first_name')
    address.last_name = request.POST.get('last_name')
    address.phone = request.POST.get('phone')
    address.address = request.POST.get('address')
    address.email = request.POST.get('email')
    if request.POST.get('status'):
        Addressbook.objects.update(status=False)
        address.status = True
    else:
        address.status = False
    address.save()
    return JsonResponse({'bool': True})
