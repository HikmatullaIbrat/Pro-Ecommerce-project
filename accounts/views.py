from django.shortcuts import render
from django.contrib.auth import authenticate , login ,get_user_model
from django.shortcuts import render, redirect
from django.http import HttpResponse

# is_safe_url is used to avoid redirecting to those urls which or not hosted with https
from django.utils.http import  is_safe_url
from .models import GuestEmailModel

from .forms import  LoginForm, RegisterationForm, GuestForm
# Create guest logging views here.
def guest_register_view(request):
    guest_form = GuestForm(request.POST or None)

    # next keyword is used on urls to redirect to the specified url which assigned to next
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None

    pass_username_password = {
        'form' : guest_form
    }
    if guest_form.is_valid():
        email = guest_form.cleaned_data.get('email')
        new_guest_email = GuestEmailModel.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id

        #we can use is_safe_url with this method
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect('/register/')  # redirect to home page

    return redirect('/register/')

# Create login page views .
def login_page(request):
    login_form = LoginForm(request.POST or None)
    #print('user is logged in')
    #print(request.user.is_authenticated())
    # next keyword is used on urls to redirect to the specified url which assigned to next
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    pass_username_password = {
        'form' : login_form
    }
    if login_form.is_valid():
        print(login_form.cleaned_data) # displays values of login_form like username and password
        username = login_form.cleaned_data.get('user_name')
        password = login_form.cleaned_data.get('password')

        user = authenticate(request, username = username, password = password)

        print(user)

        if user is not None:
            login(request, user)
            try:
                del request.session['guest_email_id']
            except:
                pass

            return redirect('/')  # redirect to home page

            # we can use is_safe_url with this method
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('/')  # redirect to home page
            
        else:
            print('Error')


    
    return render(request, 'auth/login.html', pass_username_password)


User = get_user_model()

def register_page(request):
    register_form = RegisterationForm(request.POST or None)

    user_data = {
        'form': register_form
    }
    if register_form.is_valid():
        print(register_form.cleaned_data)
        username =  register_form.cleaned_data.get('username')
        email = register_form.cleaned_data.get('email')
        password = register_form.cleaned_data.get('password')

        new_user = User.objects.create_user(username,email,password)
        print(new_user)

    return render(request, 'auth/register.html', user_data)