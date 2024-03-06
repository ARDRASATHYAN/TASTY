from django.urls import path

from cartapp import views

urlpatterns = [
    path('cartdetail',views.cart,name='cartdetail'),
    path('place_order',views.place_order, name='place_order'),
    path('addcart/<int:pro_id>/',views.add_cart,name='addcart'),
    path('min/<int:pro_id>/',views.min_cart,name='min'),
    path('remove/<int:pro_id>/',views.delete_cart,name='remove'),
]