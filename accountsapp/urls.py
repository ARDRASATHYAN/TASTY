from django.urls import path

from accountsapp import views

urlpatterns = [
    path('',views.register,name='accounts'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
]