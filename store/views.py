from ast import keyword
from email import message
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import is_valid_path

from category.models import Category
from .models import Product, ReviewRating
from .forms import ReviewForm
from category.models import Category
from carts.views import _cart_id
from carts.models import CartItem
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator # Work with pagination
from django.contrib import messages
from orders.models import OrderProduct

# Create your views here.

def store(request, category_slug=None): 
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug) # bring the category , otherwise the error 404
        products = Product.objects.filter(category=categories, is_available=True)        
        paginator = Paginator(products, 1) # pass the product var. and the number of item for display in each page
        page = request.GET.get('page') # page redirect , like page=1/2/...
        paged_products = paginator.get_page(page) # the six products will be stored here
        product_count = products.count() # Count the products     
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id') # Bring all products that are available
        paginator = Paginator(products, 3) # pass the product var. and the number of item for display in each page
        page = request.GET.get('page') # page redirect , like page=1/2/...
        paged_products = paginator.get_page(page) # the six products will be stored here
        product_count = products.count() # Count the products

    # Making the products be available in store page
    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug) # getting the slug of category
        # Checking if the product is in the cart 
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()  #cart__cart_id , cuz in models cart is a foreign_key and we want to access the cart_id in the same model
    except Exception as e:
        raise e

    # Verify if the product is ordered to show the review button
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    # Get the reviews
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)


    context = {
        'single_product': single_product,
        'in_cart'       : in_cart,
        'orderproduct'  : orderproduct,
        'reviews'       : reviews,
    }   
    return render(request, 'store/product_detail.html', context)


# Search Function
def search(request):
    if 'keyword' in request.GET: # verifying if the word keyword exists, if true will store the value store in keyword variable
        keyword = request.GET['keyword']
        if keyword: # if got some value, than...
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword)) # description__icontains=keyword >> will look for all description and if found something related to this keyword will bring it and show
            product_count = products.count()
        context = {
            'products': products,
            'product_count': product_count,
        }
    return render(request, 'store/store.html', context)


# Submit Review 
def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submited.')
                return redirect(url)

