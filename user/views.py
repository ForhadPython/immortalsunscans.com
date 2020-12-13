from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from order.models import Order, OrderProduct
from product.models import Comment
from user.forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from user.models import UserProfile


@login_required(login_url='/login')  # Check login
def index(request):
    current_user = request.user  # Access User Session information
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = { 'profile': profile}
    return render(request, 'user_profile.html', context)


def login_form(request):
    if request.method == 'POST':  # check post
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = request.user
            userprofile = UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage'] = userprofile.image.url
            return HttpResponseRedirect('/')
        else:
            messages.success(request, " Username And Password is Incorrect !! ")
            return HttpResponseRedirect('/login')
    context = {}
    return render(request, 'login_form.html', context)


def signup_form(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()  # completed sign up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            # Create data in profile table for user
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/user.png"
            data.save()
            messages.success(request, 'Your account has been created!')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/signup')

    form = SignUpForm()
    context = {'form': form}
    return render(request, 'signup_form.html', context)


def logout_func(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url='/login')  # Check login
def user_update(request):
    return HttpResponse("<h2>Hello Sir This Page is comming soon </h2>")


@login_required(login_url='/login')  # Check login
def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below.<br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        form = PasswordChangeForm(request.user)
        contect = {
            'form': form}
        return render(request, 'user_password.html', contect)


@login_required(login_url='/login')  # Check login
def user_orders(request):
    current_user = request.user
    orders = Order.objects.filter(user_id=current_user.id)
    context = {
               'orders': orders,
               }
    return render(request, 'user_orders.html', context)


@login_required(login_url='/login')  # Check login
def user_orderdetail(request, id):
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)
    context = {
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'user_order_detail.html', context)


@login_required(login_url='/login')  # Check login
def user_order_product(request):
    current_user = request.user
    order_product = OrderProduct.objects.filter(user_id=current_user.id).order_by('-id')
    context = {
               'order_product': order_product,
               }
    return render(request, 'user_order_products.html', context)


@login_required(login_url='/login')  # Check login
def user_order_product_detail(request, id, oid):
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=oid)
    orderitems = OrderProduct.objects.filter(id=id, user_id=current_user.id)
    context = {
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'user_order_detail.html', context)


def user_comments(request):
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        'comments': comments,
    }
    return render(request, 'user_comments.html', context)


@login_required(login_url='/login')  # Check login
def user_deletecomment(request, id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Comment deleted..')
    return HttpResponseRedirect('/user/comments')
