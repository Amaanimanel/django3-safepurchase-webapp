from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import PurchaseForm
from .models import Purchase
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'purchase/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'purchase/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currentpurchases')
            except IntegrityError:
                return render(request, 'purchase/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'purchase/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'purchase/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'purchase/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currentpurchases')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def createpurchase(request):
    if request.method == 'GET':
        return render(request, 'purchase/createpurchase.html', {'form':PurchaseForm()})
    else:
        try:
            form = PurchaseForm(request.POST)
            newpurchase = form.save(commit=False)
            newpurchase.user = request.user
            newpurchase.save()
            return redirect('https://ravesandbox.flutterwave.com/pay/9sphzqkvazwm')
        except ValueError:
            return render(request, 'purchase/createpurchase.html', {'form':PurchaseForm(), 'error':'Bad data passed in. Try again.'})

@login_required
def currentpurchases(request):
    purchases = Purchase.objects.filter(user=request.user, datereceived__isnull=True)
    return render(request, 'purchase/currentpurchases.html', {'purchases':purchases})

@login_required
def receivedpurchases(request):
    purchases = Purchase.objects.filter(user=request.user, datereceived__isnull=False).order_by('-datereceived')
    return render(request, 'purchase/receivedpurchases.html', {'purchases':purchases})

@login_required
def viewpurchase(request, purchase_pk):
    purchase = get_object_or_404(Purchase, pk=purchase_pk, user=request.user)
    if request.method == 'GET':
        form = PurchaseForm(instance=purchase)
        return render(request, 'purchase/viewpurchase.html', {'purchase':purchase, 'form':form})
    else:
        try:
            form = PurchaseForm(request.POST, instance=purchase)
            return redirect('currentpurchases')
        except ValueError:
            return render(request, 'purchase/viewpurchase.html', {'purchase':purchase, 'form':form, 'error':'Bad info'})

@login_required
def viewreceivedpurchase(request, purchase_pk):
    purchase = get_object_or_404(Purchase, pk=purchase_pk, user=request.user)
    if request.method == 'GET':
        form = PurchaseForm(instance=purchase)
        return render(request, 'purchase/viewreceivedpurchase.html', {'purchase':purchase, 'form':form})
    else:
        try:
            form = PurchaseForm(request.POST, instance=purchase)
            return redirect('receivedpurchases')
        except ValueError:
            return render(request, 'purchase/viewreceivedpurchase.html', {'purchase':purchase, 'form':form, 'error':'Bad info'})


@login_required
def receivepurchase(request, purchase_pk):
    purchase = get_object_or_404(Purchase, pk=purchase_pk, user=request.user)
    if request.method == 'POST':
        purchase.datereceived = timezone.now()
        purchase.save()
        return redirect('currentpurchases')

@login_required
def deletepurchase(request, purchase_pk):
    purchase = get_object_or_404(Purchase, pk=purchase_pk, user=request.user)
    if request.method == 'POST':
        purchase.delete()
        return redirect('receivedpurchases')