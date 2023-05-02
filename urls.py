from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('demohome', views.demohome, name='demohome'),
    path('demoabout', views.demoabout, name='demoabout'),
    path('democontact', views.democontact, name='democontact'),       
    path('signup', views.signup, name='signup'),  
    path('home', views.home, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('faq', views.FAQ, name='FAQ'), 
    path('general_journal_list', views.general_journal_list, name='general_journal_list'), 
    path('basic_journal_list', views.basic_journal_list, name='basic_journal_list'), 
    path('life_journal_list', views.life_journal_list, name='life_journal_list'),
    path('engineering_journal_list', views.engineering_journal_list, name='engineering_journal_list'), 
    path('mathematics_journal_list', views.mathematics_journal_list, name='mathematics_journal_list'), 
    path('medicine_journal_list', views.medicine_journal_list, name='medicine_journal_list'), 
    path('other_journal_list', views.other_journal_list, name='other_journal_list'),
    path('testing', views.testing, name='testing'),
]
