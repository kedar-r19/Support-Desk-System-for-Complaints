from asyncio.windows_events import NULL
from django.forms import NullBooleanField
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin 
from leads.models import Customer,  Complaint
from .forms import CustomerModelForm, CustomerComplaintForm
from agents.mixins import OwnerAndLoginRequiredMixin, OwnerCustomerAndLoginRequiredMixin
from django.core.mail import send_mail
import random
from django.shortcuts import redirect, get_object_or_404


class CustomerLandingPage(LoginRequiredMixin, generic.TemplateView):
    template_name = "customer_landing_page.html"

class CustomerListView(OwnerAndLoginRequiredMixin, generic.ListView):
    template_name = "customer_list.html"
    queryset = Customer.objects.all()

class CustomerCreateView(OwnerAndLoginRequiredMixin, generic.CreateView):
    template_name = "customer_create.html"
    form_class = CustomerModelForm

    def get_success_url(self):
        return "/customers"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_customer = True
        user.is_agent = False
        user.is_owner = False
        user.set_password(f"{random.randint(0, 10000)}")
        user.save()
        Customer.objects.create(
            user = user
        )
        send_mail(
            subject = "Your account has been created.",
            message = f"To add complaints or view previous complaints, login to the system. Your username is {user.username}",
            from_email = "kedarraul19@yahoo.com",
            recipient_list=[user.email]
        )
        return super(CustomerCreateView, self).form_valid(form)
                   

class CustomerDetailView(OwnerAndLoginRequiredMixin, generic.DetailView):
    template_name = "customer_detail.html"
    queryset = Customer.objects.all()
    context_object_name = "customer"

class CustomerUpdateView(OwnerAndLoginRequiredMixin, generic.UpdateView):
    template_name = "customer_update.html"
    form_class = CustomerModelForm
   
    #Queryset - single instance i.e. the customer
    def get_object(self, queryset=None):
        customer_pk = self.kwargs.get('pk', None)
        return get_object_or_404(Customer, pk=customer_pk)

    #display details in form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.get_object()  # -> returns a customer object
        data = {
               'username': customer.user.username,
               'first_name': customer.user.first_name,
               'last_name': customer.user.last_name,
               'email': customer.user.email,
        }
        form = self.form_class(initial=data, instance=customer.user)
        context['form'] = form  # -> updating the class view context dictionary
        return context

    # Use the post method to handle the form submission
    def post(self, request, *arg, **kwargs):
        # setting the user instance on the form
        customer = self.get_object()
        form = self.form_class(request.POST, instance=customer.user)  
        if form.is_valid():
            form.save()
            return redirect('/customers') 
        

        # Passing back the form to the template
        return render(request, self.template_name, {'form': form})
     
    
 
class CustomerDeleteView(OwnerAndLoginRequiredMixin, generic.DeleteView):
    template_name = "customer_delete.html"
    queryset = Customer.objects.all()
    context_object_name = "customer"

    def get_success_url(self):
        return "/customers"



class CustomerComplaintCreateView(OwnerCustomerAndLoginRequiredMixin, generic.CreateView):
    template_name = "customercomplaint_create.html"
    form_class = CustomerComplaintForm
    
    def get_success_url(self):
        return "/complaints"

    def form_valid(self, form):
        complaint = form.save(commit=False)
        customer = get_object_or_404(Customer, user=self.request.user) 
        
        if customer:
            complaint.customer = customer  

        complaint.source = 'ticket'
        complaint.save()
        return super(CustomerComplaintCreateView, self).form_valid(form)

class CustomerComplaintUpdateView(OwnerCustomerAndLoginRequiredMixin, generic.UpdateView):
    template_name = "customercomplaint_update.html"
    form_class = CustomerComplaintForm
    
    def get_queryset(self):
        queryset = Complaint.objects.all()
        if self.request.user.is_owner:
            queryset=Complaint.objects.filter(agent__isnull=False)
        elif self.request.user.is_agent:
            queryset=Complaint.objects.filter(agent__isnull=False)
            queryset = queryset.filter(agent__user=self.request.user)
        else:
            queryset=Complaint.objects.filter(agent__isnull=False)
            queryset = queryset.filter(customer__user=self.request.user)
        return queryset

    def get_success_url(self):
        return "/complaints"


