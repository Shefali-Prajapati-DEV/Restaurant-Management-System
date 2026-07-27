from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Menu
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


def menu(request):
    items = Menu.objects.all()
    

    return render(request, 'menu.html', {'items':items})
   


@login_required
def add_menu(request):


    if not request.user.is_superuser:
        return redirect('menu')

    if request.method == 'POST':

        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')

        Menu.objects.create(
            name=name,
            price=price,
            description=description
        )

        return redirect('menu')

    return render(request, 'add_menu.html')








def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('menu')

    return render(request, 'login.html')




def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def edit_menu(request, id):

    if not request.user.is_superuser:
        return redirect('menu')

    item = Menu.objects.get(id=id)

    if request.method == "POST":
        item.name = request.POST.get('name')
        item.price = request.POST.get('price')
        item.description = request.POST.get('description')

        item.save()

        return redirect('menu')

    return render(request, 'edit_menu.html', {'item': item})


@login_required
def delete_menu(request, id):

    if not request.user.is_superuser:
        return redirect('menu')

    item = Menu.objects.get(id=id)
    item.delete()

    return redirect('menu')

def signup(request):

    if request.method == "POST":

        username = request.POST.get('username')

        email = request.POST.get('email')

        password = request.POST.get('password')

        User.objects.create_user(

            username=username,

            email=email,

            password=password

        )

        return redirect('login')

    return render(request,'signup.html')


