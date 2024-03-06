from django.urls import path

from homeapp import views

urlpatterns = [
    path('home',views.home,name='home'),
    path('<slug:c_slug>/',views.home,name='prod_cat'),
    path('<slug:c_slug>/<slug:p_slug>',views.proddetails,name='details'),
    path('search',views.search,name='search')
]