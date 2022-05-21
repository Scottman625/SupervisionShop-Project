from calendar import month
from django.shortcuts import render ,redirect,get_object_or_404
from django.http import HttpResponse
import requests
from modelCore.models import User , Category, Product , ProductImage , SupervisionOffice , ProductSupervisionOfficeShip ,Order ,ProductOrderShip,PayInfo , ShoppingCart ,OrderState,image_upload_handler
from modelCore.forms import *
import urllib 
from django.db.models import Sum
from datetime import datetime, timedelta

# Create your views here.

def index(request):
    orders = Order.objects.filter(state=1)
    ships = ProductOrderShip.objects.all()
    products =Product.objects.all()
    undealtorders = Order.objects.filter(state=1)
    UndealtOrdersNum = undealtorders.count()
    dealtOrdersShips = Order.objects.filter(state=2)
    last7Days = (datetime.today() - timedelta(days=7)).date()
    last6Days = (datetime.today() - timedelta(days=6)).date()
    last5Days = (datetime.today() - timedelta(days=5)).date()
    last4Days = (datetime.today() - timedelta(days=4)).date()
    last3Days = (datetime.today() - timedelta(days=3)).date()
    last2Days = (datetime.today() - timedelta(days=2)).date()
    last1Days = (datetime.today() - timedelta(days=1)).date()
    WeekOrders = dealtOrdersShips.filter(createDate__date__gte=last7Days)
    last7DaysOrders = dealtOrdersShips.filter(createDate__date=last7Days)
    last6DaysOrders = dealtOrdersShips.filter(createDate__date=last6Days)
    last5DaysOrders = dealtOrdersShips.filter(createDate__date=last5Days)
    last4DaysOrders = dealtOrdersShips.filter(createDate__date=last4Days)
    last3DaysOrders = dealtOrdersShips.filter(createDate__date=last3Days)
    last2DaysOrders = dealtOrdersShips.filter(createDate__date=last2Days)
    last1DaysOrders = dealtOrdersShips.filter(createDate__date=last1Days)
    sum7=0
    sum6=0
    sum5=0
    sum4=0
    sum3=0
    sum2=0
    sum1=0
    sum7Money=0 
    sum6Money=0
    sum5Money=0
    sum4Money=0
    sum3Money=0
    sum2Money=0
    sum1Money=0
    for last7DaysOrder in last7DaysOrders:
        ships7 = ships.filter(order=last7DaysOrder)
        for ship in ships7:
            sum7 += ship.amount
            sum7Money += ship.product.price * ship.amount
    for last6DaysOrder in last6DaysOrders:
        ships6 = ships.filter(order=last6DaysOrder)
        for ship in ships6:
            sum6 += ship.amount
            sum6Money += ship.product.price * ship.amount
    for last5DaysOrder in last5DaysOrders:
        ships5 = ships.filter(order=last5DaysOrder)
        for ship in ships5:
            sum5 += ship.amount
            sum5Money += ship.product.price * ship.amount
    for last4DaysOrder in last4DaysOrders:
        ships4 = ships.filter(order=last4DaysOrder)
        for ship in ships4:
            sum4 += ship.amount
            sum4Money += ship.product.price * ship.amount
    for last3DaysOrder in last3DaysOrders:
        ships3 = ships.filter(order=last3DaysOrder)
        for ship in ships3:
            sum3 += ship.amount
            sum3Money += ship.product.price * ship.amount
    for last2DaysOrder in last2DaysOrders:
        ships2 = ships.filter(order=last2DaysOrder)
        for ship in ships2:
            sum2 += ship.amount
            sum2Money += ship.product.price * ship.amount
    for last1DaysOrder in last1DaysOrders:
        ships1 = ships.filter(order=last1DaysOrder)
        for ship in ships1:
            sum1 += ship.amount
            sum1Money += ship.product.price * ship.amount
    for product in products:
        sum = 0
        for WeekOrder in WeekOrders:
            OrderShips=ships.filter(order=WeekOrder,product=product)       
            for OrderShip in OrderShips:
                sum += OrderShip.amount                 
        product.week_sum_nums = sum      
        product.save()   
    print(sum7Money)
    productRank = Product.objects.order_by("-week_sum_nums")[:3]
    
    return render(request, 'backboard/index.html',{'sum7Money':sum7Money,'sum6Money':sum6Money,'sum5Money':sum5Money,'sum4Money':sum4Money,'sum3Money':sum3Money,'sum2Money':sum2Money,'sum1Money':sum1Money, 'sum1':sum1,'sum2':sum2,'sum3':sum3,'sum4':sum4,'sum5':sum5,'sum6':sum6,'sum7':sum7, 'last6Days':last6Days,'last5Days':last5Days,'last4Days':last4Days ,'last3Days':last3Days,'last2Days':last2Days,'last1Days':last1Days, 'last7Days':last7Days, 'orders':orders,'UndealtOrdersNum':UndealtOrdersNum,'productRank':productRank})

