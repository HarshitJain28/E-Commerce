from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),
    path('product/<int:id>', views.detail_product, name='detail-product'),
    path('addtocart/<int:id>', views.add_to_cart, name='add-to-cart'),
    path('removefromcart/<int:id>',
         views.remove_from_cart, name='remove-from-cart'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('order-confirm', views.order_confirm, name='order-confirm'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
