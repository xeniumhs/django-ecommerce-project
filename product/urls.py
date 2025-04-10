from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'product'

urlpatterns=[
    path('', views.home , name='home'),
    path('all_products/', views.product_list, name='product_list'),
    path('add/', views.add , name='add'),
    path('home/', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('add_category/', views.add_category , name='add_category'),
    path('product/<int:id>/', views.product_details, name='product_details'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('delete/<int:id>/',views.delete,name='delete'),
    path('about/', views.about , name='about'),
    path('search/', views.search, name='search'),
    path('inventory/', views.inventory, name='inventory'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    
    path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('my-orders/', views.customer_orders, name='order_history'),
    path("order/<int:order_id>/", views.order_details, name="order_details"),
    path('orders/', views.order_list, name='order_list'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)