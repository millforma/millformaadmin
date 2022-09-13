from django.urls import path

from pdfDossier.views.main_pdf import Generate_formation_files_view

app_name = 'pdfDossier'


urlpatterns = [

    path('pdf/<uuid:formation_id>/', Generate_formation_files_view, name='generate_formation'),

]

