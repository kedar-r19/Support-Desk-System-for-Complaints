from django.urls import path
from .views import AssignAgentView, ComplaintCreateView, ComplaintDeleteView, ComplaintListView, ComplaintDetailView, ComplaintUpdateView, ComplaintDeleteView, CategoryListView, CategoryDetailView, CategoryUpdateView, CategoryCreateView, CategoryEditView, CategoryDeleteView, complaints_filter


app_name = "leads"

urlpatterns = [
    #path('', home_page)
    path('', ComplaintListView.as_view()),
    path('create/', ComplaintCreateView.as_view()),
    path('filter/', complaints_filter),
    path('<int:pk>/',ComplaintDetailView.as_view(), name='complaint-detail'),
    path('<int:pk>/update/',ComplaintUpdateView.as_view()),
    path('<int:pk>/delete/',ComplaintDeleteView.as_view()),
    path('<int:pk>/assignagent/',AssignAgentView.as_view()),
    path('categories/', CategoryListView.as_view()),
    path('categories/create/', CategoryCreateView.as_view()),
    path('categories/<int:pk>/edit', CategoryEditView.as_view()),
    path('categories/<int:pk>/delete', CategoryDeleteView.as_view()),
    path('categories/<int:pk>/', CategoryDetailView.as_view()),
    path('<int:pk>/categories/',CategoryUpdateView.as_view()),
    
]