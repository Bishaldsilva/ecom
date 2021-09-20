from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *
from .utils import cookieCart,cartData
from django.contrib import messages
from django.contrib.auth.models import User,auth
import json
# Create your views here.
def store(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    product = Product.objects.all()
    context = {'product':product,'itemNum':len(items)}
    return render(request,'store/store.html',context)

def cart(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    context = {'items':items,'order':order,'itemNum':len(items)}
    return render(request,'store/cart.html',context)

def checkout(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    context = {'items':items,'order':order,'itemNum':len(items)}
    return render(request,'store/checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order,created = Order.objects.get_or_create(customer=customer)
    item,created = OrderItem.objects.get_or_create(order=order,product=product)
    if action=='add':
        item.quantity +=1
    elif action=='remove':
        item.quantity-=1
    item.save()
    if item.quantity<=0:
        item.delete()
    return JsonResponse('Item was added', safe=False)
def login(request):
    if request.method == 'POST':
        un = request.POST['un']
        pass1 = request.POST['pass1']
        user = auth.authenticate(username=un,password=pass1)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Invalid username or password')
            return redirect('login')
    else:
        data = cartData(request)
        items = data['items']
        order = data['order']
        context = {'items':items,'order':order,'itemNum':len(items)}
        return render(request,'store/login.html',context)

def register(request):
    if request.method == 'POST':
        fn=request.POST['fn']
        ln = request.POST['ln']
        un = request.POST['un']
        email = request.POST['em']
        pass1 = request.POST['ps1']
        pass2 = request.POST['ps2']
        if pass1==pass2:
            if User.objects.filter(username=un).exists():  #checking the existence of user
                messages.info(request,'Username taken')
                return redirect('/register')
            else:
                user = User.objects.create_user(username=un, password=pass1, email=email, first_name=fn, last_name=ln)
                user.save()
                customer = Customer.objects.create(user=user,name=fn,email=email)
                customer.save()
        else:
            messages.info(request, 'Password dismatch')
            return redirect('/register')
        return redirect('login')
    else:
        data = cartData(request)
        items = data['items']
        order = data['order']
        context = {'items':items,'order':order,'itemNum':len(items)}
        return render(request,'store/reg.html',context)
def logout(request):
    auth.logout(request)
    return redirect('/')