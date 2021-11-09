from django.db.models import Q  # can search data not just in titles but with different fields
from django.shortcuts import render
from django.views.generic import ListView
from products.models import Product
# Create your views here.

#class based view for feature list products
class ProductsSearchView(ListView):
    # template_name = 'product/list.html'
    template_name = 'search/view_search.html'
    # this section make a name for self.request.GET.get('q') like query to be used on view_search.html
    def get_context_data(self, *args, **kwargs):
        context = super(ProductsSearchView,self).get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        print(request.GET.get('q'))
        # request.GET returns the key on of dictionary
        # q is recieving the get value on search bar; so anythin not found, don't show anything
        # Or we can pass a default like shirt on below, but not necessary
        query = request.GET.get('q','shirt')

        if query is not None:
            # this lookups method is useful but till it is model's job so we transferred lookups to search func in  products models
            # lookups = Q(title__icontains = query) | Q(description__icontains = query)| Q(price__icontains = query)
            # This below line is before lookups method to search for an object containing just titles
            # return Product.objects.filter(title__icontains= query)
            # return Product.objects.filter(lookups).distinct() 
            return Product.objects.search(query)
            # distinct() prevents from returning an object for twice if object finded on title and description
        # return Product.objects.none()
        return Product.objects.featured()