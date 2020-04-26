from django.shortcuts import render,redirect
from .models import *
from .forms import OrderForm
from django.forms import inlineformset_factory
# Create your views here.
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
	context={'customer':customer,'orders':orders,'order_count':order_count}
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
