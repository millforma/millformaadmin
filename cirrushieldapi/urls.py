from django.urls import path

from cirrushieldapi.views.email_view import send_links_for_formation, send_convention
from cirrushieldapi.views.importFormation import SaveFormation
from cirrushieldapi.views.searchFormationSession import SearchFormation
from cirrushieldapi.views.send_username_view import SendUsername
from main.views.LinkView import LinkView
from pdfDossier.views.main_pdf import Generate_convention

app_name = 'cirrushieldapi'

urlpatterns = [
    path('searchformation/', SearchFormation.as_view(), name='home_millforma'),
    path('searchformation/<slug:formation_id>/', SaveFormation.as_view(), name='postformation'),
    path('link/<uuid:formation_id>/', LinkView.as_view(), name='link_view'),
    path('send_link/<uuid:formation_id>/', send_links_for_formation, name='send_link'),
    path('send_convention/<uuid:formation_id>/', send_convention, name='send_convention'),
    path('download_convention/<uuid:formation_id>/', Generate_convention, name='download_convention'),
    path('resend_username/', SendUsername.as_view(), name='username_send'),
]