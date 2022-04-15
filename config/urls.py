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

from django.conf.urls import include
from django.contrib import admin
from django.urls import path

# should'nt be used on Production
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
# from carts.views import cart_home, CartHome
from accounts.views import guest_register_view, LoginView, RegisterView #login_page , register_page, 
from .views import home_page, about_page, product_page, contact_page 
from addresses.views import checkout_address_create_view, checkout_address_reuse_view
from carts.views import cart_detail_api_view

urlpatterns = [
    path('admin/' , admin.site.urls),
    #path('', include ('pages.urls')), 
    path(r'', home_page, name = 'home'),
    path(r'about/', about_page, name='about'),
    #path('products/', product_page),
    path('contact/',contact_page,name = 'contact'),
    # path('login/',login_page , name='login'),
    # path('register/',register_page, name = 'register'),
    path('login/',LoginView.as_view() , name='login'),
    path('register/',RegisterView.as_view(), name = 'register'),
    path('guest/register/',guest_register_view, name = 'guest_register'),
    path('logout/',LogoutView.as_view(), name = 'logout'),
    path(r'products/',include(('products.urls','products'),namespace='products')),
    path(r'search/',include(('searchbar.urls','searchbar'),namespace='searchbar')),
    path(r'carts/',include(('carts.urls','carts'),namespace='carts')),
    path('checkout/address/create',checkout_address_create_view, name = 'checkout_address_create'),
    path('checkout/address/reuse',checkout_address_reuse_view, name = 'checkout_address_reuse'),
    #path(r'carts/',include(('carts.urls','carts'),namespace='carts')),
    # path(r'carts/', cart_home,name='cart'),
    # path(r'carts/', CartHome.as_view(),name='cart'),
    path('api/cart/',cart_detail_api_view,name='api-cart')

]


if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL , document_root  = settings.MEDIA_ROOT)