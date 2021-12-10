from django.shortcuts import render
from django.http import Http404
# Create your views here.
from .models import Product, ProductManager
from django.views.generic import ListView , DetailView
from carts.models import Cart
from django.core.paginator import Paginator
# import custom user defined signals use them so that when user see any product can be detected 
from analytics.mixins import ObjectViewedMixin

#class based view for listing products
class ProductListView(ListView):
    # queryset = Product.objects.all()
    template_name = 'product/list.html'
    paginate_by = 2
    

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        # print(context)
        context['cart'] = cart_obj
    
        return context
    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()


# Function base view for listing products:
def product_list_view(request):
    queryset = Product.objects.all()
    """On 21st  line we can change the name of object_list to anything but it be object_list when we 
    work with class based view but if we work with function based views not necessary to pass the 
    data with anyname"""
    Product_list = {
        'object_list' : queryset
    }
    # we can also send the data to index.html on outer templates but not to other pages of out one
    #return render(request , 'index.html',Product_list)
    return render (request, 'product/list.html',Product_list)


#class based detail view for listing products:

class ProductDetailView(ObjectViewedMixin,DetailView):
    queryset = Product.objects.all()
    template_name = 'product/detail.html'


    """This code is just for recognizing that how we can get the data with which name,
    Which in this place it shows (object) and that's why we retrieved the data with object : like
    object.title or object.description"""
    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        # print(context)
        #context['object_list'] = queryset
        return context



# Function base detail view for listing products:
def product_Detail_view(request,pk):
    #queryset = Product.objects.all()
    #queryset1 = Product.objects.get(id = pk)
    try:
        queryset1 = Product.objects.get(id = pk)
    except Product.DoesNotExist:
        print('No Product Here')
        raise Http404('Product Does Not Exist have you seen')
    except:
        print('nothing for finally')
    Product_list = {
        
        'object' : queryset1
    }
    # we can also send the data to index.html on outer templates but not to other pages of out one
    #return render(request , 'index.html',Product_list)
    return render (request, 'product/detail.html',Product_list)



#class based view for feature list products
class FeaturedProductsListView(ListView):
    template_name = 'product/feature_list.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.featured()


# class base view for featured products' details with their identity number on url

class FeaturedProductsDetailView(ObjectViewedMixin,DetailView):
    template_name = 'product/feature.html'
    
    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.featured()


# class for showing products with their names on url
class ProductDetailSlugView(ObjectViewedMixin, DetailView):
    queryset = Product.objects.all()
    template_name = 'product/detail.html'
    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')

        try:
            instance = Product.objects.get(slug = slug,active = True)
        except Product.DoesNotExist:
            raise Http404('Not found')
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug = slug , active = True)
            instance = qs.first()
        except:
            raise Http404('so may it exists')

        # object_viewed_signal.send(instance.__class__, instance=instance, request=request)
        return instance