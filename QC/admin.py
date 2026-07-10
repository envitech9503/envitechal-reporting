from django.contrib import admin
from QC.models import *
# Register your models here.


@admin.register(Dw_rds)
class Dw_rdsAdmin(admin.ModelAdmin):
    list_display = ("id", "sample_id", "created_at")
    search_fields = ("sample_id",)
    ordering = ("-created_at",)
    
    

@admin.register(Ww_rds)
class Ww_rdsAdmin(admin.ModelAdmin):
    list_display = ("id", "sample_id", "created_at")
    search_fields = ("sample_id",)
    ordering = ("-created_at",)
    
    
@admin.register(QCAuditConfig)
class QCAuditConfigAdmin(admin.ModelAdmin):
    list_display = ['use_manual_dw', 'use_manual_ww']
    
    
@admin.register(TestingResultsOfDWSamples)
class TestingResultsOfDWSamplesAdmin(admin.ModelAdmin):
    list_display = ("id", "sample_id", "created_at")
    search_fields = ("sample_id",)
    ordering = ("-created_at",)
    
    
@admin.register(TestingResultsOfWWSamples)
class TestingResultsOfWWSamplesAdmin(admin.ModelAdmin):
    list_display = ("id", "sample_id", "created_at")
    search_fields = ("sample_id",)
    ordering = ("-created_at",)