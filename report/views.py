import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from main.decorators import  allow_user
from django.contrib import messages
from django.db.models import Sum, Count, Value, DecimalField, Q
from django.db.models.functions import Cast
from django.db.models.functions import Coalesce

from project.models import Project, ProjectLocation, Program, SubProgram, Owner, ProjectJustification
from contract.models import Contract, ContractAmendment
from allocation.models import Allocation, Transferencia
from amendment.models import AmendmenAmount, AmendmenTime
from payment.models import Payment, PaymentHistory
from custom.models import Ano
from django.db.models.functions import ExtractMonth

@login_required
@allow_user(allow_roles=['admin', 'focal_point', 'diretor', 'finance'])
def RDashboard(request):
    year_now = str(datetime.date.today().year)    
    year_selected = request.GET.get('year', year_now)
    ano_obj = Ano.objects.filter(ano=year_selected).first() 

    allocation = Allocation.objects.filter(year=ano_obj).aggregate(
        sum_allocation=Sum('allocation_total'),
        sum_execution=Sum('execution_amount')
    ) if ano_obj else {'sum_allocation': 0, 'sum_execution': 0}

    total_alocation = allocation.get('sum_allocation') or 0
    total_execution = allocation.get('sum_execution') or 0
    total_balance = total_alocation - total_execution

    per_execution = 0
    if total_alocation > 0:
        per_execution = round((total_execution / total_alocation) * 100, 2)

    total_programa = Project.objects.filter(project_allocation__year=ano_obj).distinct().aggregate(
        total=Count('program', distinct=True)
    )['total'] or 0

    total_dono = Project.objects.filter(project_allocation__year=ano_obj).distinct().aggregate(
        total=Count('owner', distinct=True)
    )['total'] or 0

    chart_payment_month = [0] * 12  
    chart_total_project = [0] * 12  
    if ano_obj:
        payments_by_month = Payment.objects.filter(date__year=year_selected)\
            .annotate(month=ExtractMonth('date'))\
            .values('month')\
            .annotate(
                total_dana_terbayar=Sum('payment_amount'),
                jumlah_proyek_terbayar=Count('project', distinct=True) 
            ).order_by('month')

        for record in payments_by_month:
            if record['month']:
                month_index = record['month'] - 1
                if 0 <= month_index < 12:
                    chart_payment_month[month_index] = float(record['total_dana_terbayar'] or 0)
                    chart_total_project[month_index] = int(record['jumlah_proyek_terbayar'] or 0)

    lista_anos = Ano.objects.all().order_by('-ano')

    conteudo = {
        "title": "Painel Relatorio",
        "subtitle": "Painel Relatorio",
        "year_selected": year_selected,
        "lista_anos": lista_anos,  
        
        "total_alocation": total_alocation,
        "total_execution": total_execution,
        "total_balance": total_balance,
        "per_execution": per_execution,
        
        "total_programa": total_programa,
        "total_dono": total_dono,
        
        "chart_payment_month": chart_payment_month, 
        "chart_total_project": chart_total_project, 
    }
    
    return render(request, 'report/dashboard.html', conteudo)




