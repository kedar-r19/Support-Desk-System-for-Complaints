from django.urls import path

from leads.models import Agent
from .views import AgentListView, AgentCreateView, AgentDetailView, AgentDeleteView, AgentUpdateView

app_name = 'agents'

urlpatterns = [
    path('', AgentListView.as_view()),
    path('create/', AgentCreateView.as_view()),
    path('<int:pk>/', AgentDetailView.as_view()),
    path('<int:pk>/update/',AgentUpdateView.as_view()),
    path('<int:pk>/delete/',AgentDeleteView.as_view())
]