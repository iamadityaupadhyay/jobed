from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(UserModel)
# admin.site.register(Company)
# admin.site.register(Job)



class CompanyAdmin(admin.ModelAdmin):
    
    exclude = ['user']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.type == 'Recruiter':
            return qs.filter(user=request.user)
        return qs

    
    def save_model(self, request, obj, form, change):
        if not change: 
            obj.user = request.user
        obj.save()
    
    def has_add_permission(self, request):
        return request.user.is_staff  

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
    exclude = ['user']
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.user.type == 'Recruiter':
            form.base_fields['company'].queryset = Company.objects.filter(user=request.user)
        return form
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    def save_model(self, request, obj, form, change):
        if not change: 
            obj.user = request.user
        obj.save()
    
    def has_add_permission(self, request):
        return request.user.is_staff  

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_staff
    
    def has_module_permission(self, request):
        return request.user.is_staff

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff
admin.site.register(Job, JobAdmin)