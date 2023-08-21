from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Products, Order
from .forms import ProductForm, OrderForm
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
@login_required
def index(request):
    workers_count = User.objects.all().count()
    orders = Order.objects.all()
    order_count = orders.count()
    products = Products.objects.all()
    items_count = products.count()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.staff = request.user
            instance.save()
            return redirect('dashboard-index')
    else:
        form = OrderForm()
    context = {
        'orders':orders,
        'form':form,
        'products' : products,
        'workers_count': workers_count,
        'order_count': order_count,
        'items_count': items_count,
    }
    return render(request,'dashboard/index.html', context)


@login_required
def staff(request):
    workers = User.objects.all()
    workers_count = workers.count()
    items = Products.objects.all()
    items_count = items.count()
    order = Order.objects.all()
    order_count = order.count()
    context = {
        'workers':workers,
        'workers_count' : workers_count,
        'items_count' : items_count,
        'order_count': order_count
    }
    return render(request,'dashboard/staff.html', context)

@login_required
def staff_detail(request,pk):
    workers = User.objects.get(id=pk)
    context = {
        'workers' : workers,
    }
    return render(request,"dashboard/staff_detail.html", context)

# @login_required
# def staff_index(request):
#     order = Order.objects.all()
#     context = {
#         'order':order,
#     }
#     return render(request,"dashboard/staff_index.html", context)


@login_required
def products(request):
    items = Products.objects.all()
    items_count = items.count()
    workers = User.objects.all()
    workers_count = workers.count()
    order = Order.objects.all()
    order_count = order.count()
    if request.method == 'POST':
        form  = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            productname = form.cleaned_data.get('name')
            messages.success(request, f'{productname} has been added')
            return redirect('dashboard-products')
    else:
        form = ProductForm()

    context = {
        'items':items,
        'form':form,
        'workers_count' : workers_count,
        'items_count' : items_count,
        'order_count': order_count,
    }
    return render(request,'dashboard/products.html', context)

@login_required
def product_delete(request, pk):
    items = Products.objects.get(id=pk)
    if request.method=='POST':
        items.delete()
        return redirect('dashboard-products')
    return render(request, "dashboard/product_delete.html")

@login_required
def product_update(request,pk):
    item = Products.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard-products')
    else:
        form = ProductForm(instance=item)
    context = {
        'form': form,
    }
    return render(request,'dashboard/product_edit.html', context)

@login_required
def orders(request):
    order = Order.objects.all()
    order_count = order.count()
    items = Products.objects.all()
    items_count = items.count()
    workers = User.objects.all()
    workers_count = workers.count()
    context={
        'order':order,
        'order_count' : order_count,
        'items_count': items_count,
        'workers_count' : workers_count,
    }
    return render(request,'dashboard/orders.html', context)