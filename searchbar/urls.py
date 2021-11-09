from django.urls import path
from .views import( 
    ProductsSearchView,
    )

urlpatterns = [
    path('', ProductsSearchView.as_view(), name='query'),


]
