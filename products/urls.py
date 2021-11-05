from django.conf.urls import url

from django.contrib import admin
from django.urls import path , include

# should'nt be used on Production
from django.conf import settings
from django.conf.urls.static import static


from .views import(
    product_list_view,  
    ProductListView,
    # ProductDetailView,
    # product_Detail_view,
    FeaturedProductsDetailView,
    FeaturedProductsListView,
    ProductDetailSlugView,
    )

urlpatterns = [
    # for products list template  8000/products/products-fbv/
    path('products-fbv/', product_list_view), # function based view of products,
    # 8000/products/products-cl/
    #path('products-cl/', ProductListView.as_view()),
    # but for this one we can just write on url : 8000/products/
    path('', ProductListView.as_view()),

    # for products Detail template
    #path('products-fbv/<pk>/',product_Detail_view, name ='detail'),
    #path('products-cl/<pk>/', ProductDetailView.as_view(), name = 'detail'),

    # for Featured products 
    # 8000/products/featured-products/DellComputer/
    path('featured-products/',FeaturedProductsListView.as_view()),
    # path('featured-products/<pk>/', FeaturedProductsDetailView.as_view(), name='feature'),
    path('featured-products/<slug>/', FeaturedProductsDetailView.as_view(), name='feature'),

    # path for adding slug view
    # typically we can write:  8000/products/DellComputer/
    path(r'<slug>/', ProductDetailSlugView.as_view(), name = 'detail'),
]
