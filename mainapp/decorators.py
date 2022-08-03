from django.shortcuts import redirect

def redirect_authenticated_user(func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return func(request,*args,**kwargs)
    return wrapper