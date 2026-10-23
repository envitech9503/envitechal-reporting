"""Management Records / Reports module (24-10-2026) - mounted at /management/."""
from django.urls import path

from QC.views import mgmt

urlpatterns = [
    path('', mgmt.mgmt_home, name='mgmt_home'),
    path('ia/', mgmt.mgmt_ia, name='mgmt_ia'),
    path('document-control/', mgmt.mgmt_doc_register, name='mgmt_doc_register'),
]
