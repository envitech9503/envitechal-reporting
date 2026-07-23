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
    path('reagent_prep_doc_save/', views.reagent_prep_doc_save, name='reagent_prep_doc_save'),
]
