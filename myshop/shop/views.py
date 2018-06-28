from django.shortcuts import render, get_object_or_404

# Create your views here.
from shop.models import Category, Product


def product_list(request, category_slug=None):
    cateogry = None
    cateogries = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': cateogry,
                   'categories': cateogries,
                   'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request,
                  'shop/product/detail.html',
                  {'product': product})
