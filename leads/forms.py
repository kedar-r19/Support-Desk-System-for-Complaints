from modulefinder import STORE_NAME
from django import forms
from .models import Complaint, Agent, Category
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model
import django_filters

User = get_user_model()

class ComplaintForm(forms.Form):
    store_name=forms.CharField()
    store_contact_no=forms.IntegerField()
    store_id=forms.CharField()

class ComplaintModelForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = (
            'store_name',
            'store_id',
            'store_contact_no',
            'agent',
            'customer',
            'source',
            'description',   
                 
        )



class CustomUserCreationForm(UserCreationForm):
     class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username':UsernameField}
        
        
class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.all())

class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = (
            'category',
        )
    
class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = (
            'name',
        )

class ComplaintFilter(django_filters.FilterSet):
    class Meta:
        model = Complaint
        fields = ['store_name', 'agent', 'category', 'customer', 'source']
