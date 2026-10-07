from django.urls import path
from . import views

urlpatterns = [
    path('qc_main/', views.qc_main, name='qc_main'),
    path('create_dw_qc/',views.create_dw_qc,name="create_dw_qc"),
    path('get_dw/',views.get_dw,name="get_dw"),
    path('generate_dw_qc_pdf_response/<int:pk>/',views.generate_dw_qc_pdf_response,name="generate_dw_qc_pdf_response"),
    path('dw_rds_list/',views.dw_rds_list,name='dw_rds_list'),
    
    path('create_ww_qc/',views.create_ww_qc,name="create_ww_qc"),
    path('get_ww/',views.get_ww,name="get_ww"),
    path('generate_ww_qc_pdf_response/<int:pk>/',views.generate_ww_qc_pdf_response,name="generate_ww_qc_pdf_response"),
    path('ww_rds_list/',views.ww_rds_list,name='ww_rds_list'),
    
    
    path('create_dw_qc_manual/',views.create_dw_qc_manual,name="create_dw_qc_manual"),
    path('create_ww_qc_manual/',views.create_ww_qc_manual,name="create_ww_qc_manual"),
    
    path('dw_testing_results_sample/',views.dw_testing_results_sample, name='dw_testing_results_sample'),
    path('dw_testing_results_sample_save/',views.dw_testing_results_sample_save, name='dw_testing_results_sample_save'),
    path('dw-testing-results-list/', views.dw_testing_results_sample_list, name='dw_testing_results_sample_list'),
    path('dw_testing_results_sample_pdf_from_list/<int:pk>/',views.dw_testing_results_sample_pdf_from_list, name='dw_testing_results_sample_pdf_from_list'),
    
    path('ww_testing_results_sample/',views.ww_testing_results_sample, name='ww_testing_results_sample'),
    path('ww_testing_results_sample_save/',views.ww_testing_results_sample_save, name='ww_testing_results_sample_save'),   
    path('ww-testing-results-list/', views.ww_testing_results_sample_list, name='ww_testing_results_sample_list'),
    path('ww_testing_results_sample_pdf_from_list/<int:pk>/',views.ww_testing_results_sample_pdf_from_list, name='ww_testing_results_sample_pdf_from_list'),   
    path('reagent_prep/', views.reagent_prep, name='reagent_prep'),
    path('reagent_prep_save/', views.reagent_prep_save, name='reagent_prep_save'),
    path('reagent-prep-list/', views.reagent_prep_list, name='reagent_prep_list'),
    path('reagent_prep_calculator/', views.reagent_prep_calculator, name='reagent_prep_calculator'),
    path('reagent_prep_pdf_from_list/<int:pk>/', views.reagent_prep_pdf_from_list, name='reagent_prep_pdf_from_list'),
    path('reagent_prep_verify/', views.reagent_prep_verify, name='reagent_prep_verify'),
    path('reagent_prep_manual/', views.reagent_prep_manual, name='reagent_prep_manual'),


    path('reagent_prep_month_pdf/', views.reagent_prep_month_pdf, name='reagent_prep_month_pdf'),

    path('reagent_prep_doc_save/', views.reagent_prep_doc_save, name='reagent_prep_doc_save'),
    path('reagent_prep_delete/', views.reagent_prep_delete, name='reagent_prep_delete'),

    # Control Charts (ETAL-LAB-604-FF-11), 07-10-2026
    path('control-charts/', views.control_chart_list, name='control_chart_list'),
    path('control-charts/new/', views.control_chart_edit, name='control_chart_new'),
    path('control-charts/archive/', views.control_chart_archive, name='control_chart_archive'),
    path('control_chart_manual/', views.control_chart_manual, name='control_chart_manual'),
    path('control-charts/reviewers/', views.control_chart_reviewers, name='control_chart_reviewers'),
    path('control-charts/<int:pk>/', views.control_chart_detail, name='control_chart_detail'),
    path('control-charts/<int:pk>/edit/', views.control_chart_edit, name='control_chart_edit'),
    path('control-charts/<int:pk>/baseline/', views.control_chart_baseline, name='control_chart_baseline'),
    path('control-charts/<int:pk>/result/', views.control_chart_result_save, name='control_chart_result_save'),
    path('control-charts/<int:pk>/result/<int:rid>/delete/', views.control_chart_result_delete, name='control_chart_result_delete'),
    path('control-charts/<int:pk>/signoff/', views.control_chart_signoff, name='control_chart_signoff'),
    path('control-charts/<int:pk>/pdf/', views.control_chart_pdf, name='control_chart_pdf'),
]
