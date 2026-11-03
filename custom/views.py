from django.shortcuts import render, redirect, get_object_or_404
from main.decorators import  allow_user
from django.contrib.auth.decorators import login_required
from project.models import *
from custom.forms import *
from django.contrib import messages


@login_required
@allow_user(allow_roles=['admin', 'focal_point', 'finance', 'diretor'])
def CustomLists(request, slug):
    group = request.user.groups.all()[0].name
    data = None
    title = ''
    topic =  ""
    template = 'custom/list.html'
    form = None
    program = None
    
    if slug == 'program':
        data = Program.objects.all()
        title = 'Lista Programa'
        topic = 'Programa'
        template = 'custom/list.html'
        if request.method == 'POST':
            if request.POST.get('id'):
                obj = get_object_or_404(Program,id=request.POST.get('id'))
                form = ProgramForm(request.POST,instance=obj)

                if form.is_valid():
                    form.save()
                    messages.success(request, 'Susesu Altera')
                    return redirect('custom-list', slug='program')
            else:
                form = ProgramForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Susesu Aumenta')
                    return redirect('custom-list',slug='program')
        else:
            form = ProgramForm()
    elif slug == 'subprogram':
        data = SubProgram.objects.all()
        program = Program.objects.all()
        title = 'Lista Sub Programa'
        topic = 'Sub Programa'
        template = 'custom/list3.html'
        if request.method == 'POST':
            if request.POST.get('id'):
                obj = get_object_or_404(SubProgram,id=request.POST.get('id'))
                form = SubProgramForm(request.POST,instance=obj)

                if form.is_valid():
                    form.save()
                    messages.success(request, 'Susesu Altera')
                    return redirect('custom-list', slug='subprogram')
            else:
                form = SubProgramForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Susesu Aumenta')
                    return redirect('custom-list',slug='subprogram')
        else:
            form = SubProgramForm()
    elif slug == 'owner':
        data = Owner.objects.all()
        title = 'Lista Dono do Projeto'
        topic = 'Dono do Projeto'
        template = 'custom/list.html'
        if request.method == 'POST':
            if request.POST.get('id'):
                obj = get_object_or_404(Owner,id=request.POST.get('id'))
                form = OwnerForm(request.POST,instance=obj)

                if form.is_valid():
                    form.save()
                    messages.success(request, 'Susesu Altera')
                    return redirect('custom-list', slug='owner')
            else:
                form = OwnerForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Susesu Aumenta')
                    return redirect('custom-list',slug='owner')
        else:
            form = OwnerForm()
    elif slug == 'fund':
        data = Fund.objects.all()
        title = 'Lista Fundus'
        topic = 'Fundus'
        template = 'custom/list.html'
        if request.method == 'POST':
            if request.POST.get('id'):
                obj = get_object_or_404(Fund,id=request.POST.get('id'))
                form = FundForm(request.POST,instance=obj)

                if form.is_valid():
                    form.save()
                    messages.success(request, 'Susesu Altera')
                    return redirect('custom-list', slug='fund')
            else:
                form = FundForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Susesu Aumenta')
                    return redirect('custom-list',slug='fund')
        else:
            form = FundForm()
    elif slug == 'type':
        data = Type.objects.all()
        title = 'Lista Tipo'
        topic = 'Tipo'
        template = 'custom/list2.html'
        if request.method == 'POST':
            if request.POST.get('id'):
                obj = get_object_or_404(Type,id=request.POST.get('id'))
                form = TypeForm(request.POST,instance=obj)

                if form.is_valid():
                    form.save()
                    messages.success(request, 'Susesu Altera')
                    return redirect('custom-list', slug='type')
            else:
                form = TypeForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Susesu Aumenta')
                    return redirect('custom-list',slug='type')
        else:
            form = TypeForm()
        
    conteudo = {
        "title" : title,
        'topic': topic,
        'data' : data,
        'program':program,
        'group':group, 'form': form
    }
    return render(request, template, conteudo)