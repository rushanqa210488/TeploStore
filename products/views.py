from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.forms import CartAddProductForm
from cart.forms import CartAddProductForm

from products.models import Product, ProductCategory, Basket
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    context = {'title': 'Главная'}
    return render(request, 'products/index.html', context=context)



def products(request, category_id=None, page_number=1):
    products = Product.objects.filter(category__id=category_id) if category_id else Product.objects.all()
    per_page = 6
    paginator = Paginator(products, per_page)
    products_paginator = paginator.page(page_number)
    context = {
        'title': 'Store - catalog',
        'categories': ProductCategory.objects.all(),
        'products': products_paginator,
        'cart_product_form': CartAddProductForm()
  
    }
    return render(request, 'products/products.html', context=context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_product_form = CartAddProductForm()
    return render(request, 'products/detail.html', {
                'product': product,
                'cart_product_form': cart_product_form,
        })



def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)
    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])