@login_required
@allow_user(allow_roles=['admin', 'focal_point', 'diretor', 'finance'])
def RProgramDashboard(request, year):
    year_selected = str(year)
    
    programs_data = Program.objects.filter(
        project_program__project_allocation__year__ano=year_selected
    ).annotate(
        total_allocation=Coalesce(
            Sum('project_program__project_allocation__allocation_total', 
                filter=Q(project_program__project_allocation__year__ano=year_selected)), 
            0.00, output_field=DecimalField()
        ),
        total_execution=Coalesce(
            Sum('project_program__project_allocation__execution_amount', 
                filter=Q(project_program__project_allocation__year__ano=year_selected)), 
            0.00, output_field=DecimalField()
        ),
        total_balance=Coalesce(
            Sum('project_program__project_allocation__contract_balance', 
                filter=Q(project_program__project_allocation__year__ano=year_selected)), 
            0.00, output_field=DecimalField()
        )
    ).distinct()

    programs_report = []
    
    for program in programs_data:
        prog_execution_percent = 0.00
        prog_balance_percent = 0.00
        if program.total_allocation > 0:
            prog_execution_percent = (program.total_execution / program.total_allocation) * 100
            prog_balance_percent = (program.total_balance / program.total_allocation) * 100

        sub_programs_data = SubProgram.objects.filter(
            program=program,
            project_sub_program__project_allocation__year__ano=year_selected
        ).annotate(
            sub_allocation=Coalesce(
                Sum('project_sub_program__project_allocation__allocation_total', 
                    filter=Q(project_sub_program__project_allocation__year__ano=year_selected)), 
                0.00, output_field=DecimalField()
            ),
            sub_execution=Coalesce(
                Sum('project_sub_program__project_allocation__execution_amount', 
                    filter=Q(project_sub_program__project_allocation__year__ano=year_selected)), 
                0.00, output_field=DecimalField()
            ),
            sub_balance=Coalesce(
                Sum('project_sub_program__project_allocation__contract_balance', 
                    filter=Q(project_sub_program__project_allocation__year__ano=year_selected)), 
                0.00, output_field=DecimalField()
            )
        ).distinct()

        sub_programs_list = []
        for sub in sub_programs_data:
            sub_execution_percent = 0.00
            sub_balance_percent = 0.00
            if sub.sub_allocation > 0:
                sub_execution_percent = (sub.sub_execution / sub.sub_allocation) * 100
                sub_balance_percent = (sub.sub_balance / sub.sub_allocation) * 100
            
            sub_programs_list.append({
                'code': sub.code,
                'name': sub.name,
                'id': sub.id,
                'allocation': sub.sub_allocation,
                'execution': sub.sub_execution,
                'balance': sub.sub_balance,
                'execution_percent': sub_execution_percent,
                'balance_percent': sub_balance_percent,
            })

        programs_report.append({
            'code': getattr(program, 'code', ''),  
            'name': program.name,
            'id': program.id,
            'allocation': program.total_allocation,
            'execution': program.total_execution,
            'balance': program.total_balance,
            'execution_percent': prog_execution_percent,
            'balance_percent': prog_balance_percent,
            'sub_programs': sub_programs_list, 
        })

    total_all_allocation = sum(item['allocation'] for item in programs_report)
    total_all_execution = sum(item['execution'] for item in programs_report)
    total_all_balance = sum(item['balance'] for item in programs_report)
    
    total_all_execution_percent = 0.00
    total_all_balance_percent = 0.00
    if total_all_allocation > 0:
        total_all_execution_percent = (total_all_execution / total_all_allocation) * 100
        total_all_balance_percent = (total_all_balance / total_all_allocation) * 100

    context = {
        "title": "Painel Relatorio Programa",
        "subtitle": "Painel Relatorio Programa & Sub Programa",
        "year_selected": year_selected,
        "programs_report": programs_report,
        "summary": {
            "allocation": total_all_allocation,
            "execution": total_all_execution,
            "balance": total_all_balance,
            "execution_percent": total_all_execution_percent,
            "balance_percent": total_all_balance_percent,
        }
    }
    
    return render(request, 'report_program/program.html', context)




@login_required
@allow_user(allow_roles=['admin', 'focal_point', 'diretor', 'finance'])
def ROwnerDashboard(request, year):
    year_selected = str(year)
    
    owners_data = Owner.objects.filter(
        project_owner__project_allocation__year__ano=year_selected
    ).annotate(
        total_allocation=Coalesce(
            Sum('project_owner__project_allocation__allocation_total', 
                filter=Q(project_owner__project_allocation__year__ano=year_selected)), 
            0.00, output_field=DecimalField()
        ),
        total_execution=Coalesce(
            Sum('project_owner__project_allocation__execution_amount', 
                filter=Q(project_owner__project_allocation__year__ano=year_selected)), 
            0.00, output_field=DecimalField()
        ),
        total_balance=Coalesce(
            Sum('project_owner__project_allocation__contract_balance', 
                filter=Q(project_owner__project_allocation__year__ano=year_selected)), 
            0.00, output_field=DecimalField()
        )
    ).distinct()

    owners_report = []
    
    for owner in owners_data:
        owner_execution_percent = 0.00
        owner_balance_percent = 0.00
        if owner.total_allocation > 0:
            owner_execution_percent = (owner.total_execution / owner.total_allocation) * 100
            owner_balance_percent = (owner.total_balance / owner.total_allocation) * 100

        owners_report.append({
            'code': owner.code,
            'name': owner.name,
            'id': owner.id,
            'allocation': owner.total_allocation,
            'execution': owner.total_execution,
            'balance': owner.total_balance,
            'execution_percent': owner_execution_percent,
            'balance_percent': owner_balance_percent,
        })

    total_all_allocation = sum(item['allocation'] for item in owners_report)
    total_all_execution = sum(item['execution'] for item in owners_report)
    total_all_balance = sum(item['balance'] for item in owners_report)
    
    total_all_execution_percent = 0.00
    total_all_balance_percent = 0.00
    if total_all_allocation > 0:
        total_all_execution_percent = (total_all_execution / total_all_allocation) * 100
        total_all_balance_percent = (total_all_balance / total_all_allocation) * 100

    context = {
        "title": "Painel Relatorio Dono do Projeto (Owner)",
        "subtitle": "Painel Relatorio Finansas por Owner",
        "year_selected": year_selected,
        "owners_report": owners_report,
        "summary": {
            "allocation": total_all_allocation,
            "execution": total_all_execution,
            "balance": total_all_balance,
            "execution_percent": total_all_execution_percent,
            "balance_percent": total_all_balance_percent,
        }
    }
    
    return render(request, 'report_owner/owner.html', context)


