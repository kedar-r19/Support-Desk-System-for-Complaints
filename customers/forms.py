from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from leads.models import Complaint, Customer


User = get_user_model()

class CustomerModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
        )

class CustomerComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = (
            'store_name',
            'store_id',
            'store_contact_no',
            'description',  
        )