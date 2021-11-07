from django.conf.urls import url

from django.contrib import admin
from django.urls import path , include, re_path

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
    path('products-fbv/', product_list_view,name = 'fbv-list'), # function based view of products,
    # 8000/products/products-cl/
    #path('products-cl/', ProductListView.as_view()),
    # but for this one we can just write on url : 8000/products/
    path('', ProductListView.as_view(), name='list'),

    # for products Detail template
    #path('products-fbv/<pk>/',product_Detail_view, name ='detail'),
    #path('products-cl/<pk>/', ProductDetailView.as_view(), name = 'detail'),

    # for Featured products 
    # 8000/products/featured-products/DellComputer/
    path(r'featured-products/',FeaturedProductsListView.as_view(),name= 'feature-list'),
    # path('featured-products/<pk>/', FeaturedProductsDetailView.as_view(), name='feature'),
    re_path(r'^featured-products/(?P<slug>[\w-]+)/$', FeaturedProductsDetailView.as_view(), name='feature'),

    # path for adding slug view
    # typically we can write:  8000/products/DellComputer/
    re_path(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name='detail'),
]