@login_required
def RListAll(request, year):
    year_selected = request.GET.get('year', year)
    ano_obj = Ano.objects.filter(ano=year_selected).first()

    project_list_data = []

    if ano_obj:
        projects = Project.objects.filter(
            project_allocation__year=ano_obj
        ).select_related(
            'program', 'sub_program', 'owner', 'fund', 'type', 'project_location',
            'project_location__municipality', 'project_location__administrative_post', 'project_location__village'
        ).distinct().order_by('id')

        for index, proj in enumerate(projects, start=1):
            last_amend_amount = proj.amendment_amount_project.all().order_by('-id').first()
            total_amend_amount_count = proj.amendment_amount_project.count()

            last_amend_time = proj.amendment_time_project.all().order_by('-id').first()
            total_amend_time_count = proj.amendment_time_project.count()
            

            alloc_year = proj.project_allocation.filter(year=ano_obj).first()

            last_transfer = proj.transferencia_project.all().order_by('-id').first()
            transfer_count = proj.transferencia_project.count()

            last_payment = proj.payment_project.all().order_by('-id').first()

            contract_original = proj.contract_project
            contract_final = proj.project_contract_amendment if hasattr(proj, 'project_contract_amendment') else None
            justification = ProjectJustification.objects.filter(project=proj).last()
            project_list_data.append({
                'no': index,
                'uuid': proj.uuid,
                'activity_code': proj.activity_code,
                'program_code': proj.program.code if proj.program else '-',
                'program_name': proj.program.name if proj.program else '-',
                'sub_program_code': proj.sub_program.code if proj.sub_program else '-',
                'sub_program_name': proj.sub_program.name if proj.sub_program else '-',
                'owner': proj.owner.name if proj.owner else '-',
                'owner_code': proj.owner.code if proj.owner else '-',
                'fund_code': proj.fund.code if proj.fund else '-',
                'fund': proj.fund.name if proj.fund else '-',
                'project_name': proj.name,
                
                # Lokalizasaun
                'municipality': proj.project_location.municipality.name if hasattr(proj, 'project_location') and proj.project_location.municipality else '-',
                'administrative_post': proj.project_location.administrative_post.name if hasattr(proj, 'project_location') and proj.project_location.administrative_post else '-',
                'village': proj.project_location.village.name if hasattr(proj, 'project_location') and proj.project_location.village else '-',
                'aldeia': proj.project_location.aldeia.name if hasattr(proj, 'project_location') and proj.project_location.aldeia else '-',
                'latitude_start': proj.project_location.latitude_start if hasattr(proj, 'project_location') and proj.project_location.latitude_start else '-',
                'longitude_start': proj.project_location.longitude_start if hasattr(proj, 'project_location') and proj.project_location.longitude_start else '-',
                'latitude_end': proj.project_location.latitude_end if hasattr(proj, 'project_location') and proj.project_location.latitude_end else '-',
                'longitude_end': proj.project_location.longitude_end if hasattr(proj, 'project_location') and proj.project_location.longitude_end else '-',

                # Kontratu Original & Amandemen
                'company': contract_original.company if contract_original else '-',
                'contract_number': contract_original.number if contract_original else '-',
                #'contract_start': contract_original.date if contract_original else '-',
                #'contract_end': last_amend_time.end_date if last_amend_time else '-',
                #'contract_end': last_amend_time.end_date if last_amend_time else (contract_original.end_date if contract_original else '-'),
                'contract_start': getattr(contract_original, 'start_date', '-') or getattr(contract_original, 'date', '-'),
                'contract_end': getattr(last_amend_time, 'end_date', '-') or getattr(contract_original, 'end_date', '-'),
                'contract_original': contract_original.amount,
                'project_type': proj.type.name if proj.type else '-',

                # Bank Guarantee
                'performance_security': contract_original.contract_bank_guarantee.first().performance_security if contract_original and contract_original.contract_bank_guarantee.exists() else 0.00,
                'advance_payment': contract_original.contract_bank_guarantee.first().advance_payment if contract_original and contract_original.contract_bank_guarantee.exists() else 0.00,
                'retention': contract_original.contract_bank_guarantee.first().retention if contract_original and contract_original.contract_bank_guarantee.exists() else 0.00,
                'performance_security_amount': contract_original.contract_bank_guarantee.first().performance_security_amount if contract_original and contract_original.contract_bank_guarantee.exists() else 0.00,
                'amount_advance_payment': contract_original.contract_bank_guarantee.first().amount_advance_payment if contract_original and contract_original.contract_bank_guarantee.exists() else 0.00,
                'retention_amount': contract_original.contract_bank_guarantee.first().retention_amount if contract_original and contract_original.contract_bank_guarantee.exists() else 0.00,
                
                #  Amandemen


                'amend_cost_no': last_amend_amount.number if last_amend_amount else '-',
                'amend_cost_amount': last_amend_amount.amount if last_amend_amount else 0.00,
                'amend_time_no': last_amend_time.number if last_amend_time else '-',
                'amend_time_date': last_amend_time.date if last_amend_time else '-',
                'total_amend_time_count': total_amend_time_count,
                'total_amend_amount_count': total_amend_amount_count,
                
                'contract_final': contract_final.amendment_amount if contract_final and hasattr(contract_final, 'amendment_amount') else 0.00,
                'owner_estimation': proj.owner_estimation or 0.00,
                'total_project_cost': contract_final, 
                
                # Alokasaun & Transferensia
                'alloc_original': alloc_year.allocation_original if alloc_year else 0.00,
                'transfer_amount': last_transfer.transferencia if last_transfer else 0.00,
                'transfer_count_info': f"Transf. ba-{transfer_count}" if transfer_count > 0 else "Laiha Transferensia",
                'alloc_total': alloc_year.allocation_total if alloc_year else 0.00,
                
                # Pagamento
                'payment_date': last_payment.date if last_payment else '-',
                'payment': last_payment.payment_amount if last_payment else '-',
                'physical_progress': last_payment.physical_progress if last_payment else '-',
                'payment_cumulative': last_payment.comulative_amount if last_payment else 0.00,
                'payment_cumulative_percent': last_payment.comulative_percent if last_payment else 0.00,
                'payment_balance': last_payment.balance_amount if last_payment else 0.00,
                'payment_balance_percent': last_payment.balance_percent if last_payment else 0.00,
                
                # Status & Adisional
                'status': contract_original.status if contract_original.status else "-",
                'justification': justification.description if justification else '-'
            })

    lista_anos = Ano.objects.all().order_by('-ano')

    conteudo = {
        "title": f"Lista Pagamento Tinan {year_selected}",
        "year_selected": year_selected,
        "lista_anos": lista_anos,  
        "project_list_data": project_list_data,
    }
    
    return render(request, 'report/list.html', conteudo)



