from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView, DetailView, FormView
from .models import Category, Complaint, Agent
from .forms import CategoryModelForm, CategoryUpdateForm, ComplaintForm, ComplaintModelForm, CustomUserCreationForm, AssignAgentForm, ComplaintFilter
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OwnerAndLoginRequiredMixin, OwnerCustomerAndLoginRequiredMixin, OwnerAgentAndLoginRequiredMixin
from django.urls import reverse
from django.contrib.auth import views as views_auth
from django.contrib.auth.forms import AuthenticationForm


#from django.core.mail import send_mail

#CRUD - Create, Retrieve, Update and Delete

#Class based views:

class LoginView(views_auth.LoginView):
    form_class=AuthenticationForm
    redirect_authenticated_user=True

    def get_success_url(self):
        # write your logic here
        if self.request.user.is_owner or self.request.user.is_agent:
            return '/complaints'
        elif self.request.user.is_customer:
            return '/customer_landing_page'
        return '/'

class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm
    
    def get_success_url(self):
        return "/login"

class LandingPageView(TemplateView):
    template_name = "landing_page.html"

class ComplaintListView(LoginRequiredMixin, ListView):
    template_name = "complaint_list.html"
    context_object_name =  "complaints"

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
        

    def get_context_data(self, **kwargs):
        context = super(ComplaintListView, self).get_context_data(**kwargs)
        if self.request.user.is_owner:
            queryset = Complaint.objects.filter(agent__isnull=True)
            context.update({
                "unassigned_complaints": queryset
            })
        elif self.request.user.is_customer:
            queryset = Complaint.objects.filter(agent__isnull=True)
            queryset = queryset.filter(customer__user=self.request.user)
            context.update({
                "unassigned_complaints": queryset
            })
        return context

class ComplaintDetailView(LoginRequiredMixin, DetailView):
    template_name = "complaint_detail.html"
    context_object_name =  "complaint"

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
        

class ComplaintCreateView(OwnerAndLoginRequiredMixin, CreateView):
    template_name = "complaint_create.html"
    form_class = ComplaintModelForm
    
    def get_success_url(self):
        return "/complaints"
    
   

class ComplaintUpdateView(OwnerCustomerAndLoginRequiredMixin, UpdateView):
    template_name = "complaint_update.html"
    form_class = ComplaintModelForm
    
    def get_queryset(self):
            queryset = Complaint.objects.all()
            if self.request.user.is_owner:
                queryset=Complaint.objects.filter(agent__isnull=False)
            else:
                queryset=Complaint.objects.filter(agent__isnull=False)
                queryset = queryset.filter(customer__user=self.request.user)
            return queryset

    def get_success_url(self):
        return "/complaints"

class ComplaintDeleteView(OwnerCustomerAndLoginRequiredMixin, DeleteView):
    template_name = "complaint_delete.html"
    
    def get_queryset(self):
            queryset = Complaint.objects.all()
            if self.request.user.is_owner:
                queryset=Complaint.objects.filter(agent__isnull=False)
            else:
                queryset=Complaint.objects.filter(agent__isnull=False)
                queryset = queryset.filter(customer__user=self.request.user)
            return queryset

    def get_success_url(self):
        return "/complaints"

class AssignAgentView(OwnerAndLoginRequiredMixin, FormView):
    template_name = "assign_agent.html"
    form_class = AssignAgentForm

    def get_success_url(self):
        return "/complaints"

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        complaint = Complaint.objects.get(id=self.kwargs["pk"])
        complaint.agent=agent
        complaint.save()
        return super(AssignAgentView, self).form_valid(form)
        
class CategoryListView(LoginRequiredMixin, ListView):
    template_name = "category_list.html"
    context_object_name = "category_list"
    queryset = Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context.update({
            "unassigned_complaint_count": Complaint.objects.filter(category__isnull=True).count(),
            #"unresolved_complaint_count": Complaint.objects.filter(category='Resolved').count()
        })
        return context

class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = "category_detail.html"  
    queryset = Category.objects.all()     
    context_object_name = "category"

    

class CategoryUpdateView(OwnerAgentAndLoginRequiredMixin, UpdateView):
    template_name = "category_update.html"
    form_class = CategoryUpdateForm
   
    def get_queryset(self):
        queryset = Complaint.objects.all()
        if self.request.user.is_owner:
            queryset=Complaint.objects.filter(agent__isnull=False)
        elif self.request.user.is_agent:
            queryset=Complaint.objects.filter(agent__isnull=False)
            queryset = queryset.filter(agent__user=self.request.user)
        return queryset
        

    def get_success_url(self):
        return reverse("leads:complaint-detail", kwargs={"pk": self.get_object().id})


class CategoryCreateView(OwnerAndLoginRequiredMixin, CreateView):
    template_name = "category_create.html"
    form_class = CategoryModelForm
    
    def get_success_url(self):
        return "/complaints/categories"

class CategoryEditView(OwnerAndLoginRequiredMixin, UpdateView):
    template_name = "category_edit.html"
    form_class = CategoryModelForm
    queryset = Category.objects.all()
    context_object_name = "category"

    def get_success_url(self):
        return "/complaints/categories"

class CategoryDeleteView(OwnerAndLoginRequiredMixin, DeleteView):
    template_name = "category_delete.html"
    queryset = Category.objects.all()

    def get_success_url(self):
        return "/complaints/categories"

def complaints_filter(request):
    f = ComplaintFilter(request.GET, queryset=Complaint.objects.all())
    return render(request, 'complaint_filter.html', {'filter': f})
    

