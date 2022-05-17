import io

from django.shortcuts import redirect
from django.urls import reverse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table

from main.models import Event
from main.models.file.pdf_document import PdfDocument
from main.models.formationsession import FormationSession
from main.views.email_view import send_attendance_inquiry
from main.views.emargement import genEmargementFirst
from main.views.footer import genFooterTable
from main.views.header import genHeaderTable
from main.views.main import save_file_in_db


def Generate_emargement(request, formation_id, event):

    try:
        formation = FormationSession.objects.get(id=formation_id)
        event_instance = Event.objects.get(id=event)
        day = event_instance.start_time.date()
        file_name = f"Emargement_du_{day.strftime('%d-%m-%Y')}_{formation.name}.pdf"

        PdfDocument.objects.get(formation_session=formation, original_filename=file_name)

    except PdfDocument.DoesNotExist:
        formation = FormationSession.objects.get(id=formation_id)
        event_instance = Event.objects.get(id=event)


        trainees = formation.trainee
        width, height = A4
        files = []
        formation_session = FormationSession.objects.get(id=formation_id)

        buffer = io.BytesIO()
        day = event_instance.start_time.date()

        emargement = canvas.Canvas(buffer, pagesize=A4)
        emargement.setTitle('Emargements stagiaires')

        heightList_solo_page = [height * 0.14,
                                height * 0.735,
                                height * 0.125,
                                ]

        EmargementFirst = Table([
            [genHeaderTable(width, heightList_solo_page[0])],
            [genEmargementFirst(width, heightList_solo_page[1], formation_id, day, event_instance)],
            [genFooterTable(width, heightList_solo_page[2])],
        ],
            colWidths=width,
            rowHeights=heightList_solo_page
        )

        EmargementFirst.setStyle([
            ('LEFTPADDING', (1, 1), (0, 2), 0.1475 * width),
        ])

        EmargementFirst.wrapOn(emargement, 0, 0)
        EmargementFirst.drawOn(emargement, 0, 0)

        emargement.showPage()
        emargement.save()

        emargement = buffer.getvalue()
        file_name = f"Emargement_du_{day.strftime('%d-%m-%Y')}_{formation.name}.pdf"
        save_file_in_db(emargement, formation_session, file_name, user=request.user,doc_type=1)
        buffer.close()



    return reverse('main:session', kwargs={'formation_id': formation.id})
