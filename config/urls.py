"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path , include

# should'nt be used on Production
from django.conf import settings
from django.conf.urls.static import static

from .views import home_page, about_page, product_page, contact_page, login_page, register_page

from products.views import (
    product_list_view,  
    ProductListView ,
    ProductDetailView,
    product_Detail_view,
    FeaturedProductsDetailView,
    FeaturedProductsListView,
    ProductDetailSlugView,
)

urlpatterns = [
    path('admin/' , admin.site.urls),
    #path('', include ('pages.urls')), 
    path(r'', home_page, name = 'index'),
    path(r'about/', about_page),
    path('products/', product_page),
    path('contact/',contact_page),
    path('login/',login_page , name='login'),
    path('register/',register_page, name = 'register'),


    # for products list template
    path('products-fbv/', product_list_view), # function based view of products,
    path('products-cl/', ProductListView.as_view()),

    # for products Detail template
    path('products-fbv/<pk>/',product_Detail_view, name ='detail'),
    #path('products-cl/<pk>/', ProductDetailView.as_view(), name = 'detail'),

    # for Featured products 
    path('featured-products/',FeaturedProductsListView.as_view()),
    path('featured-products/<pk>/', FeaturedProductsDetailView.as_view(), name='feature'),

    # path for adding slug view
    #path(r'^products-cl/(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name = 'detail')



]


if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL , document_root  = settings.MEDIA_ROOT)