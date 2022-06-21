from django.contrib import admin
from django.urls import path, include
from crm.settings import STATIC_ROOT, STATIC_URL
from leads.views import  LandingPageView, SignupView, LoginView
from customers.views import CustomerLandingPage
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetView, PasswordResetCompleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('complaints/', include('leads.urls', namespace="complaints")),
    path('agents/', include('agents.urls', namespace="agents")),
    path('customers/', include('customers.urls', namespace="customers")),
    path('', LandingPageView.as_view()),
    path('customer_landing_page/', CustomerLandingPage.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('signup/', SignupView.as_view()),
    path('passwordreset/', PasswordResetView.as_view()),
    path('passwordresetdone/', PasswordResetDoneView.as_view(), name = 'password_reset_done'),
    path('passwordresetconfirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name = 'password_reset_confirm'),
    path('passwordresetcomplete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

"""if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)"""