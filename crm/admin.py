from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(CustomerModel)
class CustomerAdmin(admin.ModelAdmin):
    readonly_fields = ("user_created", "user_modified", "created_date", "modified_date")
    search_fields = ("fisrtname", "lastname", "company", "code")
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.user_modified = request.user
        else:
            obj.user_created = request.user
            obj.user_modified = request.user
        return super().save_model(request, obj, form, change)
    
@admin.register(DocumentsModel)
class DocumentsAdmin(admin.ModelAdmin):
    readonly_fields = ("user_created", "user_modified", "created_date", "modified_date")
    search_fields = ("customer",)
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.user_modified = request.user
        else:
            obj.user_created = request.user
            obj.user_modified = request.user
        return super().save_model(request, obj, form, change)
    
@admin.register(ExhibitionModel)
class ExhibitionAdmin(admin.ModelAdmin):
    readonly_fields = ("user_created", "user_modified", "created_date", "modified_date")
    search_fields = ("title",)
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.user_modified = request.user
        else:
            obj.user_created = request.user
            obj.user_modified = request.user
        return super().save_model(request, obj, form, change)
    
@admin.register(InvoiceModel)
class InvoiceAdmin(admin.ModelAdmin):
    readonly_fields = ("user_created", "user_modified", "created_date", "modified_date")
    search_fields = ("customer", "exhibition")
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.user_modified = request.user
        else:
            obj.user_created = request.user
            obj.user_modified = request.user
        return super().save_model(request, obj, form, change)