from django.shortcuts import render, redirect
from funsionariu.models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.forms import *

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required
def userList(request):
    objects = []
    users = User.objects.all().exclude(id=request.user.id).select_for_update('employeeuser')
    for x in users:
        stored_password = x.password
        is_valid_match = check_password('password123', stored_password)  # password uluk mak password, password bainhira kria user foun mak password123
        if is_valid_match:
            objects.append([x,"password123"])
        else:
            objects.append([x,"alteradu"])
    context = {
        'title': 'Lista Utilizadores',
        'obj': objects,
    }
    return render(request, 'user.html', context)

@login_required
def deleteUsers(request, hamosID):
    try:
        userData = User.objects.get(pk=hamosID)
        if hasattr(userData, 'employeeuser'):
            funsionariu = userData.employeeuser
            funsionariu.user = None
            funsionariu.save()
        userData.delete()
        messages.success(request, f'User {userData.username} Hamoos ho Susesu!')
    except Exception as e:
        messages.error(request, f'Erro iha prosesu delete: {str(e)}')
    return redirect('user_list')

@login_required
def resetUsersPassword(request, id):
    userData = User.objects.get(pk=id)
    password = make_password('password123')
    userData.password = password
    userData.save()
    messages.success(request, f'Password ba {userData.username} Reset ho Susesu!')
    return redirect('user_list')

@login_required
def ativuUser(request,id):
    userData = User.objects.get(id=id)
    userData.is_active = True
    userData.save()
    messages.success(request, f'User {userData.username} Ativu ho Susesu!')
    return redirect('user_list')

@login_required
def desativuUser(request,id):
    userData = User.objects.get(id=id)
    userData.is_active = False
    userData.save()
    messages.success(request, f'User {userData.username} Desativu ho Susesu!')
    return redirect('user_list')

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'profile.html', {
        'title': 'Profile Settings',
        'form': form
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully!')
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'change_password.html', {
        'title': 'Change Password',
        'form': form
    })
