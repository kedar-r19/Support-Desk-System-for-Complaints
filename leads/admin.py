from django.contrib import admin

from .models import Category, User, Agent, Customer, Complaint

admin.site.register(User)
admin.site.register(Agent)
admin.site.register(Customer)
admin.site.register(Complaint)
admin.site.register(Category)
