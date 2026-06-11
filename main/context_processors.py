from django.contrib.auth.models import Group
from project.models import Program
from funsionariu.models import Funsionariu



def user_group(request):
    group_name = None
    if request.user.is_authenticated and request.user.groups.exists():
        group_name = request.user.groups.first().name
    return {
        'user_group': group_name
    }


def user_programs_processor(request):
    context = {
        'user_programs': None
    }
    
    if request.user.is_authenticated:
        try:
            funsionariu = Funsionariu.objects.get(user=request.user)
            
            context['user_programs'] = funsionariu.program.all()
            
        except Funsionariu.DoesNotExist:
            if request.user.is_superuser:
                context['user_programs'] = Program.objects.all()
            else:
                context['user_programs'] = Program.objects.none()
                
    return context