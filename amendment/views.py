from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from amendment.models import AmendmenTime, AmendmenAmount
from amendment.forms import AmendmentAmountForm, AmendmentTimeForm
from main.decorators import  allow_user
from django.contrib import messages
from project.models import Project
from contract.models import ContractAmendment
from decimal import Decimal

from django.db.models import Subquery, OuterRef

from funsionariu.models import Funsionariu



@login_required
@allow_user(allow_roles=['admin', 'focal_point', 'finance', 'diretor'])
def AmandmenAmountList(request):
    group = request.user.groups.all()[0].name
    
    latest_allocation = AmendmenAmount.objects.filter(
        project_id=OuterRef('project_id')  
    ).order_by('-id').values('id')[:1]
    
    data = AmendmenAmount.objects.filter(id=Subquery(latest_allocation))
    
    conteudo = {
        "title" : "Lista Amandament Orsamento",
        'data' : data,
        'group': group
    }
    return render(request, 'amendment/amount_list.html', conteudo)



@login_required
@allow_user(allow_roles=['admin', 'focal_point'])
def AmandmenAmountFCList(request):
    user_groups = request.user.groups.all()
    group = user_groups[0].name if user_groups.exists() else "No Group"
    try:
        funsionariu_obj = Funsionariu.objects.get(user=request.user)
        user_programs = funsionariu_obj.program.all()
    except Funsionariu.DoesNotExist:
        user_programs = None


    if request.user.is_superuser:
        latest_allocation = AmendmenAmount.objects.filter(
            project_id=OuterRef('project_id')  
        ).order_by('-id').values('id')[:1]
    elif user_programs:
        latest_allocation = AmendmenAmount.objects.filter(
            project__program__in=user_programs,
            project_id=OuterRef('project_id')  
        ).order_by('-id').values('id')[:1]
    else:
        latest_allocation = AmendmenAmount.objects.filter(
            project_id=OuterRef('project_id')  
        ).order_by('-id').values('id')[:1]


    
    
    data = AmendmenAmount.objects.filter(id=Subquery(latest_allocation))
    
    conteudo = {
        "title" : "Lista Amandament Orsamento",
        'data' : data,
        'group': group
    }
    return render(request, 'amendment/amount_list.html', conteudo)


@login_required
@allow_user(allow_roles=['admin', 'focal_point', 'finance', 'diretor'])
def AmandmenTimeList(request):
    group = request.user.groups.all()[0].name
    
    latest_allocation = AmendmenTime.objects.filter(
        project_id=OuterRef('project_id')  
    ).order_by('-id').values('id')[:1]
    
    data = AmendmenTime.objects.filter(id=Subquery(latest_allocation))
    
    conteudo = {
        "title" : "Lista Amandament Tempo",
        'data' : data,
        'group': group
    }
    return render(request, 'amendment/time_list.html', conteudo)



@login_required
@allow_user(allow_roles=['admin', 'focal_point'])
def AmandmenFCTimeList(request):
    user_groups = request.user.groups.all()
    group = user_groups[0].name if user_groups.exists() else "No Group"
    try:
        funsionariu_obj = Funsionariu.objects.get(user=request.user)
        user_programs = funsionariu_obj.program.all()
    except Funsionariu.DoesNotExist:
        user_programs = None
    
    
    if request.user.is_superuser:
        latest_allocation = AmendmenTime.objects.filter(
            project_id=OuterRef('project_id')  
        ).order_by('-id').values('id')[:1]
    elif user_programs:
        latest_allocation = AmendmenTime.objects.filter(
        project__program__in=user_programs,
        project_id=OuterRef('project_id')  
    ).order_by('-id').values('id')[:1]
    else:
        latest_allocation = AmendmenTime.objects.filter(
            project_id=OuterRef('project_id')  
        ).order_by('-id').values('id')[:1]
    
    data = AmendmenTime.objects.filter(id=Subquery(latest_allocation))
    
    conteudo = {
        "title" : "Lista Amandament Tempo",
        'data' : data,
        'group': group
    }
    return render(request, 'amendment/time_list.html', conteudo)

@login_required
@allow_user(allow_roles=['admin', 'focal_point'])
def AmendmentAmountAdd(request, uuid):
    project = get_object_or_404(Project, uuid=uuid)
    contract_amend = get_object_or_404(ContractAmendment, project=project)
    
    group = request.user.groups.first().name if request.user.groups.exists() else "No Group"
    
    if request.method == "POST":
        form = AmendmentAmountForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.project = project
            instance.user = request.user
            
            current_amend_amount = contract_amend.amendment_amount or Decimal('0.00')
            new_amount = Decimal(str(instance.amount)) 
            
            current_total = instance.amount_total or Decimal('0.00')
            
            instance.amount_total = current_amend_amount + new_amount
            instance.save()
            
            contract_amend.amendment_amount = current_amend_amount + new_amount
            contract_amend.save()
            
            messages.success(request, 'Amendment Amount aumenta ona')
            return redirect('proj-detail', uuid)
        else:
            messages.error(request, 'Formulario invalidu, favor cek fali dadus.')
            print(form.errors)
    else:
        form = AmendmentAmountForm()
        
    conteudo = {
        "title": "Aumenta Amendment Amount",
        "subtitle": "Formulario Aumenta Amendment Amount",
        "group": group, 
        "form": form, 
        "uuid": uuid
    }
    
    return render(request, 'amendment/form.html', conteudo)


@login_required
@allow_user(allow_roles=['admin', 'focal_point'])
def AmendmentTimeAdd(request, uuid):
    project = get_object_or_404(Project, uuid=uuid)
    contract_amend = get_object_or_404(ContractAmendment, project=project)
    
    group = request.user.groups.first().name if request.user.groups.exists() else "No Group"
    
    if request.method == "POST":
        form = AmendmentTimeForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.project = project
            instance.user = request.user
            instance.save()
            
            contract_amend.amendment_end_date = instance.end_date
            contract_amend.save()
            
            messages.success(request, 'Amendment Tempo aumenta ona')
            return redirect('proj-detail', uuid)
        else:
            messages.error(request, 'Formulario invalidu, favor cek fali dadus.')
    else:
        form = AmendmentTimeForm()
        
    conteudo = {
        "title": "Aumenta Amendment Amount",
        "subtitle": "Formulario Aumenta Amendment Amount",
        "group": group, 
        "form": form, 
        "uuid": uuid
    }
    
    return render(request, 'amendment/form.html', conteudo)

