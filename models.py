from django.db import models

class DemoContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100, default='')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'demo_contact_messages'

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100, default='')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'contact_messages'

class ContactCompliant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    url_name = models.CharField(max_length=100)
    journal_name = models.CharField(max_length=100)
    issue = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'contact_compliant'

class SignUpData(models.Model):
    mail_id = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    confirm_password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'signup_data'

class LoginValidation(models.Model):
    username = models.CharField(max_length=100)
    verify_password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'login_data'

class QueryData(models.Model):
    title = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'query_data'

class UrlData(models.Model):
    url = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'url_data'

    



