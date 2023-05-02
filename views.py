from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import DemoContactForm ,SignUpForm, LoginForm, QueryForm, UrlForm, ContactForm, CompliantForm
from .models import DemoContactMessage ,SignUpData, LoginValidation, QueryData, UrlData, ContactMessage, ContactCompliant
from pretty_html_table import build_table
from googlesearch import search

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import pandas as pd
import pymongo

def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())

def demohome(request):
    template = loader.get_template('demoindex.html')
    return HttpResponse(template.render())

def demoabout(request):
    template = loader.get_template('demoabout.html')
    return HttpResponse(template.render())

def democontact(request):
    if request.method == 'POST':
        form = DemoContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            contact_message = DemoContactMessage(name=name, email=email, subject=subject, message=message)
            contact_message.save()
            return render(request, 'demosuccess.html')
    else:
        form = DemoContactForm()
    return render(request, 'democontact.html', {'form': form}) 

def contact(request):
    form = ContactForm()  
    form1 = CompliantForm() 
    if request.method == 'POST':
        if 'submit' in request.POST and request.POST['submit'] == 'feedback':
            form = ContactForm(request.POST)
            if form.is_valid():   
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']
                contact_message = ContactMessage(name=name, email=email, subject=subject, message=message)
                contact_message.save()
                return render(request, 'success.html')
            else:
                form1 = CompliantForm()        
        elif 'submit' in request.POST and request.POST['submit'] == 'compliant':
            form1 = CompliantForm(request.POST)
            if form1.is_valid():
                name = form1.cleaned_data['name']
                email = form1.cleaned_data['email']
                url_name = form1.cleaned_data['url_name']
                journal_name = form1.cleaned_data['journal_name']
                issue = form1.cleaned_data['issue']
                contact_compliant = ContactCompliant(name=name, email=email, url_name=url_name, journal_name=journal_name, issue=issue)
                contact_compliant.save()
                return render(request, 'success.html')       
            else:
                form = ContactForm()      
    else:
        form = ContactForm()
        form1 = CompliantForm()
    return render(request, 'contact.html', {'form': form, 'form1': form1})  
         
def create_html_tables(title=None, publisher=None, index=None):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Accujournal"]
    if index == 'Authenticated Journals':
        mycol = mydb["journals"]
        query = {}
        if title:
            query["$or"] = [
                {"Journal title": {"$regex": title, "$options": "i"}},
                {"ISSN": {"$regex": title, "$options": "i"}},
            ]
        if publisher:
            query["Publisher name"] = {"$regex": publisher, "$options": "i"}
    
    elif index == 'Cloned / Fake Journals':
        mycol = mydb["cloned/fake_journals"]
        query = {}
        if title:
            query["$or"] = [
                {"title": {"$regex": title, "$options": "i"}},
                {"issn": {"$regex": title, "$options": "i"}},
            ]
        if publisher:
            query["publisher"] = {"$regex": publisher, "$options": "i"}

    mydoc = mycol.find(query, {"_id": 0})
    df = pd.DataFrame(mydoc)
    
    if not mydoc:
        return None
    
    html_table_blue_light = build_table(df, 'blue_light')
    with open('query_results.html', 'w', encoding='utf-8-sig') as f:
        f.write(html_table_blue_light)

def home(request):
    form = QueryForm()  
    form1 = UrlForm()        
    if request.method == 'POST':
        if 'submit' in request.POST and request.POST['submit'] == 'query':
            form = QueryForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                publisher = form.cleaned_data['publisher']
                index = form.cleaned_data['index']
                if not title and not publisher:
                    # Return the query_results.html template with no results
                    return render(request, 'query_results.html', {'results': None})
                final_title = str.upper(title)
                final_publisher = str.upper(publisher)
                create_html_tables(final_title, final_publisher, index)           
                with open('query_results.html', 'r', encoding='utf-8-sig') as f:
                    results = f.read()                                    
                query_data = QueryData(title=title, publisher=publisher)
                query_data.save()
                return render(request, 'query_results.html', {'results': results})       
            else:
                form1 = UrlForm()
        elif 'submit' in request.POST and request.POST['submit'] == 'url':
            form1 = UrlForm(request.POST)
            if form1.is_valid():
                url = form1.cleaned_data['url']
                results = list(search(url, num_results=10))
                context = {
                    'query': url,
                    'results': results,
                }
                url_data = UrlData(url=url)
                url_data.save()
                return render(request, 'url_results.html', context)
            else:
                form = QueryForm()
    else:
        form = QueryForm()
        form1 = UrlForm()
    return render(request, 'index.html', {'form': form, 'form1': form1})
    
