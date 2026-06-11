from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from main.decorators import  allow_user
from django.contrib import messages
from django.db import transaction

from project.models import Project, ProjectLocation, ProjectJustification, ProjectStatus
from contract.models import Contract, ContractAmendment
from allocation.models import Allocation, Transferencia
from amendment.models import AmendmenAmount, AmendmenTime
from payment.models import Payment, PaymentHistory

from contract.forms import ContractForm
from project.forms import ProjectForm, ProjectLocationForm, ProjectStatusForm, ProjectJustificationForm
from funsionariu.models import Funsionariu

@login_required
@allow_user(allow_roles=['admin', 'finance', 'diretor'])
def ProjectLists(request):
    group = request.user.groups.all()[0].name
    data = Project.objects.all()
    conteudo = {
        "title" : "Lista Projetu",
        'data' : data,
        'group':group
    }
    return render(request, 'project/list.html',conteudo)

@login_required
@allow_user(allow_roles=['focal_point'])
def ProjectFCLists(request):
    user_groups = request.user.groups.all()
    group = user_groups[0].name if user_groups.exists() else "No Group"
    
    try:
        funsionariu_obj = Funsionariu.objects.get(user=request.user)
        user_programs = funsionariu_obj.program.all()
    except Funsionariu.DoesNotExist:
        user_programs = None

    if request.user.is_superuser:
        data = Project.objects.all()
    elif user_programs:
        data = Project.objects.filter(program__in=user_programs).distinct()
    else:
        data = Project.objects.none()

    conteudo = {
        "title" : "Lista Projetu",
        'data' : data,
        'group': group
    }
    return render(request, 'project/list.html', conteudo)


@login_required
@allow_user(allow_roles=['admin', 'focal_point', 'finance'])
def ProjectAdd(request):
    group = request.user.groups.all()[0].name if request.user.groups.exists() else "No Group"
    
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        proj_location_form = ProjectLocationForm(request.POST)
        contract_form = ContractForm(request.POST)
        
        if project_form.is_valid() and project_form.is_valid() and proj_location_form.is_valid() and contract_form.is_valid():
            try:
                project = project_form.save(commit=False)
                project.user = request.user
                project.save()
                
                location = proj_location_form.save(commit=False)
                if hasattr(location, 'project'): 
                    location.project = project
                location.save()
                
                contract = contract_form.save(commit=False)
                if hasattr(contract, 'project'): 
                    contract.project = project
                    contract.user = request.user
                contract.save()
                if contract.amount:
                    ContractAmendment.objects.create(
                        project=project,
                        amendment_contract_number=contract.number,
                        amendment_end_date=contract.end_date,
                        amendment_amount=contract.amount,
                        user=request.user
                    )
                
                messages.success(request, "Projetu foun aumenta ho susesu!")
                return redirect('proj-detail', project.uuid) 
                
            except Exception as e:
                messages.error(request, f"Mosu erro wainhira rai dadus: {str(e)}")
        else:
            messages.error(request, "Favor bele hadi'ak fali erro iha okos wainhira submete formulario.")
    else:
        project_form = ProjectForm()
        proj_location_form = ProjectLocationForm()
        contract_form = ContractForm()

    conteudo = {
        "title": "Aumenta Projetu",
        "subtitle": "Formulario Aumenta Projeto",
        "group": group,
        "project_form": project_form,
        "proj_location_form": proj_location_form,
        "contract_form": contract_form,
    }
    
    return render(request, 'project/form.html', conteudo)



