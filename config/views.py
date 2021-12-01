from django.contrib.auth import authenticate , login ,get_user_model
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from .forms import ContactForm


# View for Login and registration and 

def home_page(request):
    #return HttpResponse('<h1>Hello world!</h1>')
    content = 'Hello Afghanistan'  
    #return HttpResponse(content)  

    # getting the session with the provided name on carts view, 
    # unknown is a default value if user not have been recongnized
    print(request.session.get('first_name','unknown'))
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
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
        if request.is_ajax():
            return JsonResponse({'message':'Thank you'})
    
    # if there is any error in form validation
    if contact_form.errors:
            errors = contact_form.errors.as_json()
            if request.is_ajax():
                return HttpResponse(errors, status=400, content_type='application/json')


    if request.method == 'POST':
        #print(request.POST) # for checking form data which can be displayed or not: it will output on cmd
        #print(request.POST.get('firstname'))
        print(request.POST.get('full_name'))
        print(request.POST.get('email'))
        print(request.POST.get('Message'))



    return render(request, 'contact/contact.html', mydict)


