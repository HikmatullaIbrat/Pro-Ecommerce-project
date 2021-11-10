from django.contrib.auth import authenticate , login ,get_user_model
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import ContactForm, LoginForm, RegisterationForm


# View for Login and registration and 

def home_page(request):
    #return HttpResponse('<h1>Hello world!</h1>')
    content = 'Hello Afghanistan'  
    #return HttpResponse(content)  
    mydict = {
        'firstName':'Hikmat',
        'content': 'Welcome to the home page'
    }  # passing this dict to render method
    if request.user.is_authenticated:
        mydict['premium_content'] = 'You\'re using a Premium account'  # give special content for premiun users
    return render(request,'index.html',mydict)
    
def about_page(request):
    mydict = {
        'firstName':'Seerat',
        'content': 'welcome to the about page'
        }
    return render(request, 'index.html', mydict)

def product_page(request):
    mydict = {
        'firstName': 'Eisa',
        'content': 'Product Page',
        'product_name': 'Mobile Phones'
    }
    return render(request, 'index.html',mydict)


def contact_page(request):

    contact_form = ContactForm(request.POST or None) # pass the form's data whether it is sent with post or don't send it
    mydict = {     # mydict is just for test of sending the data
        'first_name': 'Raees',
        'content': 'You can contact with us with filling below form',
        'form' : contact_form # we passed to dict that can be usable in view.html
    }

    

    if request.method == 'POST':
        #print(request.POST) # for checking form data which can be displayed or not: it will output on cmd
        #print(request.POST.get('firstname'))
        print(request.POST.get('full_name'))
        print(request.POST.get('email'))
        print(request.POST.get('Message'))



    return render(request, 'contact/contact.html', mydict)


def login_page(request):
    login_form = LoginForm(request.POST or None)
    print('user is logged in')
    #print(request.user.is_authenticated())
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