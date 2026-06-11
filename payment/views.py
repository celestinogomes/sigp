import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.contrib import messages
from django.db import transaction
from django.db.models import Subquery, OuterRef

from main.decorators import  allow_user

from payment.models import Payment, PaymentHistory
from payment.forms import PaymentForm
from project.models import Project
from allocation.models import Allocation
from contract.models import Contract, ContractAmendment
from funsionariu.models import Funsionariu


@login_required
@allow_user(allow_roles=['admin', 'finance', 'diretor'])
def PaymentLists(request):
    group = request.user.groups.all()[0].name
    
    latest_allocation = Payment.objects.filter(
        project_id=OuterRef('project_id')  
    ).order_by('-id').values('id')[:1]
    
    data = Payment.objects.filter(id=Subquery(latest_allocation))
    
    conteudo = {
        "title" : "Lista Pagamento",
        'data' : data,
        'group': group
    }
    return render(request, 'payment/list.html', conteudo)


@login_required
@allow_user(allow_roles=['focal_point'])
def PaymentFCLists(request):
    user_groups = request.user.groups.all()
    group = user_groups[0].name if user_groups.exists() else "No Group"
    try:
        funsionariu_obj = Funsionariu.objects.get(user=request.user)
        user_programs = funsionariu_obj.program.all()
    except Funsionariu.DoesNotExist:
        user_programs = None

    if request.user.is_superuser:
        latest_allocation = Payment.objects.filter(
            project_id=OuterRef('project_id')  
        ).order_by('-id').values('id')[:1]
    elif user_programs:
        latest_allocation = Payment.objects.filter(
            project__program__in=user_programs,
            project_id=OuterRef('project_id')  
        ).order_by('-id').values('id')[:1]
    else:
        latest_allocation = Payment.objects.filter(
            project_id=OuterRef('project_id')  
        ).order_by('-id').values('id')[:1]
    
    
    data = Payment.objects.filter(id=Subquery(latest_allocation))
    
    conteudo = {
        "title" : "Lista Pagamento",
        'data' : data,
        'group': group
    }
    return render(request, 'payment/list.html', conteudo)




