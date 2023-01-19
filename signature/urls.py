from django.urls import path

from .views.list_attendance import AttendanceSignListView
from .views.pdf_signature import DocumentSignListView, SignaturePreView
from .views.save_signature import SaveSignatureView

app_name = 'signature'

urlpatterns = [

    path('pdf/signature/', DocumentSignListView.as_view(), name='pdflist'),
    path('pdf/signature/preview/<int:doc_id>/', SignaturePreView.as_view(), name='pdf_sign'),
    path('learner/<uuid:formation_id>/', AttendanceSignListView.as_view(), name='Attendance_list_view'),
    path('save_signature/', SaveSignatureView.as_view(), name='save_signature'),


]