def about(request):
    template = loader.get_template('about.html')
    return HttpResponse(template.render())

def FAQ(request):
    template = loader.get_template('FAQ.html')
    return HttpResponse(template.render())

def create_journals(category):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Sorted_journals"]
    mycol = mydb[category]
    query = {}
    mydoc = mycol.find(query, {"_id": 0})
    df = pd.DataFrame(mydoc)

    html_table_blue_light = build_table(df, 'blue_light')
    with open('journal.html', 'w', encoding='utf-8-sig') as f:
        f.write(html_table_blue_light)

def general_journal_list(request):
    create_journals("General")
    with open('journal.html', 'r', encoding='utf-8-sig') as f:
        results = f.read()                                    
    return render(request, 'journal.html', {'results': results}) 

def basic_journal_list(request):
    create_journals("Basic")
    with open('journal.html', 'r', encoding='utf-8-sig') as f:
        results = f.read()                                    
    return render(request, 'journal.html', {'results': results}) 
 
def life_journal_list(request):
    create_journals("Life_Sciences")
    with open('journal.html', 'r', encoding='utf-8-sig') as f:
        results = f.read()                                    
    return render(request, 'journal.html', {'results': results}) 

def engineering_journal_list(request):
    create_journals("Engineering")
    with open('journal.html', 'r', encoding='utf-8-sig') as f:
        results = f.read()                                    
    return render(request, 'journal.html', {'results': results}) 

def mathematics_journal_list(request):
    create_journals("Mathematics")
    with open('journal.html', 'r', encoding='utf-8-sig') as f:
        results = f.read()                                    
    return render(request, 'journal.html', {'results': results}) 

def medicine_journal_list(request):
    create_journals("Medicine")
    with open('journal.html', 'r', encoding='utf-8-sig') as f:
        results = f.read()                                    
    return render(request, 'journal.html', {'results': results}) 

def other_journal_list(request):
    create_journals("Unclassified")
    with open('journal.html', 'r', encoding='utf-8-sig') as f:
        results = f.read()                                    
    return render(request, 'journal.html', {'results': results})      

def signup(request):
    form = SignUpForm()
    form1 = LoginForm()
    if request.method == 'POST':
        if 'submit' in request.POST and request.POST['submit'] == 'SignUp':
            form = SignUpForm(request.POST)
            if form.is_valid():
                mail_id = form.cleaned_data['mail_id']
                password = form.cleaned_data['password']
                confirm_password = form.cleaned_data['confirm_password']
                if password == confirm_password:
                    ph = PasswordHasher()
                    hashed_password = ph.hash(password)
                    signup_data = SignUpData(mail_id=mail_id, password=hashed_password, confirm_password=confirm_password)
                    signup_data.save()
                    return redirect('home')
                else:
                    form1 = LoginForm()
        elif 'submit' in request.POST and request.POST['submit'] == 'Login':
            form1 = LoginForm(request.POST)
            if form1.is_valid():
                username = form1.cleaned_data['username']
                verify_password = form1.cleaned_data['verify_password']
                try:
                    user = SignUpData.objects.get(mail_id=username)
                    ph = PasswordHasher()
                    ph.verify(user.password, verify_password)
                    login_data = LoginValidation(username=username, verify_password=verify_password)
                    login_data.save()
                    return redirect('home')
                except (SignUpData.DoesNotExist, VerifyMismatchError):
                    form1.add_error(None, 'Invalid username or password')
            else:
                form = SignUpForm()
    else:
        form = SignUpForm()
        form1 = LoginForm()
    return render(request, 'signup.html', {'form': form, 'form1': form1})

# def signup(request):
#     if request.method == 'POST':
#         if 'submit' in request.POST and request.POST['submit'] == 'SignUp':
#             form = SignUpForm(request.POST)
#             if form.is_valid():
#                 mail_id = form.cleaned_data['mail_id']
#                 password = form.cleaned_data['password']
#                 confirm_password = form.cleaned_data['confirm_password']
#                 password_in_bytes = bytes(password, 'utf-8')
#                 hashed_password = argon2.hash_password(password_in_bytes)
#                 signup_data = SignUpData(mail_id=mail_id, password=hashed_password, confirm_password=confirm_password)
#                 signup_data.save()
#                 return redirect('/home')
#             else:
#                 form1 = LoginForm()
#         elif 'submit' in request.POST and request.POST['submit'] == 'Login':
#             form1 = LoginForm(request.POST)
#             if form1.is_valid():
#                 username = form1.cleaned_data['username']
#                 verify_password = form1.cleaned_data['verify_password']
#                 login_data = LoginValidation(username=username, verify_password=verify_password)
#                 login_data.save()
#                 return redirect('/home')
#             else:
#                 form = SignUpForm()
#     else:
#         form = SignUpForm()
#         form1 = LoginForm()
#     return render(request, 'signup.html', {'form1': form1, 'form': form})

