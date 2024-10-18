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
            return qs.filter(recruiter=request.user)
        return qs

    # Automatically set the recruiter field when a new object is created
    def save_model(self, request, obj, form, change):
        if not change:  # If the object is being created, not updated
            obj.recruiter = request.user
        obj.save()
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.type == 'Recruiter':
            return qs.filter(recruiter=request.user)
        return qs

    # Allow recruiters to only edit their own objects
    def has_change_permission(self, request, obj=None):
        if obj is not None and request.user.type == 'Recruiter':
            return obj.recruiter == request.user
        return super().has_change_permission(request, obj)

    # Allow recruiters to only delete their own objects
    def has_delete_permission(self, request, obj=None):
        if obj is not None and request.user.type == 'Recruiter':
            return obj.recruiter == request.user
        return super().has_delete_permission(request, obj)
admin.site.register(Company, CompanyAdmin)

class JobAdmin(admin.ModelAdmin):
    # Display only the jobs created by the logged-in recruiter
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
    def has_change_permission(self, request, obj=None):
        if obj is not None and request.user.type == 'Recruiter':
            return obj.recruiter == request.user
        return super().has_change_permission(request, obj)

    # Allow recruiters to only delete their own objects
    def has_delete_permission(self, request, obj=None):
        if obj is not None and request.user.type == 'Recruiter':
            return obj.recruiter == request.user
        return super().has_delete_permission(request, obj)
admin.site.register(Job, JobAdmin)