def base(request):
    return render(request, 'backboard/base.html')


def bills(request):
    offices = SupervisionOffice.objects.all()
    orders=Order.objects.filter(state=2)
    TotalOrder = orders.count()
    TotalMoney = 0
    for order in orders:
        TotalMoney += order.orderMoney
    officeOrders1 =  orders.filter(supervisionOffice=1)
    officeTotalorder1 = officeOrders1.count()
    officeTotalMoney1 = 0
    for officeOrder1 in officeOrders1:
        officeTotalMoney1 += officeOrder1.orderMoney
    officeOrders2 =  orders.filter(supervisionOffice=2)
    officeTotalorder2 = officeOrders2.count()
    officeTotalMoney2 = 0
    for officeOrder2 in officeOrders2:
        officeTotalMoney2 += officeOrder2.orderMoney
    officeOrders3 =  orders.filter(supervisionOffice=3)
    officeTotalorder3 = officeOrders3.count()
    officeTotalMoney3 = 0
    for officeOrder3 in officeOrders3:
        officeTotalMoney3 += officeOrder3.orderMoney
    
    today = datetime.today()
    current_month = today.month
    current_year = today.year
    this_month = Order.objects.filter(createDate__year=current_year,
                           createDate__month=current_month)
    
    d = {}
    for i in range(current_month):
        num = current_month -i
        if num > 0:
            d['last'+str(i)+'Months'] = Order.objects.filter(createDate__year=current_year,
                           createDate__month=num)
    
    return render(request, 'backboard/bills.html',{ 'current_month':current_month,'current_year':current_year, 'd':d,'this_month':this_month,'offices':offices, 'TotalOrder':TotalOrder,'TotalMoney':TotalMoney,'officeTotalorder1':officeTotalorder1,'officeTotalMoney1':officeTotalMoney1,'officeTotalorder2':officeTotalorder2,'officeTotalMoney2':officeTotalMoney2,"officeTotalorder3":officeTotalorder3,"officeTotalMoney3":officeTotalMoney3})

def customers(request):
    customers = User.objects.all()
    
    for customer in customers:
        
        customer_id=customer.id
    return render(request, 'backboard/customers.html',{'customers':customers,'customer_id':customer_id})

def customer_detail(request):
    customers = User.objects.all()
    orders = Order.objects.all()
    customer_id = request.GET.get('customer_id','')
    customers = customers.filter(id=customer_id)
    
    for order in orders:
        if order.user == customers.get(id=customer_id):
                order_id = order.id
    return render(request, 'backboard/customer_detail.html',{'orders':orders,'customers':customers,'order_id':order_id})

def orders(request):
    
    
    orders = Order.objects.all()
    users = User.objects.all()
    orderstates = OrderState.objects.all()
    q = request.GET.get('order_state')
    if q != None:
        theOrderstates = orderstates.filter(id=request.GET.get('order_state'))        
    else:
        theOrderstates = orderstates
   
    for order in orders:
        IdOder=order.id
 
    return render(request, 'backboard/orders.html',{'orders':orders,'users':users,'IdOder':IdOder,'orderstates':orderstates,'theOrderstates':theOrderstates})
    

