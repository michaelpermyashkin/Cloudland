import random # to shuffle product order for display
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.urls import reverse
from store.models import Product, Seller, Category
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.decorators import login_required

categories = Category.objects.order_by('name') # list of all categories 
sellers = Seller.objects.order_by('seller_listing_name') # list of all sellers 

# list of all currently active filters
active_filters = {
    'category': 'category_All',
    'seller': '',
    'price': '',
    'min_price': '',
    'max_price': '',
    'order_by': '?',
}
active = [] # array of active filter id's passed into template 

# sets all default filters 
def resetDefaultFilters():
    global active_filters
    active_filters = {
        'seller': '',
        'category': 'category_All',
        'min_price': '',
        'max_price': '',
        'order_by': '?',
    }
    getActiveList()

# builds array of all currently set filters
def getActiveList():
    active.clear()
    for key in active_filters:
        if active_filters[key] != '':
            active.append(active_filters[key])

# # Builds pagination system from product liust to display
# def buildPaginator(request, products):
#     paginator = Paginator(products, 12) # Show 20 products per page.
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return page_obj

# Gets all products that match the current filters settings
def getProductsWithActiveFilters():
    # products = Product.objects.filter(quantity__gte=1).order_by('?')
    products = Product.objects.order_by('?')
    getActiveList()
    if active_filters['min_price'] != '' and active_filters['max_price'] != '':
        products = products.filter(price__gte=active_filters['min_price'], price__lte=active_filters['max_price'])
    if active_filters['min_price'] != '' and active_filters['max_price'] == '':
        products = products.filter(price__gte=active_filters['min_price'])
    if active_filters['seller'] != '':
        products = products.filter(seller__slug = active_filters['seller'])
    if active_filters['category'] != 'category_All' and active_filters['category'] != '':
        products = products.filter(category__slug = active_filters['category'])
    if active_filters['order_by'] != '':
        products = products.order_by(active_filters['order_by'])
    return products


# Products page to view all items
def products_page_all(request):
    resetDefaultFilters()
    products = getProductsWithActiveFilters()
    args = {
        'products': products,
        'sellers': sellers,
        'categories': categories,
        'active': active,
    }
    return render(request, 'store/products-page.html', args)

# Filter products by selected seller
def products_by_seller(request, slug):
    active_filters['seller'] = slug
    products = getProductsWithActiveFilters()
    args = {
        'products': products,
        'sellers': sellers,
        'categories': categories,
        'active': active,
    }
    return render(request, 'store/products-page.html', args)

# Filter products by selected category
def products_by_category(request, slug):
    active_filters['category'] = slug
    products = getProductsWithActiveFilters()
    args = {
        'products': products,
        'sellers': sellers,
        'categories': categories,
        'active': active,
    }
    return render(request, 'store/products-page.html', args)

# Sets the order_by filter
def products_order_by(request, order_by):
    active_filters['order_by'] = order_by
    products = getProductsWithActiveFilters()
    args = {
        'products': products,
        'sellers': sellers,
        'categories': categories,
        'active': active,
    }
    return render(request, 'store/products-page.html', args)


# Filter products by price where lower and upper bound is defined
def products_by_price(request, min_price, max_price):
    active_filters['price'] = 'price_'+str(min_price)+'-'+str(max_price)
    active_filters['min_price'] = min_price
    active_filters['max_price'] = max_price
    products = getProductsWithActiveFilters()
    args = {
        'products': products,
        'sellers': sellers,
        'categories': categories,
        'active': active,
    }
    return render(request, 'store/products-page.html', args)

# Filter products by price where only lower bound is defined
def products_by_price_min(request, min_price):
    active_filters['price'] = 'price_'+str(min_price)
    active_filters['min_price'] = min_price
    products = getProductsWithActiveFilters()
    args = {
        'products': products,
        'sellers': sellers,
        'categories': categories,
        'active': active,
    }
    return render(request, 'store/products-page.html', args)

# View when an item is selected to display item detail
def view_item(request, id):
    product = Product.objects.get(product_id=id)
    qaunt_available = range(1, product.quantity+1)
    args = {
        'product': product,
        'qaunt_available': qaunt_available,
    }
    return render(request, 'store/view-item.html', args)

# Contact page
def about(request):
    sellers = Seller.objects.all() 
    return render(request, 'store/about.html', {'sellers': sellers})

# Contact page
@login_required
def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            from_email = form.cleaned_data['your_email']
            subject = "Message from: " + from_email + " re: " + form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, [settings.DEFAULT_FROM_EMAIL])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return render(request, 'store/contact-success.html')
    return render(request, 'store/contact.html', {'form': form})


# products = [
#     {
#         'product_id': 100002,
#         'product_name': 'Item name',
#         'price': 7.98,
#         'seller': Seller.objects.get(pk=1),
#         'category': Category.objects.get(pk=1),
#         'description_short': 'Brief description...',
#         'description_full': 'Full product description...',
#         'product_image': 'img.jpg',
#         'is_featured': False,
#         'date_listed': datetime.now(),
#         'quantity': 10,
#     }, 
# ]

# for product in products:
#     Product.objects.create(**product)