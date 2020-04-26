from django.shortcuts import render,redirect
from .models import *
from .forms import OrderForm,UserForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form=UserForm()
		if request.method=='POST':
			form=UserForm(request.POST)
			if form.is_valid():
				form.save()
				user=form.cleaned_data.get('username')
				messages.success(request,"Account was created successfully" + user)
				return redirect('login')
		context={'form':form}
		return render(request,'html/register.html',context)
def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
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
def customers(request,pk):
	customer=Customer.objects.get(id=pk)
	orders=customer.order_set.all()
	order_count=orders.count()
	myFilter=OrderFilter(request.GET,queryset=orders)
	orders=myFilter.qs
	context={'customer':customer,'orders':orders,'order_count':order_count,'myFilter':myFilter}
	return render(request, 'html/customers.html',context)
def products(request):
	products=Product.objects.all()
	context={'products':products}
	return render(request,'html/products.html',context)
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
def updateOrder(request,pk):
	order=Order.objects.get(id=pk)
	form=OrderForm(instance=order)
	if request.method=='POST':
		form=OrderForm(request.POST,instance=order)
		form.save()
		return redirect('/')
	context={'form':form}
	return render(request,'html/createorder.html',context)
def deleteOrder(request,pk):
	item=Order.objects.get(id=pk)
	if request.method=="POST":
		item.delete()
		return redirect('/')
	context={'item':item}
	return render(request,'html/deleteorder.html',context)