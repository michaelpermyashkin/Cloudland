from django.contrib.auth.models import User
from django.shortcuts import render
from datetime import datetime
from store.models import Product
import random # to shuffle product order for display

def updateProductList(filterCategory):
    if filterCategory == 'all':
        products = Product.objects.values().order_by('?')
    else:
        products = Product.objects.filter(category=filterCategory)
    args = {
        'products':products,
    }
    return args

# Landing home page
def home(request):
    args = updateProductList('all')
    return render(request, 'store/index.html', args)

# Products page to view all items
def products_page_all(request):
    args = updateProductList('all')
    args['category'] = 'All Products'
    return render(request, 'store/products-page.html', args)

# Products page to view accessory items
def products_page_accessories(request):
    args = updateProductList('accessories')
    args['category'] = 'accessories'
    return render(request, 'store/products-page.html', args)

# Products page to view craft items
def products_page_craft(request):
    args = updateProductList('craft')
    args['category'] = 'craft'
    return render(request, 'store/products-page.html', args)

    # Products page to view jewelry items
def products_page_jewelry(request):
    args = updateProductList('jewelry')
    args['category'] = 'jewelry'
    return render(request, 'store/products-page.html', args)

# View when an item is selected to display item detail
def view_item(request):
    selectedProductID = None
    if request.method == 'POST':
        for key in request.POST.keys():
            if key.startswith('get-prod-info'):
                selectedProductID = int(key[13:])

    # we successfully found product
    if selectedProductID != None:
        product = Product.objects.filter(productID=selectedProductID)
        args = {
            'product': product,
        }
        return render(request, 'store/view-item.html', args)
    #  maybe add an oops page instead of going back to same page
    else :
        return render(request, 'store/products-page.html')

# Contact page
def contact(request):
    return render(request, 'store/contact.html')

# products = [
#     {
#         # 'productID': 999999,
#         'productName': 'Item name',
#         'category': 'jewelry',
#         'price': 7.98,
#         'description': 'Some discription',
#         'productImage': 'img.jpg',
#         'is_featured': True,
#         'dateListed': datetime.now(),
#         'quantity': 10,
#     }, {
#         # 'productID': 100002,
#         'productName': 'Item name',
#         'category': 'jewelry',
#         'price': 4.99,
#         'description': 'Some discription',
#         'productImage': 'img.jpg',
#         'is_featured': False,
#         'dateListed': datetime.now(),
#         'quantity': 10,
#     }, {
#         # 'productID': 100003,
#         'productName': 'Item name',
#         'category': 'accessories',
#         'price': 4.99,
#         'description': 'Some discription',
#         'productImage': 'img.jpg',
#         'is_featured': False,
#         'dateListed': datetime.now(),
#         'quantity': 10,
#     }, {
#         # 'productID': 100004,
#         'productName': 'Item name',
#         'category': 'accessories',
#         'price': 4.97,
#         'description': 'Some discription',
#         'productImage': 'img.jpg',
#         'is_featured': True,
#         'dateListed': datetime.now(),
#         'quantity': 10,
#     }, {
#         # 'productID': 100005,
#         'productName': 'Item name',
#         'category': 'accessories',
#         'price': 4.99,
#         'description': 'Some discription',
#         'productImage': 'img.jpg',
#         'is_featured': False,
#         'dateListed': datetime.now(),
#         'quantity': 10,
#     }, {
#         # 'productID': 100006,
#         'productName': 'Item name',
#         'category': 'craft',
#         'price': 5.98,
#         'description': 'Some discription',
#         'productImage': 'img.jpg',
#         'is_featured': True,
#         'dateListed': datetime.now(),
#         'quantity': 10,
#     }, {
#         # 'productID': 100007,
#         'productName': 'Item name',
#         'category': 'craft',
#         'price': 3.98,
#         'description': 'Some discription',
#         'productImage': 'img.jpg',
#         'is_featured': False,
#         'dateListed': datetime.now(),
#         'quantity': 10,
#     }, {
#         # 'productID': 100008,
#         'productName': 'Item name',
#         'category': 'jewelry',
#         'price': 5.98,
#         'description': 'Some discription',
#         'productImage': 'img.jpg',
#         'is_featured': False,
#         'dateListed': datetime.now(),
#         'quantity': 10,
#     }
# ]

# for product in products:
#     Product.objects.create(**product)