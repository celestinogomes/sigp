from django.shortcuts import redirect, render



def allow_user(allow_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.all()[0].name:
                group = request.user.groups.all()[0].name
            if group in allow_roles:
                return view_func(request, *args, **kwargs)
            else:
                return render(request, 'layout/403.html')
        return wrapper_func
    return decorator