def testing(request):
    template = loader.get_template('template.html')
    context = {
        'fruits': ['Apple', 'Banana', 'Cherry'],  
        }
    return HttpResponse(template.render(context, request))

# def query(request):
#   template = loader.get_template('query.html')
#   if request.method == 'get':
#       myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#       mydb = myclient["journals"]
#       mycol = mydb["wosdata"]
#       form = SearchForm(request.get)
#       if form.is_valid():
#         query_by_title = form.cleaned_data['query_by_title']
#         query_by_publisher = form.cleaned_data['query_by_publisher']
#         finalquery = str.upper(query_by_publisher)
#         myquery = { "Publisher name" : finalquery }
#         mydoc = mycol.find(myquery).sort("Journal title", 1)
#         df = pd.DataFrame(mydoc)
#         html_table_blue_light = build_table(df, 'blue_light')
#         with open('results.html', 'w') as f:
#           f.write(html_table_blue_light)
#         return render(request, 'results.html')
#   else:
#     form = SearchForm()
#   return render(request, 'query.html')

# def search(request):
#     if request.method == 'POST':
#         query = request.POST.get('query')
#         client = MongoClient('mongodb://localhost:27017/')
#         db = client['mydatabase']
#         collection = db['search_data']
#         results = collection.find({'$text': {'$search': query}})
#         return render(request, 'search_results.html', {'results': results})
#     return render(request, 'search.html')

# def signup(request):
#    user = "not logged in"
   
#    if request.method == "POST":
#       #Get the posted form
#       MyLoginForm = SignupForm(request.POST)
      
#       if MyLoginForm.is_valid():
#          username = SignupForm.cleaned_data['user']
#    else:
#       MyLoginForm = SignupForm()		
#    return render(request, 'loggedin.html', {"username" : user})

# def contact_view(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             return render(request, 'success.html', {'form': form})
#             pass
#     else:
#         form = ContactForm()
#     return render(request, 'contact.html', {'form': form})

# from django.core.mail import send_mail
# def contact(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             email = form.cleaned_data['email']
#             subject = form.cleaned_data['subject']
#             message = form.cleaned_data['message']
#             # Save the form data to MongoDB using the ContactMessage model
#             contact_message = ContactMessage(name=name, email=email, subject=subject, message=message)
#             contact_message.save()
#             # Send email using Django's built-in email functionality
#             # send_mail(
#             #     'Contact Form Submission',
#             #     f'Name: {name}\nEmail: {email}\nMessage: {message}',
#             #     'your_email@example.com',
#             #     ['recipient_email@example.com'],
#             #     fail_silently=False,
#             # )
#             return render(request, 'success.html')
#     else:
#         form = ContactForm()
#     return render(request, 'contact.html', {'form': form})


# flag = 0
            # while True:
            #     if (len(password)<=8):
            #         flag = -1
            #         break
            #     elif not re.search("[a-z]", password):
            #         flag = -1
            #         break
            #     elif not re.search("[A-Z]", password):
            #         flag = -1
            #         break
            #     elif not re.search("[0-9]", password):
            #         flag = -1
            #         break
            #     elif not re.search("[_@$]" , password):
            #         flag = -1
            #         break
            #     elif re.search("\s" , password):
            #         flag = -1
            #         break
            #     else:
            #         flag = 0
            #         print("Minimum length 8, include numbers, special characters, uppercase letter!")
            #         break
            # if flag == -1:\
            #     print("Minimum length 8, include numbers, special characters, uppercase letter!")

# def index(request):
#     template = loader.get_template('index.html')
#     return HttpResponse(template.render())

# def contact(request):
#     template = loader.get_template('contact.html')
#     if request.method == 'post':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             email = form.cleaned_data['email']
#             subject = form.cleaned_data['subject']
#             message = form.cleaned_data['message']
#             # Save the form data to MongoDB using the ContactMessage model
#             contact_message = ContactMessage(name=name, email=email, subject=subject, message=message)
#             contact_message.save()
#             # Send email using Django's built-in email functionality
#             # send_mail(
#             #     'Contact Form Submission',
#             #     f'Name: {name}\nEmail: {email}\nMessage: {message}',
#             #     'your_email@example.com',
#             #     ['recipient_email@example.com'],
#             #     fail_silently=False,
#             # )
#             return render(request, 'homecontact_success.html')
#     else:
#         form = ContactForm()
#     return render(request, 'contact.html', {'form': form})
