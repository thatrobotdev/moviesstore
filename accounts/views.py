from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, CustomErrorList
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            request.session['failed_attempts'] = 0
            return redirect('orders')
        else:
            failed_attempts = request.session.get('failed_attempts', 0) + 1
            request.session['failed_attempts'] = failed_attempts
            context['error'] = "Invalid username or password."
            if failed_attempts >= 1:
                context['login_failed'] = True

    return render(request, 'login.html', {'template_data': context})

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html', {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')

def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html', {'template_data': template_data})

@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html', {'template_data': template_data})

def reset_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        maiden_name = request.POST.get('maiden_name')
        new_password = request.POST.get('new_password')

        try:
            user = User.objects.get(username=username)
            if user.profile.maiden_name.lower() == maiden_name.lower():  # Assuming the field is in the profile model
                user.set_password(new_password)
                user.save()
                return redirect('accounts.login')
            else:
                return render(request, 'accounts/reset_password.html', {'error': 'Incorrect security answer'})
        except User.DoesNotExist:
            return render(request, 'accounts/reset_password.html', {'error': 'User not found'})

    return render(request, 'accounts/reset_password.html')
