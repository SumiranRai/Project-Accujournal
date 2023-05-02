from django import forms
from django.forms import TextInput, EmailInput

class DemoContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'form-control border-0 bg-light px-4', 'style': 'height: 55px;'}), max_length=100, label="", required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Your Email', 'class': 'form-control border-0 bg-light px-4', 'style': 'height: 55px;'}), max_length=100, label="", required=False)
    subject = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Subject', 'class': 'form-control border-0 bg-light px-4', 'style': 'height: 55px;'}), max_length=100, label="", required=False)
    message = forms.CharField(label="", required=False, widget=forms.Textarea(attrs={'placeholder': 'Message', 'class': 'form-control border-0 bg-light px-4 py-3', 'rows': '4'}))

class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'form-control border-0 bg-light px-4', 'style': 'height: 55px;'}), max_length=100, label="", required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Your Email', 'class': 'form-control border-0 bg-light px-4', 'style': 'height: 55px;'}), max_length=100, label="", required=False)
    subject = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Subject', 'class': 'form-control border-0 bg-light px-4', 'style': 'height: 55px;'}), max_length=100, label="", required=False)
    message = forms.CharField(label="", required=False, widget=forms.Textarea(attrs={'placeholder': 'Message', 'class': 'form-control border-0 bg-light px-4 py-3', 'rows': '4'}))

class CompliantForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'form-control border-0 bg-light px-4', 'style': 'height: 55px;'}), max_length=100, label="", required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Your Email', 'class': 'form-control border-0 bg-light px-4', 'style': 'height: 55px;'}), max_length=100, label="", required=False)
    url_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Website name/link (if available)', 'class': 'form-control border-0 bg-light px-4', 'style': 'height: 55px;'}), max_length=100, label="", required=False)
    journal_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Journal name', 'class': 'form-control border-0 bg-light px-4', 'style': 'height: 55px;'}), max_length=100, label="", required=False)
    issue = forms.CharField(label="", required=False, widget=forms.Textarea(attrs={'placeholder': 'What is the issue? Is it a fake journal?', 'class': 'form-control border-0 bg-light px-4 py-3', 'rows': '1'}))

class SignUpForm(forms.Form):
    mail_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Mail ID', 'input class': 'input', 'style': 'height: 55px;'}), max_length=100, label="", required=False)
    password = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your password', 'input class': 'input', 'type': 'password', 'style': 'height: 55px;'}), max_length=100, label="", required=False)
    confirm_password = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Retype to confirm password', 'input class': 'input', 'type': 'password', 'style': 'height: 55px;'}), max_length=100, label="", required=False)

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Username / Mail ID', 'input class': 'input', 'style': 'height: 55px;'}), max_length=100, label="", required=False)
    verify_password = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your password', 'input class': 'input', 'type': 'password', 'style': 'height: 55px;'}), max_length=100, label="", required=False)

class QueryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title/ISSN', 'class': 'searchText'}), max_length=100, label="", required=False)
    publisher = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Publisher Name', 'class': 'searchText'}), max_length=100, label="", required=False)
    index = forms.ChoiceField(choices=[
        ('Authenticated Journals', 'Authenticated Journals'),
        ('Cloned / Fake Journals', 'Cloned / Fake Journals')
    ], initial='Indexes', widget=forms.Select(attrs={'class': 'form-select', 'aria-label': 'Default select example', 'id': 'chooseCategory'}))

class UrlForm(forms.Form):
    url = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Website Link', 'class': 'searchText'}), max_length=100, label="", required=False)

   
