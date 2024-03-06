from django.shortcuts import render,get_object_or_404
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage,InvalidPage

# Create your views here.
def home(request,c_slug=None):
    c_page=None
    prodt_list=None
    if c_slug!=None:
        c_page=get_object_or_404(category,slug=c_slug)
        prodt_list=product.objects.filter(category=c_page,available=True)
    else:
        prodt_list=product.objects.all().filter(available=True)
        paginator=Paginator(prodt_list,4)
        try:
            page=int(request.GET.get('page','1'))
        except:
            page=1
        try:
            prodt_list=paginator.page(page)
        except (EmptyPage,InvalidPage):
           prodt_list=paginator.page(paginator.num_pages)
    cat=category.objects.all()
    # obj=product.objects.all()
    return render(request,'index.html',{'product':prodt_list,'ct':cat})



def proddetails(request,c_slug,p_slug):
    try:
        prod=product.objects.get(category__slug=c_slug,slug=p_slug)
    except Exception as e:
        raise e
    return render(request,'product.html',{'pr':prod})



def search(request):
    prod=None
    query=None
    if 'search' in request.GET:
        query=request.GET.get('search')
        prodt=product.objects.all().filter(Q(name__contains=query)|Q(desc__contains=query)|Q(price__contains=query))
    return render(request,"search.html",{'qr':query,'product':prodt})