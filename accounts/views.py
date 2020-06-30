from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.forms import inlineformset_factory
from .filters import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group

# Create your views here.

@unauthenticated_user
def registerPage(request):
    
    form=CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username')#Recuperation des données lorqu'on utilise les tags {{form.username}}
        
            messages.success(request, 'Account was created for '+username)
            return redirect('login')
    context={'form':form}
    return render(request, 'register.html',context)

@unauthenticated_user
def loginPage(request):
 
    if request.method=='POST':
        username=request.POST.get('username')#Recuperation des données lorqu'on utilise du html simple <input name='username'>
        password=request.POST.get('password')
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request,'Username Or password is incorrect')
            return render(request, 'login.html')
    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    orders=Order.objects.all()
    customers=Customer.objects.all()
    total_customers=customers.count()
    total_orders=orders.count()
    delivered=orders.filter(status='Delivered').count()
    pending=orders.filter(status='Pending').count()
    context={'orders':orders,'customers':customers,
    'total_customers':total_customers,'total_orders':total_orders,
    'delivered':delivered,'pending':pending}
    return  render(request, 'dashboard.html', context)

@login_required(login_url='login')
def profile(request):
    return  render(request, 'profile.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
    customer=Customer.objects.get(id=pk_test)
    orders=customer.order_set.all()
    order_count=orders.count()
    myFilter=OrderFilter(request.GET,queryset=orders)
    orders=myFilter.qs
    
    context={'customer':customer, 'orders':orders,'order_count':order_count,'myFilter':myFilter}
    return  render(request, 'customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products=Product.objects.all()
    return  render(request, 'products.html', {'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request,pk):
    OrderFormSet=inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)
    customer=Customer.objects.get(id=pk)
    formset=OrderFormSet(queryset=Order.objects.none(),instance=customer)
    #form=OrderForm(initial={'customer':customer})
    if request.method=='POST':
        #form=OrderForm(request.POST)
        formset=OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('dashboard')
    context={'formset':formset}
    return render(request, 'order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
    order=Order.objects.get(id=pk)
    formset=OrderForm(instance=order)
    if request.method=='POST':
        formset=OrderForm(request.POST, instance=order)
        if formset.is_valid():
            formset.save()
            return redirect('dashboard')
    context={'formset':formset}
    return render(request, 'order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
    order=Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('dashboard')
    context={'item':order}
    return render(request, 'delete_order_form.html', context)

@login_required(login_url='login')
def createCustomer(request,pk):
    CustomerFormSet=inlineformset_factory(Customer, extra=5)
    customer=Customer.objects.get(id=pk)
    formset=CustomerFormSet(queryset=Customer.objects.none(),instance=customer)
    #form=OrderForm(initial={'customer':customer})
    if request.method=='POST':
        #form=OrderForm(request.POST)
        formset=CustomerFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('dashboard')
    context={'formset':formset}
    return render(request, 'customer_form.html', context)    

@login_required(login_url='login')
def updateCustomer(request,pk):
    customer=Customer.objects.get(id=pk)
    formset=CustomerForm(instance=customer)
    if request.method=='POST':
        formset=CustomerForm(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('dashboard')
    context={'formset':formset,'customer':customer}
    return render(request, 'customer_form.html', context)

@login_required(login_url='login')
def deleteCustomer(request,pk):
    customer=Order.objects.get(id=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('dashboard')
    context={'item':customer}
    return render(request, 'delete_customer_form.html', context)

@login_required(login_url='login')
def updateProduct(request,pk):
    product=Product.objects.get(id=pk)
    form=ProductForm(instance=customer)
    if request.method=='POST':
        form=ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context={'form':form,'product':product}
    return render(request, 'product_form.html', context)

@login_required(login_url='login')
def deleteProduct(request,pk):
    product=Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('products')
    context={'item':product}
    return render(request, 'delete_product_form.html', context)

@login_required(login_url='login')
def createCustomer(request):
    form=CustomerForm()
    if request.method=='POST':
        form=CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context={'form':form}
    return render(request, 'customer_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders=request.user.customer.order_set.all()

    total_orders=orders.count()
    delivered=orders.filter(status='Delivered').count()
    pending=orders.filter(status='Pending').count()
    context={'orders':orders, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending}
    return render(request, 'user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer=request.user.customer
    form=CustomerForm(instance=customer)
    if request.method == 'POST':
        form=CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context={'form':form}
    return render(request, 'accounts_settings.html', context)





