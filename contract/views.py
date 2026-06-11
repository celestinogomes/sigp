from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from main.decorators import  allow_user
from django.contrib import messages
from funsionariu.models import Funsionariu

from contract.models import Contract

# Create your views here.
@login_required
@allow_user(allow_roles=['admin', 'finance', 'diretor'])
def ContractLists(request):
    group = request.user.groups.all()[0].name
    data = Contract.objects.all()
    conteudo = {
        "title" : "Lista Kontratu",
        'data' : data,
        'group':group
    }
    return render(request, 'contract/list.html',conteudo)


@login_required
@allow_user(allow_roles=['focal_point'])
def ContractFCLists(request):
    user_groups = request.user.groups.all()
    group = user_groups[0].name if user_groups.exists() else "No Group"
    try:
        funsionariu_obj = Funsionariu.objects.get(user=request.user)
        user_programs = funsionariu_obj.program.all()
    except Funsionariu.DoesNotExist:
        user_programs = None

    if request.user.is_superuser:
        data = Contract.objects.all()
    elif user_programs:
        data = Contract.objects.filter(project__program__in=user_programs).distinct()
    else:
        data = Contract.objects.all()
    conteudo = {
        "title" : "Lista Kontratu",
        'data' : data,
        'group':group
    }
    return render(request, 'contract/list.html',conteudo)