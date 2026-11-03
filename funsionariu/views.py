from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from funsionariu.models import *
from funsionariu.forms import *
from django.contrib import messages
from django.contrib.auth.models import User, Group

@login_required
# @allowed_users(allowed_roles=['ADMIN'])
def ListFunsionariu(request):
    listfunsionariu = Funsionariu.objects.all()
    
    for fun in listfunsionariu:
        fun.has_user = User.objects.filter(employeeuser=fun).exists()
    conteudo = {
        "title" : "Lista Dadus Funsionario",
        'listaFunsionariu' : listfunsionariu,
    }
    return render(request, 'funsionario.html',conteudo)

@login_required
# @allowed_users(allowed_roles=['ADMIN'])
def AddFunsionariu(request):
    if request.method == 'POST':
        form = FunsionariuForm(request.POST)
        if form.is_valid():
            form.save()
            # messages.success(request,f'Funsionariu Aumenta ho Susesu')
            return redirect('funsionario')
    else:
        form = FunsionariuForm()
    context = {
        "title" : "Formulario Aumenta Funsionariu",
        'form':form,
    }
    return render(request,'addfunsionario.html',context)


@login_required
# @allowed_users(allowed_roles=['ADMIN'])
def UpdateFunsionariu(request,id_update):
    dadusfunsionariu = get_object_or_404(Funsionariu,nu_registu=id_update)
    if request.method == 'POST':
        form = FunsionariuForm(request.POST,instance=dadusfunsionariu)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            # messages.success(request,f'Dadus Funsionariu Hadia ho susesu')
            return redirect('funsionario')
    else:
        form = FunsionariuForm(instance=dadusfunsionariu)
    conteudu = {
        "title" : "Formulariu Alterasaun Dadus Funsionariu",
        "form" : form,
    }
    return render(request,'addfunsionario.html',conteudu)

@login_required
# @allowed_users(allowed_roles=['ADMIN'])
def DeleteFunsionariu(request, id_delete):
    funsionariu = get_object_or_404(Funsionariu, nu_registu=id_delete)
    funsionariu.delete()
    # messages.success(request,f'Supplier {material.naran_material} Hamoos ho Susesu!')
    return redirect('funsionario')

@login_required
def kriaUser(request, pk):
    funsi = get_object_or_404(Funsionariu, nu_registu=pk)
    
    if not funsi.user:
        try:
            username = f'user_{funsi.nu_registu}'
            password = 'password123'

            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=funsi.naran_kompletu.split()[0],
                last_name=' '.join(funsi.naran_kompletu.split()[1:])
            )

            group, created = Group.objects.get_or_create(name=funsi.user_level)
            user.groups.add(group)

            funsi.user = user
            funsi.save()

            messages.success(request, f'User kria ona ho susesu! Username: {username}, Password: {password}')
        except Exception as e:
            messages.error(request, f'Erro kria user: {str(e)}')
    else:
        messages.warning(request, f'Funsionariu {funsi.naran_kompletu} iha ona user')
    
    return redirect('funsionario')