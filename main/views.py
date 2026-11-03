import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from payment.models import Payment
from project.models import Program, Project, ProjectJustification
from custom.models import Ano

@login_required
def dashboard(request):
    today = timezone.now().date()
    
    start_of_week = today - datetime.timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)

    query_today = Payment.objects.filter(date=today)
    payment_today = query_today.aggregate(total=Sum('payment_amount'))['total'] or 0.00
    project_count_today = query_today.values('project').distinct().count() 
        
    query_week = Payment.objects.filter(date__gte=start_of_week, date__lte=today)
    payment_week = query_week.aggregate(total=Sum('payment_amount'))['total'] or 0.00
    project_count_week = query_week.values('project').distinct().count()
        
    query_month = Payment.objects.filter(date__gte=start_of_month, date__lte=today)
    payment_month = query_month.aggregate(total=Sum('payment_amount'))['total'] or 0.00
    project_count_month = query_month.values('project').distinct().count()

    context = {
        'title': 'DASHBOARD | SIGP (FI)',
        'payments': {
            'today': payment_today,
            'week': payment_week,
            'month': payment_month,
        },
        'projects': {
            'today': project_count_today,
            'week': project_count_week,
            'month': project_count_month,
        }
    }
    return render(request, 'dashboard.html', context)



@login_required
def RDashboardListAll(request, slug):
    today = timezone.now().date()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)

    if slug == 'today':
        start_date = today
        title = "Loron Ida Ne"
    elif slug == 'week':
        start_date = start_of_week
        title = "Semana Ida Ne"
    elif slug == 'month':
        start_date = start_of_month
        title = "Fulan Ida Ne"
    else:
        start_date = today

    payments = Payment.objects.filter(
        date__gte=start_date,
        date__lte=today
    ).select_related(
        'project', 
        'project__program', 
        'project__sub_program', 
        'project__owner', 
        'project__fund', 
        'project__type',
        'project__project_location',
        'project__project_location__municipality', 
        'project__project_location__administrative_post', 
        'project__project_location__village'
    ).order_by('-date', '-id')

    project_list_data = []

    for index, pay in enumerate(payments, start=1):
        proj = pay.project  

        last_amend_amount = proj.amendment_amount_project.all().order_by('-id').first()
        total_amend_amount_count = proj.amendment_amount_project.count()

        last_amend_time = proj.amendment_time_project.all().order_by('-id').first()
        total_amend_time_count = proj.amendment_time_project.count()
        
        current_year = today.year
        alloc_year = proj.project_allocation.filter(year__ano=current_year).first()

        last_transfer = proj.transferencia_project.all().order_by('-id').first()
        transfer_count = proj.transferencia_project.count()

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
            'contract_original': contract_original.amount if contract_original else 0.00,
            'project_type': proj.type.name if proj.type else '-',
            
            # Amandemen
            'amend_cost_no': last_amend_amount.number if last_amend_amount else '-',
            'amend_cost_amount': last_amend_amount.amount if last_amend_amount else 0.00,
            'amend_time_no': last_amend_time.number if last_amend_time else '-',
            'amend_time_date': last_amend_time.date if last_amend_time else '-',
            'total_amend_time_count': total_amend_time_count,
            'total_amend_amount_count': total_amend_amount_count,
            
            'contract_final': contract_final.amendment_amount if contract_final else 0.00,
            'owner_estimation': proj.owner_estimation or 0.00,
            'total_project_cost': contract_final.amendment_amount if contract_final else 0.00, 
            
            # Alokasaun & Transferensia
            'alloc_original': alloc_year.allocation_original if alloc_year else 0.00,
            'transfer_amount': last_transfer.transferencia if last_transfer else 0.00,
            'transfer_count_info': f"Transf. ba-{transfer_count}" if transfer_count > 0 else "Laiha Transferensia",
            'alloc_total': alloc_year.allocation_total if alloc_year else 0.00,
            
             # Pagamento
            'payment_date': pay.date if pay.date else '-',
            'payment': pay.payment_amount if pay.payment_amount else '-',
            'physical_progress': pay.physical_progress if pay.physical_progress else '-',
            'payment_cumulative': pay.comulative_amount if pay.comulative_amount else 0.00,
            'payment_cumulative_percent': pay.comulative_percent if pay.comulative_percent else 0.00,
            'payment_balance': pay.balance_amount if pay.balance_amount else 0.00,
            'payment_balance_percent': pay.balance_percent if pay.balance_percent else 0.00,
            
            # Status & Adisional
            'status': contract_original.status if contract_original and contract_original.status else "-",
            'justification': justification.description if justification else '-'
        })

    lista_anos = Ano.objects.all().order_by('-ano')

    conteudo = {
        "title": f"Lista Pagamento {title}",
        "lista_anos": lista_anos,  
        "project_list_data": project_list_data,
    }
    
    return render(request, 'report/list2.html', conteudo)