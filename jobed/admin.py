from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(UserModel)
# admin.site.register(Company)
# admin.site.register(Job)



class CompanyAdmin(admin.ModelAdmin):
    # Display only the objects created by the logged-in recruiter
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.type == 'Recruiter':
            return qs.filter(user=request.user)
        return qs

    # Automatically set the recruiter when a new job is created
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new object
            obj.user = request.user
        obj.save()
    
    def has_add_permission(self, request):
        # Allow users to add objects
        return request.user.is_staff  # or any other condition like request.user.role == 'recruiter'

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_staff
    
    def has_module_permission(self, request):
        return request.user.is_staff

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff
    
admin.site.register(Company, CompanyAdmin)

class JobAdmin(admin.ModelAdmin):
    # Display only the jobs created by the logged-in recruiter
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            # If the user is a superuser, return all objects
            return qs
        # If the user is a recruiter, filter the queryset to only show their own objects
        return qs.filter(user=request.user)
    # Automatically set the recruiter when a new job is created
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new object
            obj.user = request.user
        obj.save()
    
    def has_add_permission(self, request):
        # Allow users to add objects
        return request.user.is_staff  # or any other condition like request.user.role == 'recruiter'

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_staff
    
    def has_module_permission(self, request):
        return request.user.is_staff

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff
admin.site.register(Job, JobAdmin)