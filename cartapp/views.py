from django.shortcuts import render,redirect,get_object_or_404
from homeapp.models import *
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse


# Create your views here.
def cart(request,total=0,count=0,cart_items=None):
    ct_items = None
    try:
        ct=cartlist.objects.get(cartid=c_id(request))
        ct_items=items.objects.filter(cart=ct,active=True)
        for i in ct_items:
            total+=(i.prodt.price*i.quantity)
            count+=i.quantity
    except ObjectDoesNotExist:
        pass        
    return render(request,'card.html',{'ci':ct_items, 't':total, 'cn':count})

def c_id(request):
    ct_id=request.session.session_key
    if not ct_id:
        ct_id=request.session.create()
    return ct_id

def add_cart(request, pro_id):
    prod = product.objects.get(id=pro_id)
    try:
        ct = cartlist.objects.get(cartid=c_id(request))
    except cartlist.DoesNotExist:
        ct = cartlist.objects.create(cartid=c_id(request))
        ct.save()
    
    try:  
        c_items = items.objects.get(prodt=prod, cart=ct)
        if c_items.quantity < c_items.prodt.stock:
            c_items.quantity += 1
        c_items.save()
    except items.DoesNotExist:
        # Associate the user with the cart item when creating
        c_items = items.objects.create(prodt=prod, quantity=1, cart=ct, user=request.user)
        c_items.save()

    return redirect('cartdetail')

# def add_cart(request,pro_id):
#     prod=product.objects.get(id=pro_id)
#     try:
#         ct=cartlist.objects.get(cartid=c_id(request))
#     except cartlist.DoesNotExist:
#         ct=cartlist.objects.create(cartid=c_id(request))
#         ct.save()
#     try:  
#         c_items=items.objects.get(prodt=prod,cart=ct)
#         if c_items.quantity < c_items.prodt.stock:
#             c_items.quantity+=1
#         c_items.save()
#     except items.DoesNotExist:
#         c_items=items.objects.create(prodt=prod,quantity=1,cart=ct)
#         c_items.save()
#     return redirect('cartdetail')    



def min_cart(request,pro_id):
    card=cartlist.objects.get(cartid=c_id(request))
    produt=get_object_or_404(product,id=pro_id)
    c_items=items.objects.get(prodt=produt,cart=card)
    if c_items.quantity>1:
        c_items.quantity-=1
        c_items.save()
    else:
        c_items.delete()
    return redirect('cartdetail')


def delete_cart(request,pro_id):
    card=cartlist.objects.get(cartid=c_id(request))
    produt=get_object_or_404(product,id=pro_id)
    c_items=items.objects.get(prodt=produt,cart=card)
    c_items.delete()  
    return redirect('cartdetail') 

def place_order(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page if the user is not authenticated

    # Get the user's cart items
    cart_items = items.objects.filter(user=request.user)
    print("Debug: User's Cart Items -", cart_items.count())

    # Check if there are items in the cart
    if cart_items.exists():
        # Create an order with the cart items
        order = Order.objects.create(user=request.user)
        print("Debug: User's Cart order -", order)

        # Create order items
        for item in cart_items:
            order_items = OrderItem.objects.create(
                order=order, 
                product=item.prodt, 
                quantity=item.quantity, 
                total=item.total()
            )
            

             # Update product stock
            item.prodt.stock -= item.quantity
            item.prodt.save()
            print(f"Debug: Updated stock. New stock: {item.prodt.stock}")


            print("Debug: User's Cart order yyy-", item.user)

        # Clear the user's cart
        cart_items.delete()

        # Calculate the total order amount
        order_total = order.calculate_order_total()


        # You can add additional logic here, such as sending an order confirmation email, etc.

        return render(request, 'order_confirmation.html', {'order': order,'order_total': order_total})
    else:
        return render(request, 'empty_cart.html')  # Render a page for an empty cart

# def place_order(request):
    
#     # Check if the user is authenticated
#     if not request.user.is_authenticated:
#         return redirect('login')  # Redirect to the login page if the user is not authenticated

#     # Get the user's cart items
#     cart_items = items.objects.filter(user=request.user)
#     print("Debug: User's Cart Items -", cart_items.count())
#     # Create an order with the cart items
#     order = Order.objects.create(user=request.user)
#     print("Debug: User's Cart order -", order)
#     for item in cart_items:
#         order_items = order.orderitem_set.create(product=item.prodt, quantity=item.quantity, total=item.total)
#         print("Debug: User's Cart order yyy-", item.user)
#     # Clear the user's cart
#     cart_items.delete()

#     # You can add additional logic here, such as sending an order confirmation email, etc.

#     return render(request, 'order_confirmation.html', {'order': order})