@login_required
def RProgramListAll(request, year, pk):
    year_selected = request.GET.get('year', year)
    program = get_object_or_404(Program, pk=pk)
    ano_obj = Ano.objects.filter(ano=year_selected).first()

    project_list_data = []

    if ano_obj:
        projects = Project.objects.filter(
            project_allocation__year=ano_obj, program=program
        ).select_related(
            'program', 'sub_program', 'owner', 'fund', 'type', 'project_location',
            'project_location__municipality', 'project_location__administrative_post', 'project_location__village'
        ).distinct().order_by('id')

        for index, proj in enumerate(projects, start=1):
            last_amend_amount = proj.amendment_amount_project.all().order_by('-id').first()
            total_amend_amount_count = proj.amendment_amount_project.count()

            last_amend_time = proj.amendment_time_project.all().order_by('-id').first()
            total_amend_time_count = proj.amendment_time_project.count()
            

            alloc_year = proj.project_allocation.filter(year=ano_obj).first()

            last_transfer = proj.transferencia_project.all().order_by('-id').first()
            transfer_count = proj.transferencia_project.count()

            last_payment = proj.payment_project.all().order_by('-id').first()

            contract_original = proj.contract_project
            contract_final = proj.project_contract_amendment
            justification = ProjectJustification.objects.filter(project=proj).last()
            project_list_data.append({
                'no': index,
                'uuid': proj.uuid,
                'activity_code': proj.activity_code,
                'program_code': proj.program.code if proj.program else '-',
                'program_name': proj.program.name if proj.program else '-',
                'sub_program_code': proj.sub_program.code if proj.sub_program else '-',
                'sub_program_name': proj.sub_program.name if proj.sub_program else '-',
                'owner': proj.owner.name if proj.owner else '-',
                'owner_code': proj.owner.code if proj.owner else '-',
                'fund_code': proj.fund.code if proj.fund else '-',
                'fund': proj.fund.name if proj.fund else '-',
                'project_name': proj.name,
                
                # Lokalizasaun
                'municipality': proj.project_location.municipality.name if hasattr(proj, 'project_location') and proj.project_location.municipality else '-',
                'administrative_post': proj.project_location.administrative_post.name if hasattr(proj, 'project_location') and proj.project_location.administrative_post else '-',
                'village': proj.project_location.village.name if hasattr(proj, 'project_location') and proj.project_location.village else '-',
                'aldeia': proj.project_location.aldeia.name if hasattr(proj, 'project_location') and proj.project_location.aldeia else '-',
                'latitude_start': proj.project_location.latitude_start if hasattr(proj, 'project_location') and proj.project_location.latitude_start else '-',
                'longitude_start': proj.project_location.longitude_start if hasattr(proj, 'project_location') and proj.project_location.longitude_start else '-',
                'latitude_end': proj.project_location.latitude_end if hasattr(proj, 'project_location') and proj.project_location.latitude_end else '-',
                'longitude_end': proj.project_location.longitude_end if hasattr(proj, 'project_location') and proj.project_location.longitude_end else '-',
                
                # Kontratu Original & Amandemen
                'company': contract_original.company if contract_original else '-',
                'contract_number': contract_original.number if contract_original else '-',
                #'contract_start': last_amend_time.date if last_amend_time else '-',
                #'contract_end': last_amend_time.end_date if last_amend_time else '-',
                'contract_start': getattr(contract_original, 'start_date', '-') or getattr(contract_original, 'date', '-'),
                'contract_end': getattr(last_amend_time, 'end_date', '-') or getattr(contract_original, 'end_date', '-'),
                'contract_original': contract_original.amount,
                'project_type': proj.type.name if proj.type else '-',

                # Bank Guarantee
                'performance_security': contract_original.contract_bank_guarantee.first().performance_security if contract_original and contract_original.contract_bank_guarantee.exists() else 0.00,
                'advance_payment': contract_original.contract_bank_guarantee.first().advance_payment if contract_original and contract_original.contract_bank_guarantee.exists() else 0.00,
                'retention': contract_original.contract_bank_guarantee.first().retention if contract_original and contract_original.contract_bank_guarantee.exists() else 0.00,
                'performance_security_amount': contract_original.contract_bank_guarantee.first().performance_security_amount if contract_original and contract_original.contract_bank_guarantee.exists() else 0.00,
                'amount_advance_payment': contract_original.contract_bank_guarantee.first().amount_advance_payment if contract_original and contract_original.contract_bank_guarantee.exists() else 0.00,
                'retention_amount': contract_original.contract_bank_guarantee.first().retention_amount if contract_original and contract_original.contract_bank_guarantee.exists() else 0.00,
                
                # Amandemen

                
                'amend_cost_no': last_amend_amount.number if last_amend_amount else '-',
                'amend_cost_amount': last_amend_amount.amount if last_amend_amount else 0.00,
                'amend_time_no': last_amend_time.number if last_amend_time else '-',
                'amend_time_date': last_amend_time.date if last_amend_time else '-',
                'total_amend_time_count': total_amend_time_count,
                'total_amend_amount_count': total_amend_amount_count,
                
                'contract_final': contract_final.amendment_amount,
                'owner_estimation': proj.owner_estimation or 0.00,
                'total_project_cost': contract_final, 
                
                # Alokasaun & Transferensia
                'alloc_original': alloc_year.allocation_original if alloc_year else 0.00,
                'transfer_amount': last_transfer.transferencia if last_transfer else 0.00,
                'transfer_count_info': f"Transf. ba-{transfer_count}" if transfer_count > 0 else "Laiha Transferensia",
                'alloc_total': alloc_year.allocation_total if alloc_year else 0.00,
                
                # Pagamento
                'payment_date': last_payment.date if last_payment else '-',
                'payment': last_payment.payment_amount if last_payment else '-',
                'physical_progress': last_payment.physical_progress if last_payment else '-',
                'payment_cumulative': last_payment.comulative_amount if last_payment else 0.00,
                'payment_cumulative_percent': last_payment.comulative_percent if last_payment else 0.00,
                'payment_balance': last_payment.balance_amount if last_payment else 0.00,
                'payment_balance_percent': last_payment.balance_percent if last_payment else 0.00,
                
                # Status & Adisional
                'status': contract_original.status if contract_original.status else "-",
                'justification': justification.description if justification else '-'
            })

    lista_anos = Ano.objects.all().order_by('-ano')

    conteudo = {
        "title": f"Lista Projeto tuir Programa {program.name} Tinan {year_selected}",
        "year_selected": year_selected,
        "lista_anos": lista_anos,  
        "project_list_data": project_list_data,
    }
    
    return render(request, 'report/list.html', conteudo)


