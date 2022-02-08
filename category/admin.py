from django.contrib import admin
from .models import Category

# Register your models here.

# function that will make slugField auto-complete
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name', )}
    list_display = ('category_name', 'slug') # To display the data info in admin panel
admin.site.register(Category, CategoryAdmin)
