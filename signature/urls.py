from django.urls import path





from .views.list_attendance import AttendanceSignListView
from .views.pdf_signature import DocumentSignListView, SignaturePreView

app_name = 'signature'

urlpatterns = [

    path('pdf/signature/<int:formation_id>/', DocumentSignListView.as_view(), name='pdflist'),
    path('pdf/signature/preview/<int:doc_id>/', SignaturePreView.as_view(), name='pdf_sign'),
    path('learner/<uuid:formation_id>/', AttendanceSignListView.as_view(), name='Attendance_list_view'),

]
