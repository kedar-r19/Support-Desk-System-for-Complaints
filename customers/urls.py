from django.urls import path

from leads.models import Customer
from .views import  CustomerListView, CustomerComplaintCreateView, CustomerCreateView, CustomerDetailView, CustomerDeleteView, CustomerUpdateView, CustomerComplaintUpdateView

app_name = 'customers'

urlpatterns = [
    path('', CustomerListView.as_view()),
    path('create/', CustomerCreateView.as_view()),
    path('<int:pk>/', CustomerDetailView.as_view()),
    path('<int:pk>/update/',CustomerUpdateView.as_view(), name='update-customer'),
    path('<int:pk>/delete/',CustomerDeleteView.as_view()),
    path('complaints/create/',CustomerComplaintCreateView.as_view()),
    path('complaints/<int:pk>/update/', CustomerComplaintUpdateView.as_view()),
]