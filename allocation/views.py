from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from main.decorators import  allow_user
from django.contrib import messages
from project.models import Project
from decimal import Decimal
from django.db import transaction
from django.db.models import Subquery, OuterRef

from allocation.models import Allocation, Transferencia
from allocation.forms import AllocationForm, TransferenciaForm
from funsionariu.models import Funsionariu

@login_required
@allow_user(allow_roles=['admin', 'finance', 'diretor'])
def AllocationLists(request):
    group = request.user.groups.all()[0].name
    
    latest_allocation = Allocation.objects.filter(
        project_id=OuterRef('project_id')  
    ).order_by('-id').values('id')[:1]
    
    data = Allocation.objects.filter(id=Subquery(latest_allocation))
    
    conteudo = {
        "title" : "Lista Alokasaun",
        'data' : data,
        'group': group
    }
    return render(request, 'allocation/list.html', conteudo)

# FOCAL POINT
@login_required
@allow_user(allow_roles=['focal_point'])
def AllocationFCLists(request):
    user_groups = request.user.groups.all()
    group = user_groups[0].name if user_groups.exists() else "No Group"
    try:
        funsionariu_obj = Funsionariu.objects.get(user=request.user)
        user_programs = funsionariu_obj.program.all()
    except Funsionariu.DoesNotExist:
        user_programs = None


    if request.user.is_superuser:
        latest_allocation = Allocation.objects.filter(
            project_id=OuterRef('project_id')  
        ).order_by('-id').values('id')[:1]
    elif user_programs:
        latest_allocation = Allocation.objects.filter(
            project__program__in=user_programs,
            project_id=OuterRef('project_id')  
        ).order_by('-id').values('id')[:1]
    else:
        latest_allocation = Allocation.objects.filter(
            project_id=OuterRef('project_id')  
        ).order_by('-id').values('id')[:1]
    
    data = Allocation.objects.filter(id=Subquery(latest_allocation))
    
    conteudo = {
        "title" : "Lista Alokasaun",
        'data' : data,
        'group': group
    }
    return render(request, 'allocation/list.html', conteudo)


@login_required
@allow_user(allow_roles=['admin', 'finance', 'diretor'])
def TransferenciaLists(request):
    group = request.user.groups.all()[0].name
    
    latest_allocation = Transferencia.objects.filter(
        project_id=OuterRef('project_id')  
    ).order_by('-id').values('id')[:1]
    
    data = Transferencia.objects.filter(id=Subquery(latest_allocation))
    
    conteudo = {
        "title" : "Lista Transferensia",
        'data' : data,
        'group': group
    }
    return render(request, 'transfer/list.html', conteudo)


# FOCAL POINT
@login_required
@allow_user(allow_roles=['focal_point'])
def TransferenciaFCLists(request):
    user_groups = request.user.groups.all()
    group = user_groups[0].name if user_groups.exists() else "No Group"
    try:
        funsionariu_obj = Funsionariu.objects.get(user=request.user)
        user_programs = funsionariu_obj.program.all()
    except Funsionariu.DoesNotExist:
        user_programs = None

    if request.user.is_superuser:
        latest_allocation = Transferencia.objects.filter(
            project_id=OuterRef('project_id')  
        ).order_by('-id').values('id')[:1]
    elif user_programs:
        latest_allocation = Transferencia.objects.filter(
            project__program__in=user_programs,
            project_id=OuterRef('project_id')  
        ).order_by('-id').values('id')[:1]
    else:
        latest_allocation = Transferencia.objects.filter(
            project_id=OuterRef('project_id')  
        ).order_by('-id').values('id')[:1]
    
    
    
    data = Transferencia.objects.filter(id=Subquery(latest_allocation))
    
    conteudo = {
        "title" : "Lista Transferensia",
        'data' : data,
        'group': group
    }
    return render(request, 'transfer/list.html', conteudo)

@login_required
@allow_user(allow_roles=['admin', 'focal_point', 'finance'])
def AllocationAdd(request, uuid):
    project = get_object_or_404(Project, uuid=uuid)
    group = request.user.groups.all()[0].name if request.user.groups.exists() else "No Group"
    if request.method == "POST":
        form = AllocationForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data.get('year')
            instance = form.save(commit=False)
            existing = Allocation.objects.filter(project=project, year=year).last()
            if existing:
                messages.error(request, f'Alokasaun ba Tinan {year} iha Ona')
                return redirect('alloc-add', uuid)
            else:
                instance.project = project
                instance.user = request.user
                instance.is_active = True
                instance.allocation_total = instance.allocation_original
                instance.save()
                project.activity_code = instance.activity_code
                project.save()
                other_allocation = Allocation.objects.filter(project=project).exclude(pk=instance.id)
                for obj in other_allocation:
                    obj.is_active = False
                    obj.save()
                messages.success(request, 'Alokasaun aumenta ona')
                return redirect('proj-detail', uuid)
    else:
        check_allocation = Allocation.objects.filter(project=project).last()
        if check_allocation:
            form = AllocationForm(initial={'activity_code': check_allocation.activity_code})
        else:
            form = AllocationForm()
    conteudo = {
        "title": "Aumenta Alokasaun",
        "subtitle": "Formulario Aumenta Alokasaun",
        "group": group, 'form': form, 'uuid':uuid
    }
    
    return render(request, 'allocation/form.html', conteudo)


