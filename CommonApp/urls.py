"""
URL configuration for Code_With_Misha project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

app_name = "CommonApp"
from .views import (index, logout, login, about_us, reviews, catalog, add_item_in_catalog, basket, del_product_in_basket,
                    minus_count_product_in_basket, plus_count_product_in_basket,go_purchase,personal_profile, working,
                    update_status_order_in_worker,register)

urlpatterns = [
    path('', index, name="index"),
    path('logout/', logout,name='go_exit'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('about_us/', about_us, name='about_us'),
    path('reviews/', reviews, name='reviews'),
    path('catalog/', catalog, name='catalog'),
    path('add_item_in_catalog/<str:id_card>/', add_item_in_catalog, name='add_item_in_catalog'),
    path('basket/', basket, name='basket'),
    path('del_product_in_basket/<str:id_product>/', del_product_in_basket, name='del_product_in_basket'),
    path('minus_count_product_in_basket/<str:id_product>/', minus_count_product_in_basket, name='minus_count_product_in_basket'),
    path('plus_count_product_in_basket/<str:id_product>/', plus_count_product_in_basket, name='plus_count_product_in_basket'),
    path('go_purchase/', go_purchase, name='go_purchase'),
    path('personal_profile/', personal_profile, name='personal_profile'),
    path('working/', working, name='working'),
    path('working/update_status/<str:id_order>/', update_status_order_in_worker, name='update_status_order_in_worker'),

]
