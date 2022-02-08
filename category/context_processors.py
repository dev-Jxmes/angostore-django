from .models import Category

# Function to bring all categories to the app
def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)