@login_required
def RSubProgramListAll(request, year, pk):
    year_selected = request.GET.get('year', year)
    subprogram = get_object_or_404(SubProgram, pk=pk)
    ano_obj = Ano.objects.filter(ano=year_selected).first()

    project_list_data = []

    if ano_obj:
        projects = Project.objects.filter(
            project_allocation__year=ano_obj, sub_program=subprogram
        ).select_related(
            'program', 'sub_program', 'owner', 'fund', 'type', 'project_location',
            'project_location__municipality', 'project_location__administrative_post', 'project_location__village'
        ).distinct().order_by('id')

        for index, proj in enumerate(projects, start=1):
            last_amend_amount = proj.amendment_amount_project.all().order_by('-id').first()
            total_amend_amount_count = proj.amendment_amount_project.count()

            last_amend_time = proj.amendment_time_project.all().order_by('-id').first()
            total_amend_time_count = proj.amendment_time_project.count()
            

            alloc_year = proj.project_allocation.filter(year=ano_obj).first()

            last_transfer = proj.transferencia_project.all().order_by('-id').first()
            transfer_count = proj.transferencia_project.count()

            last_payment = proj.payment_project.all().order_by('-id').first()

            contract_original = proj.contract_project
            contract_final = proj.project_contract_amendment
            justification = ProjectJustification.objects.filter(project=proj).last()
            project_list_data.append({
                'no': index,
                'uuid': proj.uuid,
                'activity_code': proj.activity_code,
                'program_code': proj.program.code if proj.program else '-',
                'program_name': proj.program.name if proj.program else '-',
                'sub_program_code': proj.sub_program.code if proj.sub_program else '-',
                'sub_program_name': proj.sub_program.name if proj.sub_program else '-',
                'owner': proj.owner.name if proj.owner else '-',
                'owner_code': proj.owner.code if proj.owner else '-',
                'fund_code': proj.fund.code if proj.fund else '-',
                'fund': proj.fund.name if proj.fund else '-',
                'project_name': proj.name,
                
                # Lokalizasaun
                'municipality': proj.project_location.municipality.name if hasattr(proj, 'project_location') and proj.project_location.municipality else '-',
                'administrative_post': proj.project_location.administrative_post.name if hasattr(proj, 'project_location') and proj.project_location.administrative_post else '-',
                'village': proj.project_location.village.name if hasattr(proj, 'project_location') and proj.project_location.village else '-',
                'aldeia': proj.project_location.aldeia.name if hasattr(proj, 'project_location') and proj.project_location.aldeia else '-',
                'latitude_start': proj.project_location.latitude_start if hasattr(proj, 'project_location') and proj.project_location.latitude_start else '-',
                'longitude_start': proj.project_location.longitude_start if hasattr(proj, 'project_location') and proj.project_location.longitude_start else '-',
                'latitude_end': proj.project_location.latitude_end if hasattr(proj, 'project_location') and proj.project_location.latitude_end else '-',
                'longitude_end': proj.project_location.longitude_end if hasattr(proj, 'project_location') and proj.project_location.longitude_end else '-',
                
                # Kontratu Original & Amandemen
                'company': contract_original.company if contract_original else '-',
                'contract_number': contract_original.number if contract_original else '-',
                'contract_start': getattr(contract_original, 'start_date', '-') or getattr(contract_original, 'date', '-'),
                'contract_end': getattr(last_amend_time, 'end_date', '-') or getattr(contract_original, 'end_date', '-'),
                #'contract_start': last_amend_time.date if last_amend_time else '-',
                #'contract_end': last_amend_time.end_date if last_amend_time else '-',
                'contract_original': contract_original.amount,
                'project_type': proj.type.name if proj.type else '-',

                # Bank Guarantee
                'performance_security': contract_original.contract_bank_guarantee.first().performance_security if contract_original and contract_original.contract_bank_guarantee.exists() else 0.00,
                'advance_payment': contract_original.contract_bank_guarantee.first().advance_payment if contract_original and contract_original.contract_bank_guarantee.exists() else 0.00,
                'retention': contract_original.contract_bank_guarantee.first().retention if contract_original and contract_original.contract_bank_guarantee.exists() else 0.00,
                'performance_security_amount': contract_original.contract_bank_guarantee.first().performance_security_amount if contract_original and contract_original.contract_bank_guarantee.exists() else 0.00,
                'amount_advance_payment': contract_original.contract_bank_guarantee.first().amount_advance_payment if contract_original and contract_original.contract_bank_guarantee.exists() else 0.00,
                'retention_amount': contract_original.contract_bank_guarantee.first().retention_amount if contract_original and contract_original.contract_bank_guarantee.exists() else 0.00,
                
                # Amandemen
                
                'amend_cost_no': last_amend_amount.number if last_amend_amount else '-',
                'amend_cost_amount': last_amend_amount.amount if last_amend_amount else 0.00,
                'amend_time_no': last_amend_time.number if last_amend_time else '-',
                'amend_time_date': last_amend_time.date if last_amend_time else '-',
                'total_amend_time_count': total_amend_time_count,
                'total_amend_amount_count': total_amend_amount_count,
                
                'contract_final': contract_final.amendment_amount,
                'owner_estimation': proj.owner_estimation or 0.00,
                'total_project_cost': contract_final, # Total biaya proyek saat ini
                
                # Alokasaun & Transferensia
                'alloc_original': alloc_year.allocation_original if alloc_year else 0.00,
                'transfer_amount': last_transfer.transferencia if last_transfer else 0.00,
                'transfer_count_info': f"Transf. ba-{transfer_count}" if transfer_count > 0 else "Laiha Transferensia",
                'alloc_total': alloc_year.allocation_total if alloc_year else 0.00,
                
                # Pagamento
                'payment_date': last_payment.date if last_payment else '-',
                'payment': last_payment.payment_amount if last_payment else '-',
                'physical_progress': last_payment.physical_progress if last_payment else '-',
                'payment_cumulative': last_payment.comulative_amount if last_payment else 0.00,
                'payment_cumulative_percent': last_payment.comulative_percent if last_payment else 0.00,
                'payment_balance': last_payment.balance_amount if last_payment else 0.00,
                'payment_balance_percent': last_payment.balance_percent if last_payment else 0.00,
                
                # Status & Adisional
                'status': contract_original.status if contract_original.status else "-",
                'justification': justification.description if justification else '-'
            })

    lista_anos = Ano.objects.all().order_by('-ano')

    conteudo = {
        "title": f"Lista Projeto tuir Sub Programa {subprogram.name} Tinan {year_selected}",
        "year_selected": year_selected,
        "lista_anos": lista_anos,  
        "project_list_data": project_list_data,
    }
    
    return render(request, 'report/list.html', conteudo)