def order_detail(request):
    orders = Order.objects.all()
    users = User.objects.all()
    payinfos=PayInfo.objects.all()
    orderstates = OrderState.objects.all()
    products=Product.objects.all()
    ships = ProductOrderShip.objects.all()
    
    order_id=request.GET.get('IdOrder')
    orders = orders.filter(id=order_id)
    sum = 0
    for order in orders:
        for ship in ships:
            if ship.order == order:
                sum += order.orderMoney

 
    if order_id != None:        
        
        theOrder = Order.objects.get(id=order_id)
    else:
        print('order_id:',order_id)
        theOrder = Order.objects.get(id=order_id)
    
    if request.method == 'POST':
        
        State_Id = request.POST.get('OrderState')
        
        theOrder.state = OrderState.objects.get(id=State_Id)
        theOrder.save()

        return redirect('/backboard/orders')

    return render(request, 'backboard/order_detail.html',{'orders':orders,'users':users,'payinfos':payinfos,'products':products,'orderstates':orderstates,'ships':ships,'sum':sum})


def products(request):
    products = Product.objects.all()
    ships = ProductSupervisionOfficeShip.objects.all()
    productimages = ProductImage.objects.all()
    
    # for product in products:
    #     product.image = ProductImage.objects.all().first()
    #     print(product.image)

    return render(request, 'backboard/products.html',{'products':products,'ships':ships,'productimages':productimages})


def offices_order(request):
    offices_all = SupervisionOffice.objects.all()
    ships = ProductOrderShip.objects.all()
    office_Id = request.GET.get('OfficeId')
    orders =  Order.objects.filter(supervisionOffice=office_Id)
    offices = offices_all.filter(id=office_Id)
    sum = 0
    for order in orders:
            sum += order.orderMoney

    print(sum)


    
    return render(request,'backboard/offices_order.html',{'ships':ships,'orders':orders,'offices':offices,'sum':sum})


def add_new_product(request):

    supervisionoffices = SupervisionOffice.objects.all()
    categories = Category.objects.all()
    form = ProductImageForm()

    product = Product()
       

    if request.method == 'POST':

            
            
            form = ProductImageForm(request.POST, request.FILES)
            productName = request.POST.get('productName') 
            product.name = productName
            category_Id = request.POST.get('productCategory')
            product.category = Category.objects.get(id=category_Id)
            product.sublabel =request.POST.get('productSublabel')
            product.info = request.POST.get('productInfo')
            product.content = request.POST.get('productContent')
            product.price = request.POST.get('productPrice')
            product.unit =request.POST.get('productUnit')
            product.stocks = request.POST.get('productStock')
            product.isPublish = request.POST.get('productIspublish')
            product.save()
            products = Product.objects.filter(name=productName)
            
            
            ship_officeId1 =request.POST.get('ship_officeId1')
            ship_officeId2 =request.POST.get('ship_officeId2')
            ship_officeId3 =request.POST.get('ship_officeId3')
            
            if ship_officeId1 == "1":
                productsupervisionOfficeship = ProductSupervisionOfficeShip()
                productsupervisionOfficeship.supervisionOffice = SupervisionOffice.objects.get(id=ship_officeId1)
                productsupervisionOfficeship.product = product
                productsupervisionOfficeship.save()

            if ship_officeId2 == "2":
                productsupervisionOfficeship = ProductSupervisionOfficeShip()
                productsupervisionOfficeship.supervisionOffice = SupervisionOffice.objects.get(id=ship_officeId2)
                productsupervisionOfficeship.product = product
                productsupervisionOfficeship.save()

            if ship_officeId3 == "3":
                productsupervisionOfficeship = ProductSupervisionOfficeShip()
                productsupervisionOfficeship.supervisionOffice = SupervisionOffice.objects.get(id=ship_officeId3)
                productsupervisionOfficeship.product = product
                productsupervisionOfficeship.save()

            

            
            if form.is_valid():
                
                form.save()
                # Get the current instance object to display in the template
                img_obj = form.instance
                print('1')
                # form.initial['product'] = Product.objects.latest('id')
                theproductImage=ProductImage.objects.latest('id')
                theproductImage.product=Product.objects.latest('id')
                theproductImage.save()
                render(request, 'backboard/add_new_product.html',{'supervisionoffices':supervisionoffices,'categories':categories,'products':products, 'form':form, 'img_obj': img_obj})
    else:
        form = ProductImageForm()
        form.initial['product'] = Product.objects.latest('id')
        print('2')
    return render(request, 'backboard/add_new_product.html',{'supervisionoffices':supervisionoffices,'categories':categories, 'form':form})
        

    

   

