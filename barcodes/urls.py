"""
URL configuration for barcodes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path

import barcodes.views
from .views import add_product, product_detail, all_products, search_product_by_barcode, delete_product, edit_product, \
  search_and_add_to_cart, cart_view, handlelogin, handlelogout, handlesignup, checkout_view

urlpatterns = [
  path('admin/', admin.site.urls),
  path('add/', add_product, name='add_product'),
  path('product/<str:barcode>/', product_detail, name='product_detail'),
  path('all/', all_products, name='all_products'),
  path('search/', search_product_by_barcode, name='search_product_by_barcode'),
  path('delete/<str:barcode>/', delete_product, name='delete_product'),
  path('edit/<str:barcode>/', edit_product, name='edit_product'),
  path('search_and_add_to_cart/<str:barcode>/', search_and_add_to_cart, name='search_and_add_to_cart'),
  path('cart/', cart_view, name='cart_view'),
  path('login', barcodes.views.handlelogin, name='handlelogin'),
  path('logout', barcodes.views.handlelogout, name='handlelogout'),
  path('', barcodes.views.handlesignup, name='handlesignup'),
  path('checkout/', checkout_view, name='checkout'),

]
