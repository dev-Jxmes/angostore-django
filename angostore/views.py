from django.shortcuts import render
from store.models import Product

def home(request):
    products = Product.objects.all().filter(is_available=True) # Bring all products that are available

    # Making the products be available in home page
    context = {
        'products': products,
    }
    return render(request, 'home.html', context)