def edit_product(request):
    
    products = Product.objects.all()
    form = ProductImageForm()
    productId = request.GET.get("productId")
    supervisionoffices = SupervisionOffice.objects.all()
    categories = Category.objects.all()
    ProductQueryset = Product.objects.filter(id=productId)
    theproduct = Product.objects.get(id=productId)
    productships = ProductSupervisionOfficeShip.objects.filter(product=theproduct)
    ship1 = ProductSupervisionOfficeShip.objects.filter(product=theproduct,supervisionOffice=1)
    ship2 = ProductSupervisionOfficeShip.objects.filter(product=theproduct,supervisionOffice=2)
    ship3 = ProductSupervisionOfficeShip.objects.filter(product=theproduct,supervisionOffice=3)
    productimages = ProductImage.objects.filter(product=theproduct).order_by('-id')[:6]
    for ship in productships:
        print(ship.supervisionOffice.id)
  
    if request.method == 'POST':
      
        if theproduct.name == request.POST.get('productName'):
            form = ProductImageForm(request.POST, request.FILES)
            product = Product.objects.get(id=productId)
            category_Id = request.POST.get('productCategory')
            product.category = Category.objects.get(id=category_Id)
            product.sublabel =request.POST.get('productSublabel')
            product.info = request.POST.get('productInfo')
            product.content = request.POST.get('productContent')
            product.price = request.POST.get('productPrice')
            product.unit =request.POST.get('productUnit')
            product.stocks = request.POST.get('productStock')
            product.isPublish = request.POST.get('productIspublish')
            product.save()
            
            
            officeId1=request.POST.get('ship_officeId1')
            officeId2=request.POST.get('ship_officeId2')
            officeId3=request.POST.get('ship_officeId3')
            
            
            
            
            
            
            if officeId1 == "1" :
                print("officeId1:",officeId1)
                if ship1.exists() :
                    print('pass1')
                    pass
                else:
                    print('add ship1')
                    productsupervisionOfficeship = ProductSupervisionOfficeShip()
                    productsupervisionOfficeship.supervisionOffice = SupervisionOffice.objects.get(id=1)
                    productsupervisionOfficeship.product = product
                    productsupervisionOfficeship.save()

            else:
                if ship1.exists() :
                    print('delete ship1')
                    ship1.delete()
                else:
                    print('pass2')
                    pass



            if officeId2 == "2" :
                print("officeId2:",officeId2)
                if ship2.exists() :
                    print('pass1')
                    pass
                else:
                    print('add ship2')
                    productsupervisionOfficeship = ProductSupervisionOfficeShip()
                    productsupervisionOfficeship.supervisionOffice = SupervisionOffice.objects.get(id=2)
                    productsupervisionOfficeship.product = product
                    productsupervisionOfficeship.save()

            else:
                if ship2.exists() :
                    print('delete ship2')
                    ship2.delete()
                else:
                    print('pass2')
                    pass

            if officeId3 == "3" :
                print("officeId3:",officeId3)
                if ship3.exists() :
                    print('pass1')
                    pass
                else:
                    print('add ship3')
                    productsupervisionOfficeship = ProductSupervisionOfficeShip()
                    productsupervisionOfficeship.supervisionOffice = SupervisionOffice.objects.get(id=3)
                    productsupervisionOfficeship.product = product
                    productsupervisionOfficeship.save()

            else:
                if ship3.exists() :
                    print('delete ship3')
                    ship3.delete()
                else:
                    print('pass2')
                    pass

            if form.is_valid():
                
                form.save()
                # Get the current instance object to display in the template
                img_obj = form.instance
                print('1')
                # form.initial['product'] = Product.objects.latest('id')
                theproductImage=ProductImage.objects.latest('id')
                theproductImage.product=theproduct
                theproductImage.save()
                render(request, 'backboard/add_new_product.html',{'supervisionoffices':supervisionoffices,'categories':categories,'productships':productships,'products':products,'productId':productId,'ProductQueryset':ProductQueryset,'form':form, 'img_obj': img_obj})


        elif Product.objects.filter(name=request.POST.get('productName')).exists() == False :
            form = ProductImageForm(request.POST, request.FILES)
            product = Product.objects.get(id=productId)
            product.name = request.POST.get('productName')
            category_Id = request.POST.get('productCategory')
            product.category = Category.objects.get(id=category_Id)
            product.sublabel =request.POST.get('productSublabel')
            product.info = request.POST.get('productInfo')
            product.content = request.POST.get('productContent')
            product.price = request.POST.get('productPrice')
            product.unit =request.POST.get('productUnit')
            product.stocks = request.POST.get('productStock')
            product.isPublish = request.POST.get('productIspublish')
            product.save()
                        
            officeId1=request.POST.get('ship_officeId1')
            officeId2=request.POST.get('ship_officeId2')
            officeId3=request.POST.get('ship_officeId3')
                     
            if officeId1 == "1" :
                print("officeId1:",officeId1)
                if ship1.exists() :
                    print('pass1')
                    pass
                else:
                    print('add ship1')
                    productsupervisionOfficeship = ProductSupervisionOfficeShip()
                    productsupervisionOfficeship.supervisionOffice = SupervisionOffice.objects.get(id=1)
                    productsupervisionOfficeship.product = product
                    productsupervisionOfficeship.save()

            else:
                if ship1.exists() :
                    print('delete ship1')
                    ship1.delete()
                else:
                    print('pass2')
                    pass

            if officeId2 == "2" :
                print("officeId2:",officeId2)
                if ship2.exists() :
                    print('pass1')
                    pass
                else:
                    print('add ship2')
                    productsupervisionOfficeship = ProductSupervisionOfficeShip()
                    productsupervisionOfficeship.supervisionOffice = SupervisionOffice.objects.get(id=2)
                    productsupervisionOfficeship.product = product
                    productsupervisionOfficeship.save()

            else:
                if ship2.exists() :
                    print('delete ship2')
                    ship2.delete()
                else:
                    print('pass2')
                    pass

            if officeId3 == "3" :
                print("officeId3:",officeId3)
                if ship3.exists() :
                    print('pass1')
                    pass
                else:
                    print('add ship3')
                    productsupervisionOfficeship = ProductSupervisionOfficeShip()
                    productsupervisionOfficeship.supervisionOffice = SupervisionOffice.objects.get(id=3)
                    productsupervisionOfficeship.product = product
                    productsupervisionOfficeship.save()

            else:
                if ship3.exists() :
                    print('delete ship3')
                    ship3.delete()
                else:
                    print('pass2')
                    pass
            
            if form.is_valid():
                
                form.save()
                # Get the current instance object to display in the template
                img_obj = form.instance
                print('1')
                # form.initial['product'] = Product.objects.latest('id')
                theproductImage=ProductImage.objects.latest('id')
                theproductImage.product=Product.objects.get(id=productId)
                theproductImage.save()
                render(request, 'backboard/add_new_product.html',{'supervisionoffices':supervisionoffices,'categories':categories,'productships':productships,'products':products,'productId':productId,'ProductQueryset':ProductQueryset,'form':form, 'img_obj': img_obj})


    else:
        form = ProductImageForm()
        form.initial['product'] = theproduct
        print('2')
    
    return render(request, 'backboard/edit_product.html',{'supervisionoffices':supervisionoffices,'productimages':productimages,'categories':categories,'productships':productships,'products':products,'productId':productId,'ProductQueryset':ProductQueryset,'form':form})

def redirect_params(url, params=None):
    response = redirect(url)
    if params:
        query_string = urllib.parse.urlencode(params)
        response['Location'] += '?' + query_string
    return response

def deleteImage(request, id=None):
    image = get_object_or_404(ProductImage, pk=id)
    ID = image.product.id
    your_params = {
        'productId':ID
    }
    image.delete()

    
    return redirect_params("/backboard/edit_product",your_params)