@login_required
@transaction.atomic
@allow_user(allow_roles=['admin', 'focal_point', 'finance'])
def PaymentAdd(request, uuid):
    project = get_object_or_404(Project, uuid=uuid)
    
    current_year = datetime.date.today().year    
    allocation = Allocation.objects.filter(
        project=project, 
        is_active=True
    ).last()
    
    if not allocation:
        messages.error(
            request, 
            f'Alokasaun de dadus ba tinan {current_year} seidauk ativu ka seidauk kria. '
            f'Favor kria no ativa tiha alokasaun antes submete pagamento.'
        )
        return redirect('proj-detail', uuid)
        
    all_amount = allocation.allocation_total if allocation.allocation_total else Decimal('0.00')
    if all_amount <= 0:
        messages.error(request, 'Montante Alokasaun Total deit 0. Labele halo kalkulasaun pagamento.')
        return redirect('proj-detail', uuid)
    amendment = ContractAmendment.objects.filter(project=project).first()
    
    if amendment and amendment.amendment_amount:
        contract_base_amount = amendment.amendment_amount
    else:
        contract_obj = Contract.objects.filter(project=project).first()
        contract_base_amount = contract_obj.amount if contract_obj and contract_obj.amount else Decimal('0.00')
        
    if contract_base_amount <= 0:
        messages.error(request, 'Valor kontraktu deit 0 ka seidauk kria. Labele halo kalkulasaun kumulativu.')
        return redirect('proj-detail', uuid)

    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            new_payment = form.save(commit=False)
            new_payment.project = project
            new_payment.user = request.user
            
            current_payment_amount = Decimal(str(new_payment.payment_amount))
            
            current_execution = allocation.execution_amount if allocation.execution_amount else Decimal('0.00')
            
            if (current_execution + current_payment_amount) > all_amount:
                messages.error(
                    request, 
                    f'Erro: Pagamento foun ne\'e (${current_payment_amount}) ho akumulasaun tinan ne\'e '
                    f'($ {current_execution + current_payment_amount}) liu ona montante alokasaun tinan {current_year} ($ {all_amount})!'
                )
                return redirect('payment-add', uuid)            
            last_payment = Payment.objects.filter(project=project).last()
            previous_comulative = last_payment.comulative_amount if last_payment else Decimal('0.00')
            
            new_payment.comulative_amount = previous_comulative + current_payment_amount
            new_payment.comulative_percent = (new_payment.comulative_amount / contract_base_amount) * 100
            
            new_payment.balance_amount = contract_base_amount - new_payment.comulative_amount
            new_payment.balance_percent = (new_payment.balance_amount / contract_base_amount) * 100
            new_payment.contract_amount = project.project_contract_amendment.amendment_amount if project.project_contract_amendment else Decimal('0.00')
            
            new_payment.save()
            
            allocation.execution_amount = current_execution + current_payment_amount
            allocation.execution_percent = (allocation.execution_amount / all_amount) * 100
            allocation.contract_balance = all_amount - allocation.execution_amount
            allocation.balance_percent = (allocation.contract_balance / all_amount) * 100
            allocation.save()
            
            messages.success(request, 'Pagamento foun aumenta no sinkroniza ona ho Alokasaun & Kontraktu.')
            return redirect('proj-detail', uuid)
        else:
            messages.error(request, 'Formulario invalidu, favor hafoun fali.')
    else:
        form = PaymentForm()
        
    conteudo = {
        'form': form, 'uuid': uuid,
        'title': "Aumenta Pagamento", 
        'subtitle': "Formulario Aumenta Pagamento",
        'project': project, 
        'allocation': allocation,
        'all_amount': all_amount,
        'contract_base_amount': contract_base_amount
    }
    return render(request, 'payment/form.html', conteudo)



@login_required
@allow_user(allow_roles=['admin', 'focal_point', 'finance'])
def PaymentArchivedAndRefresh(request, uuid):
    project = get_object_or_404(Project, uuid=uuid)
    
    amd_contract = ContractAmendment.objects.filter(project=project).last()
    
    if not amd_contract:
        messages.error(request, "Kontratu amandemen seidauk iha!")
        return redirect('proj-detail', uuid=uuid) # Sesuaikan nama URL detail project Anda

    new_contract_amount = amd_contract.amendment_amount
    active_payments = Payment.objects.filter(project=project).order_by('date', 'datetime')

    if not active_payments.exists():
        messages.warning(request, "Seidauk iha dadus pagamento atu arkiva.")
        return redirect('proj-detail', uuid=uuid)

    with transaction.atomic():
        
        for pay in active_payments:
            PaymentHistory.objects.create(
                user=request.user,
                project=pay.project,
                contract_amount = pay.contract_amount,
                physical_progress=pay.physical_progress,
                description=pay.description,
                payment_amount=pay.payment_amount,
                comulative_amount=pay.comulative_amount,
                comulative_percent=pay.comulative_percent,
                balance_amount=pay.balance_amount,
                balance_percent=pay.balance_percent,
                process_number=pay.process_number,
                date=pay.date,
                info="Arkivo"
            )

        running_cumulative = 0
        for pay in active_payments:
            pay.contract_amount = new_contract_amount            
            running_cumulative += pay.payment_amount
            pay.comulative_amount = running_cumulative            
            if new_contract_amount > 0:
                pay.comulative_percent = (pay.comulative_amount / new_contract_amount) * 100
                pay.balance_amount = new_contract_amount - pay.comulative_amount
                pay.balance_percent = (pay.balance_amount / new_contract_amount) * 100
            else:
                pay.comulative_percent = 0
                pay.balance_amount = 0
                pay.balance_percent = 0
                
            pay.user = request.user 
            pay.save()

        messages.success(request, "Pagamento susesu arkiva no kalkula fali ona bazeia ba kontratu foun.")

    return redirect('proj-detail', uuid=uuid)