@login_required
@allow_user(allow_roles=['admin', 'focal_point', 'finance'])
def AllocationLock(request, uuid):
    allocation = get_object_or_404(Allocation, uuid=uuid)
    allocation.is_lock = True
    allocation.save()
    messages.success(request, 'Alokasaun chave ona')
    return redirect('proj-detail', allocation.project.uuid)

@login_required
@allow_user(allow_roles=['admin', 'focal_point', 'finance'])
def AllocationDelete(request, uuid):
    allocation = get_object_or_404(Allocation, uuid=uuid)
    uuid = allocation.project.uuid
    allocation.delete()
    messages.success(request, 'Alokasaun Delete Ona')
    return redirect('proj-detail', uuid)



@login_required
@allow_user(allow_roles=['admin', 'focal_point', 'finance'])
@transaction.atomic
def TransferenciaAdd(request, uuid, uuid2):
    project = get_object_or_404(Project, uuid=uuid)
    allocation = get_object_or_404(Allocation, uuid=uuid2)
    
    group = request.user.groups.first().name if request.user.groups.exists() else "No Group"
    
    if request.method == "POST":
        form = TransferenciaForm(request.POST)
        if form.is_valid():
            amount = Decimal(str(form.cleaned_data.get('transferencia')))
            
            if amount == 0:
                messages.error(request, 'Montante Transferencia labele Zero')
                return redirect('trans-add', uuid, uuid2)
            
            last_trans = Transferencia.objects.filter(project=project, allocation=allocation, is_active=True).last()
            base_total = last_trans.allocation_total if last_trans else (allocation.allocation_original or Decimal('0.00'))
            
            new_allocation_total = base_total + amount
            
            current_execution = allocation.execution_amount if allocation.execution_amount else Decimal('0.00')
            
            new_contract_balance = new_allocation_total - current_execution
            
            if new_allocation_total > 0:
                new_execution_percent = (current_execution / new_allocation_total) * 100
                new_balance_percent = (new_contract_balance / new_allocation_total) * 100 
            else:
                new_execution_percent = Decimal('0.00')
                new_balance_percent = Decimal('0.00')
            
            instance = form.save(commit=False)
            instance.project = project
            instance.allocation = allocation
            instance.user = request.user
            instance.is_active = True
            instance.allocation_total = new_allocation_total
            instance.save()

            allocation.allocation_total = new_allocation_total
            allocation.execution_amount = current_execution
            allocation.execution_percent = new_execution_percent
            allocation.contract_balance = new_contract_balance
            allocation.balance_percent = new_balance_percent 
            allocation.save()

            Transferencia.objects.filter(project=project, allocation=allocation).exclude(pk=instance.id).update(is_active=False)
            
            messages.success(request, 'Transferencia aumenta no sinkroniza ona ho susesu.')
            return redirect('proj-detail', uuid)
        else:
            messages.error(request, 'Formulario invalidu, favor hafoun fali.')
    else:
        form = TransferenciaForm()
        
    conteudo = {
        "title": "Aumenta Transferencia",
        "group": group, 
        "form": form, 
        "uuid": uuid,
        "uuid2": uuid2,
        "allocation": allocation
    }
    return render(request, 'allocation/form.html', conteudo)

@login_required
@allow_user(allow_roles=['admin', 'focal_point', 'finance'])
def TransferenciaLock(request, uuid):
    objects = get_object_or_404(Transferencia, uuid=uuid)
    objects.is_lock = True
    objects.save()
    messages.success(request, 'Transferencia chave ona')
    return redirect('proj-detail', objects.project.uuid)

@login_required
@allow_user(allow_roles=['admin', 'focal_point', 'finance'])
@transaction.atomic
def TransferenciaDelete(request, uuid):
    transfer = get_object_or_404(Transferencia, uuid=uuid)
    allocation = transfer.allocation
    project = transfer.project
    
    transfer_amount = transfer.transferencia if transfer.transferencia else Decimal('0.00')
    
    current_total = allocation.allocation_total if allocation.allocation_total else Decimal('0.00')
    new_allocation_total = current_total - transfer_amount
    
    current_execution = allocation.execution_amount if allocation.execution_amount else Decimal('0.00')
    
    new_contract_balance = new_allocation_total - current_execution
    
    if new_allocation_total > 0:
        new_execution_percent = (current_execution / new_allocation_total) * 100
        new_balance_percent = (new_contract_balance / new_allocation_total) * 100
    else:
        new_execution_percent = Decimal('0.00')
        new_balance_percent = Decimal('0.00')
        
    allocation.allocation_total = new_allocation_total
    allocation.execution_amount = current_execution
    allocation.execution_percent = new_execution_percent
    allocation.contract_balance = new_contract_balance
    allocation.balance_percent = new_balance_percent
    allocation.save()
    
    if transfer.is_active:
        previous_transfer = Transferencia.objects.filter(
            project=project, 
            allocation=allocation
        ).exclude(pk=transfer.id).last()
        
        if previous_transfer:
            previous_transfer.is_active = True
            previous_transfer.save()
            
    uuid_project = project.uuid
    transfer.delete()
    
    messages.success(request, 'Transferencia delete no sinkroniza fali ona ho Alokasaun.')
    return redirect('proj-detail', uuid_project)