@login_required
def RSubOwnerListAll(request, year, pk):
    year_selected = request.GET.get('year', year)
    owner = get_object_or_404(Owner, pk=pk)
    ano_obj = Ano.objects.filter(ano=year_selected).first()

    project_list_data = []

    if ano_obj:
        projects = Project.objects.filter(
            project_allocation__year=ano_obj, owner=owner
        ).select_related(
            'program', 'sub_program', 'owner', 'fund', 'type', 'project_location',
            'project_location__municipality', 'project_location__administrative_post', 'project_location__village'
        ).distinct().order_by('id')

        for index, proj in enumerate(projects, start=1):
            last_amend_amount = proj.amendment_amount_project.all().order_by('-id').first()
            total_amend_amount_count = proj.amendment_amount_project.count()

            last_amend_time = proj.amendment_time_project.all().order_by('-id').first()
            total_amend_time_count = proj.amendment_time_project.count()
            

            alloc_year = proj.project_allocation.filter(year=ano_obj).first()

            last_transfer = proj.transferencia_project.all().order_by('-id').first()
            transfer_count = proj.transferencia_project.count()

            last_payment = proj.payment_project.all().order_by('-id').first()

            contract_original = proj.contract_project
            contract_final = proj.project_contract_amendment
            justification = ProjectJustification.objects.filter(project=proj).last()
            project_list_data.append({
                'no': index,
                'uuid': proj.uuid,
                'activity_code': proj.activity_code,
                'program_code': proj.program.code if proj.program else '-',
                'program_name': proj.program.name if proj.program else '-',
                'sub_program_code': proj.sub_program.code if proj.sub_program else '-',
                'sub_program_name': proj.sub_program.name if proj.sub_program else '-',
                'owner': proj.owner.name if proj.owner else '-',
                'owner_code': proj.owner.code if proj.owner else '-',
                'fund_code': proj.fund.code if proj.fund else '-',
                'fund': proj.fund.name if proj.fund else '-',
                'project_name': proj.name,
                
                # Lokalizasaun
                'municipality': proj.project_location.municipality.name if hasattr(proj, 'project_location') and proj.project_location.municipality else '-',
                'administrative_post': proj.project_location.administrative_post.name if hasattr(proj, 'project_location') and proj.project_location.administrative_post else '-',
                'village': proj.project_location.village.name if hasattr(proj, 'project_location') and proj.project_location.village else '-',
                'aldeia': proj.project_location.aldeia.name if hasattr(proj, 'project_location') and proj.project_location.aldeia else '-',
                'latitude_start': proj.project_location.latitude_start if hasattr(proj, 'project_location') and proj.project_location.latitude_start else '-',
                'longitude_start': proj.project_location.longitude_start if hasattr(proj, 'project_location') and proj.project_location.longitude_start else '-',
                'latitude_end': proj.project_location.latitude_end if hasattr(proj, 'project_location') and proj.project_location.latitude_end else '-',
                'longitude_end': proj.project_location.longitude_end if hasattr(proj, 'project_location') and proj.project_location.longitude_end else '-',
                
                # Kontratu Original & Amandemen
                'company': contract_original.company if contract_original else '-',
                'contract_number': contract_original.number if contract_original else '-',
                'contract_start': getattr(contract_original, 'start_date', '-') or getattr(contract_original, 'date', '-'),
                'contract_end': getattr(last_amend_time, 'end_date', '-') or getattr(contract_original, 'end_date', '-'),
                #'contract_start': last_amend_time.date if last_amend_time else '-',
                #'contract_end': last_amend_time.end_date if last_amend_time else '-',
                'contract_original': contract_original.amount,
                'project_type': proj.type.name if proj.type else '-',

                # Bank Guarantee persiza sei hare
                'performance_security': contract_original.contract_bank_guarantee.first().performance_security if contract_original and contract_original.contract_bank_guarantee.exists() else 0.00,
                'advance_payment': contract_original.contract_bank_guarantee.first().advance_payment if contract_original and contract_original.contract_bank_guarantee.exists() else 0.00,
                'retention': contract_original.contract_bank_guarantee.first().retention if contract_original and contract_original.contract_bank_guarantee.exists() else 0.00,
                'performance_security_amount': contract_original.contract_bank_guarantee.first().performance_security_amount if contract_original and contract_original.contract_bank_guarantee.exists() else 0.00,
                'amount_advance_payment': contract_original.contract_bank_guarantee.first().amount_advance_payment if contract_original and contract_original.contract_bank_guarantee.exists() else 0.00,
                'retention_amount': contract_original.contract_bank_guarantee.first().retention_amount if contract_original and contract_original.contract_bank_guarantee.exists() else 0.00,
                
                # Amandemen
        

                'amend_cost_no': last_amend_amount.number if last_amend_amount else '-',
                'amend_cost_amount': last_amend_amount.amount if last_amend_amount else 0.00,
                'amend_time_no': last_amend_time.number if last_amend_time else '-',
                'amend_time_date': last_amend_time.date if last_amend_time else '-',
                'total_amend_time_count': total_amend_time_count,
                'total_amend_amount_count': total_amend_amount_count,
                
                'contract_final': contract_final.amendment_amount,
                'owner_estimation': proj.owner_estimation or 0.00,
                'total_project_cost': contract_final, 
                
                # Alokasaun & Transferensia
                'alloc_original': alloc_year.allocation_original if alloc_year else 0.00,
                'transfer_amount': last_transfer.transferencia if last_transfer else 0.00,
                'transfer_count_info': f"Transf. ba-{transfer_count}" if transfer_count > 0 else "Laiha Transferensia",
                'alloc_total': alloc_year.allocation_total if alloc_year else 0.00,
                
                # Pagamento
                'payment_date': last_payment.date if last_payment else '-',
                'payment': last_payment.payment_amount if last_payment else '-',
                'physical_progress': last_payment.physical_progress if last_payment else '-',
                'payment_cumulative': last_payment.comulative_amount if last_payment else 0.00,
                'payment_cumulative_percent': last_payment.comulative_percent if last_payment else 0.00,
                'payment_balance': last_payment.balance_amount if last_payment else 0.00,
                'payment_balance_percent': last_payment.balance_percent if last_payment else 0.00,
                
                # Status & Adisional
                'status': contract_original.status if contract_original.status else "-",
                'justification': justification.description if justification else '-'
            })

    lista_anos = Ano.objects.all().order_by('-ano')

    conteudo = {
        "title": f"Lista Projeto tuir Dono do Projeto {owner.name} Tinan {year_selected}",
        "year_selected": year_selected,
        "lista_anos": lista_anos,  
        "project_list_data": project_list_data,
    }
    
    return render(request, 'report/list.html', conteudo)

