from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent, User
from .forms import AgentModelForm
from .mixins import OwnerAndLoginRequiredMixin
from django.core.mail import send_mail
import random

class AgentListView(OwnerAndLoginRequiredMixin, generic.ListView):
    template_name = "agent_list.html"
    queryset = Agent.objects.all()

class AgentCreateView(OwnerAndLoginRequiredMixin, generic.CreateView):
    template_name = "agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return "/agents"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_owner = False
        user.is_customer = False
        user.set_password(f"{random.randint(0, 10000)}")
        user.save()
        Agent.objects.create(
            user = user
        )
        send_mail(
            subject = "Invited as an agent",
            message = f"You were invited as an agent, login to the system to see. Your username is {user.username}",
            from_email = "kedarraul19@yahoo.com",
            recipient_list=[user.email]
        )
        return super(AgentCreateView, self).form_valid(form)
                   

class AgentDetailView(OwnerAndLoginRequiredMixin, generic.DetailView):
    template_name = "agent_detail.html"
    queryset = Agent.objects.all()
    context_object_name = "agent"

class AgentUpdateView(OwnerAndLoginRequiredMixin, generic.UpdateView):
    template_name = "agent_update.html"
    form_class = AgentModelForm
    queryset = Agent.objects.all()

    def get_success_url(self):
        return "/agents"

class AgentUpdateView(OwnerAndLoginRequiredMixin, generic.UpdateView):
    template_name = "agent_update.html"
    form_class = AgentModelForm
   

    def get_object(self, queryset=None):
        agent_pk = self.kwargs.get('pk', None)
        return get_object_or_404(Agent, pk=agent_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        agent = self.get_object()  # -> returns an agent object
        data = {
               'username': agent.user.username,
               'first_name': agent.user.first_name,
               'last_name': agent.user.last_name,
               'email': agent.user.email,
        }
        form = self.form_class(initial=data, instance=agent.user)
        context['form'] = form  # -> updating the class view context dictionary
        return context

    # Use the post method to handle the form submission
    def post(self, request, *arg, **kwargs):
        # Should set the user instance on the form
        agent = self.get_object()
        form = self.form_class(request.POST, instance=agent.user)  
        if form.is_valid():
            form.save()
            return redirect('/agents') 

        # Passing back the form to the template
        return render(request, self.template_name, {'form': form})
     
    def get_success_url(self):
        return "/agents"


 
class AgentDeleteView(OwnerAndLoginRequiredMixin, generic.DeleteView):
    template_name = "agent_delete.html"
    queryset = Agent.objects.all()
    context_object_name = "agent"

    def get_success_url(self):
        return "/agents"
