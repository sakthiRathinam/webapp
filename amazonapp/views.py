from django.shortcuts import render,redirect
from .models import *
from .forms import OrderForm,UserForm,CustomerForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import *
@unauthenticated_user
def registerPage(request):
	form=UserForm()
	if request.method=='POST':
		form=UserForm(request.POST)
		if form.is_valid():
			user=form.save()
			username=form.cleaned_data.get('username')
			group=Group.objects.get(name='customer')
			user.groups.add(group)
			Customer.objects.create(user=user,name=user.username,)
			messages.success(request,"Account was created successfully" + username)
			return redirect('login')
	context={'form':form}
	return render(request,'html/register.html',context)
@unauthenticated_user
def loginPage(request):
	if request.method=="POST":
		username=request.POST.get('username')
		password=request.POST.get('password')
		user=authenticate(request,username=username,password=password)
		if user is not None:
			login(request,user)
			return redirect('home')
		else:
			messages.info(request,'Username or password is incorrect')
	context={}
	return render(request,'html/login.html',context)
def logoutUser(request):
	logout(request)
	return redirect('login')		
@login_required(login_url='login')
@admin_only
def home(request):
	customers=Customer.objects.all()
	orders=Order.objects.all()
	total_customers=customers.count()
	total_orders=orders.count()
	delivered=orders.filter(status='Delivered').count()
	pending=orders.filter(status='pending').count()
	context={'customers':customers,'orders':orders,'total_customers':total_customers,'total_orders':total_orders,
	'delivered':delivered,'pending':pending}
	return render(request, 'html/dashboard.html',context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
	orders=request.user.customer.order_set.all()
	total_orders=orders.count()
	delivered=orders.filter(status='Delivered').count()
	pending=orders.filter(status='pending').count()
	context={'orders':orders,'total_orders':total_orders,'delivered':delivered,'pending':pending}
	return render(request,'html/userpage.html',context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customers(request,pk):
	customer=Customer.objects.get(id=pk)
	orders=customer.order_set.all()
	order_count=orders.count()
	myFilter=OrderFilter(request.GET,queryset=orders)
	orders=myFilter.qs
	context={'customer':customer,'orders':orders,'order_count':order_count,'myFilter':myFilter}
	return render(request, 'html/customers.html',context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
	products=Product.objects.all()
	context={'products':products}
	return render(request,'html/products.html',context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request,pk):
	#form=OrderForm()
	OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'),extra=7)
	customer=Customer.objects.get(id=pk)
	formset=OrderFormSet(queryset=Order.objects.none(),instance=customer)
	if request.method=="POST":
		#form=OrderForm(request.POST)
		formset=OrderFormSet(request.POST,instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')
	context={'form':formset}
	return render(request,'html/createorder.html',context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
	order=Order.objects.get(id=pk)
	form=OrderForm(instance=order)
	if request.method=='POST':
		form=OrderForm(request.POST,instance=order)
		form.save()
		return redirect('/')
	context={'form':form}
	return render(request,'html/createorder.html',context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
	item=Order.objects.get(id=pk)
	if request.method=="POST":
		item.delete()
		return redirect('/')
	context={'item':item}
	return render(request,'html/deleteorder.html',context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer=request.user.customer
	form=CustomerForm(instance=customer)
	if request.method=='POST':
		form=CustomerForm(request.POST,request.FILES,instance=customer)
		if form.is_valid():
			form.save()
	context={'form':form}
	return render(request,'html/accountsettings.html',context)