from django.shortcuts import render, redirect
from ecommerceapp.models import Contact,Product,Orders,OrderUpdate
from django.contrib import messages
from math import ceil
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from math import ceil
import json
from PayTm import Checksum
from . import keys  # Importing keys module
MERCHANT_KEY = keys.MK

# Create your views here.

def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))  # in row 3 products
        allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds}
    return render(request, "index.html", params)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        pnumber = request.POST.get('pnumber')
        desc = request.POST.get('desc')
        myquery = Contact(name=name, email=email, phonenumber=pnumber, desc=desc)
        myquery.save()
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')
    else:
        return render(request, 'contact.html')


def about(request):
    return render(request,"about.html")

def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('/vogue_auth/login/')
    if request.method=="POST":

        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2','')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
         

        Order = Orders(items_json=items_json,name=name,amount=amount, email=email, address1=address1,address2=address2,city=city,state=state,zip_code=zip_code,phone=phone)
        print(amount)
        Order.save()
        update = OrderUpdate(order_id=Order.order_id,update_desc="the order has been placed")
        update.save()
        thank = True

        #Paytm_Integration
        id = Order.order_id
        oid=str(id)+"VogueVerse"
        oid=str(id)
        param_dict = {

            'MID': keys.MID,
            'ORDER_ID': oid,
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'paytm.html', {'param_dict': param_dict})

    return render(request, 'checkout.html')


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    checksum = None  # Initialize checksum to ensure it's defined

    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    if checksum is not None:
        verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
        if verify:
            if response_dict['RESPCODE'] == '01':
                print('order successful')
                a = response_dict['ORDERID']
                b = response_dict['TXNAMOUNT']
                filter2 = Orders.objects.filter(order_id=a)
                print(filter2)
                print(a, b)
                for post1 in filter2:
                    post1.oid = a
                    post1.amountpaid = b
                    post1.paymentstatus = "PAID"
                    post1.save()
                print("run agede function")
            else:
                print('order was not successful because' + response_dict['RESPMSG'])
    else:
        print('CHECKSUMHASH not found in the response')

    return render(request, 'paymentstatus.html', {'response': response_dict})




def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/vogue_auth/login/')
    
    currentuser = request.user.username
    items = Orders.objects.filter(email=currentuser)
    
    for i in items:
        myid = i.oid
        rid = myid.replace("VogueVerse", "")
        
        if rid.isdigit():
            status = OrderUpdate.objects.filter(order_id=int(rid))
        else:
            status = []
        
        # Attach updates to each order instance
        i.updates = status
    
    context = {'items': items}
    return render(request, "profile.html", context)