@login_required
@allow_user(allow_roles=['admin', 'focal_point', 'finance', 'diretor'])
def PaymentHistoryLists(request, uuid):
    project = get_object_or_404(Project, uuid=uuid)
    
    history_payments = PaymentHistory.objects.filter(project=project).order_by('-datetime', 'date')
    
    conteudo = {
        "title": "Historia Pagamento",
        "subtitle": f"Projetu: {project.name}", 
        "project": project,
        "history_payments": history_payments,
    }
    return render(request, 'payment_history/history.html', conteudo)


@login_required
@allow_user(allow_roles=['admin', 'focal_point', 'finance'])
def PaymentUpdate(request, uuid):
    payment_instance = get_object_or_404(Payment, uuid=uuid)
    project = payment_instance.project

    allocation = Allocation.objects.filter(project=project, is_active=True).last()

    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment_instance)
        if form.is_valid():
            with transaction.atomic():
                updated_payment = form.save(commit=False)
                updated_payment.user = request.user
                updated_payment.save()

                amd_contract = ContractAmendment.objects.filter(project=project).last()
                contract = Contract.objects.filter(project=project).last()
                current_contract_amount = amd_contract.amendment_amount if amd_contract else (contract.amount if contract else Decimal('0.00'))

                all_payments = Payment.objects.filter(project=project).order_by('date', 'datetime')
                
                running_cumulative = Decimal('0.00')
                total_execution_this_allocation = Decimal('0.00') # Untuk hitung ulang Alokasi

                for pay in all_payments:
                    pay.contract_amount = current_contract_amount
                    
                    running_cumulative += Decimal(str(pay.payment_amount))
                    pay.comulative_amount = running_cumulative
                    
                    if current_contract_amount > 0:
                        pay.comulative_percent = (pay.comulative_amount / current_contract_amount) * 100
                        pay.balance_amount = current_contract_amount - pay.comulative_amount
                        pay.balance_percent = (pay.balance_amount / current_contract_amount) * 100
                    else:
                        pay.comulative_percent = Decimal('0.00')
                        pay.balance_amount = Decimal('0.00')
                        pay.balance_percent = Decimal('0.00')
                    
                    pay.save()

                    total_execution_this_allocation += Decimal(str(pay.payment_amount))

                if allocation:
                    all_amount = allocation.allocation_total if allocation.allocation_total else Decimal('0.00')
                    
                    if all_amount > 0:
                        if total_execution_this_allocation > all_amount:
                            messages.error(
                                request, 
                                f"Erro: Total montante pagamento (${total_execution_this_allocation}) "
                                f"liu ona montante alokasaun ne'ebé ativu ($ {all_amount})!"
                            )
                            raise Exception("Alokasaun Liu")

                        allocation.execution_amount = total_execution_this_allocation
                        allocation.execution_percent = (allocation.execution_amount / all_amount) * 100
                        allocation.contract_balance = all_amount - allocation.execution_amount
                        allocation.balance_percent = (allocation.contract_balance / all_amount) * 100
                        allocation.save()

                messages.success(request, "Susesu update pagamento no sinkroniza ona ho Alokasaun & Kontraktu.")
                return redirect('proj-detail', uuid=project.uuid)
                
        else:
            messages.error(request, 'Formulario invalidu, favor hafoun fali.')
            
    else:
        form = PaymentForm(instance=payment_instance)

    conteudo = {
        'title': 'Altera Pagamento',
        'subtitle': f'Projetu: {project.name}',
        'form': form,
        'payment': payment_instance,
        'project': project, 'uuid':project.uuid
    }
    return render(request, 'payment/form.html', conteudo)