@login_required
@allow_user(allow_roles=['admin', 'focal_point', 'finance'])
def ProjectUpdate(request, uuid): 
    project = get_object_or_404(Project, uuid=uuid)
    
    proj_location = ProjectLocation.objects.filter(project=project).first()
    contract = Contract.objects.filter(project=project).first()
    contract_amend = ContractAmendment.objects.filter(project=project).last()
    group = request.user.groups.all()[0].name if request.user.groups.exists() else "No Group"
    
    if request.method == 'POST':
        project_form = ProjectForm(request.POST, instance=project)
        proj_location_form = ProjectLocationForm(request.POST, instance=proj_location)
        contract_form = ContractForm(request.POST, instance=contract)
        
        if project_form.is_valid() and proj_location_form.is_valid() and contract_form.is_valid():
            try:
                with transaction.atomic():
                    project = project_form.save(commit=False)
                    project.user = request.user
                    project.save()
                    
                    location = proj_location_form.save(commit=False)
                    location.project = project 
                    location.save()
                    
                    contract = contract_form.save(commit=False)
                    contract.project = project
                    contract.user = request.user
                    contract.save()
                    
                    contract_amend.amendment_contract_number = contract.number
                    contract_amend.amendment_end_date = contract.end_date
                    contract_amend.amendment_amount = contract.amount
                    contract_amend.user = request.user
                    contract_amend.save()
                    
                    
                    messages.success(request, "Projetu aktualiza ho susesu!")
                    return redirect('proj-detail', project.uuid)
                    
            except Exception as e:
                messages.error(request, f"Mosu erro wainhira rai dadus: {str(e)}")
        else:
            messages.error(request, "Favor bele hadi'ak fali erro iha okos wainhira submete formulario.")
            
    else:
        project_form = ProjectForm(instance=project)
        proj_location_form = ProjectLocationForm(instance=proj_location)
        contract_form = ContractForm(instance=contract)

    conteudo = {
        "title": "Atualiza Projetu",
        "subtitle": "Formulario Atualiza Projeto",
        "group": group,
        "project_form": project_form,
        "proj_location_form": proj_location_form,
        "contract_form": contract_form,
        "project": project, 
    }
    
    return render(request, 'project/form3.html', conteudo)


@login_required
@allow_user(allow_roles=['admin' , 'focal_point', 'finance', 'diretor'])
def ProjectDetail(request, uuid):
    group = request.user.groups.all()[0].name
    project = get_object_or_404(Project, uuid=uuid)
    location = get_object_or_404(ProjectLocation, project=project)
    contract = get_object_or_404(Contract, project=project)
    amd_contract = ContractAmendment.objects.filter(project=project).last()
    allocations = Allocation.objects.filter(project=project).all().order_by('-year')
    allocation = Allocation.objects.filter(project=project, is_active=True).last()
    transferencia = Transferencia.objects.filter(project=project, allocation=allocation).order_by('-pk')
    amendment_amount = AmendmenAmount.objects.filter(project=project).order_by('-pk')
    amendment_time = AmendmenTime.objects.filter(project=project).order_by('-pk')
    payments = Payment.objects.filter(project=project).order_by('pk')
    status = ProjectStatus.objects.filter(project=project).last()
    justification = ProjectJustification.objects.filter(project=project).last()
    conteudo = {
        "title" : "Detalha Projeto",
        "subtitle": "Informasaun Projeto",
        'project' : project, 'location':location,  'amd_contract':amd_contract,
        'group':group, 'contract':contract, 'allocations':allocations, 
        'transferencia':transferencia, 'allocation':allocation, 'amendment_amount':amendment_amount,
        'amendment_time':amendment_time, 'payments':payments, 'status':status, 'justification':justification
    }
    return render(request, 'project/detail.html',conteudo)




@login_required
@allow_user(allow_roles=['admin', 'focal_point', 'finance'])
def ProjectStatusUpdate(request, uuid):
    project = get_object_or_404(Project, uuid=uuid)
    contract = project.contract_project
    group = request.user.groups.first().name if request.user.groups.exists() else "No Group"
    
    if request.method == "POST":
        form = ProjectStatusForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.project = project
            instance.user = request.user
            instance.save()

            if contract:
                contract.status = instance.status
                contract.save()
            
            
            messages.success(request, 'Susesu Hadia Estadu Projeto')
            return redirect('proj-detail', uuid)
        else:
            messages.error(request, 'Formulario invalidu, favor cek fali dadus.')
    else:
        form = ProjectStatusForm()
        
    conteudo = {
        "title": "Hadia Estadu Projeto",
        "subtitle": "Formulario Hadia Estadu Projeto",
        "group": group, 
        "form": form, 
        "uuid": uuid
    }
    
    return render(request, 'project/form2.html', conteudo)


@login_required
@allow_user(allow_roles=['admin', 'focal_point', 'finance'])
def ProjectJustificationUpdate(request, uuid):
    project = get_object_or_404(Project, uuid=uuid)
    group = request.user.groups.first().name if request.user.groups.exists() else "No Group"
    
    if request.method == "POST":
        form = ProjectJustificationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.project = project
            instance.user = request.user
            instance.save()

            
            messages.success(request, 'Susesu Aumenta Justifikasaun')
            return redirect('proj-detail', uuid)
        else:
            messages.error(request, 'Formulario invalidu, favor cek fali dadus.')
    else:
        form = ProjectJustificationForm()
        
    conteudo = {
        "title": "Aumenta Justifikasaun",
        "subtitle": "Formulario Aumenta Justifikasaun",
        "group": group, 
        "form": form, 
        "uuid": uuid
    }
    
    return render(request, 'project/form2.html', conteudo)