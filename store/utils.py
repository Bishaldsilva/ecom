import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart={}
    items=[]
    order = {'get_abs_items':0,'get_abs_total':0}
    for i in cart:
        try:
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])
            order['get_abs_total'] += total
            order['get_abs_items'] +=cart[i]['quantity']
            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'image':product.image
                    },
                'quantity':cart[i]['quantity'],
                'get_total':total
            }
            items.append(item)
        except:
            pass
    return {'items':items,'order':order,'itemNum':len(items)}
def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer)
        items = order.orderitem_set.all()
    else:
        cookiedata = cookieCart(request)
        items = cookiedata['items']
        order = cookiedata['order']
    return {'items':items,'order':order,'itemNum':len(items)}