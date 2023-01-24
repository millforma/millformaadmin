import os
import fitz

from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.views.generic import ListView, TemplateView
from electronicSignature.settings import BASE_DIR, STATIC_ROOT
from main.models.file.document_type import DocumentType
from main.models.file.pdf_document import PdfDocument
from main.models.formationsession import FormationSession
from main.models.person import PersonProfession
from signature.models import SignatureModel

class DocumentSignListView(LoginRequiredMixin, ListView):
    template_name = 'pdf/documentSignList.html'
    model = PdfDocument

    def get_context_data(self, **kwargs):
        global type_of_doc_teacher
        global type_of_doc_learner
        global pdf_files
        context = super().get_context_data(**kwargs)

        try:
            type_of_doc_teacher = DocumentType.objects.filter(name__in=[2, 10, 6])
            type_of_doc_learner = DocumentType.objects.filter(name__in=[1])
        except DocumentType.DoesNotExist:
            messages.error(self.request, _("Initial data is not well configured"))

        formation_session = FormationSession.objects.filter(teacher_name=self.request.user)

        if self.request.user.groups.filter(name='teacher').exists():
            pdf_files = PdfDocument.objects.filter(formation_session__in=formation_session, is_signed=False,
                                                   type_of_document__in=type_of_doc_teacher)

        elif self.request.user.groups.filter(name='learner').exists():
            pdf_files = PdfDocument.objects.filter(formation_session__in=formation_session, is_signed=False,
                                                   type_of_document__in=type_of_doc_learner)

        context['files'] = pdf_files
        context['formation_session'] = formation_session

        return context


class SignaturePreView(LoginRequiredMixin, TemplateView):
    template_name = 'pdf/signPreview.html'

    def dispatch(self, request, *args, **kwargs):
        return super(SignaturePreView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doc_id = self.kwargs['doc_id']
        doc = PdfDocument.objects.get(id=doc_id)
        context['doc_url'] = doc.url()
        context['actual_filename'] = doc.full_upload_path
        context['doc_name'] = doc.original_filename
        context['path'] = doc.file_field.name
        return context

    def post(self, request, *args, **kwargs):
        doc_id = self.kwargs['doc_id']
        doc = PdfDocument.objects.get(id=doc_id)
        formation_session = doc.formation_session
        user = self.request.user
        if request.POST.get("sign_doc"):
            try:
                user_signature = SignatureModel.objects.get(signature_owner=user)
                user_signature_file_path = user_signature.signature
                teacher=formation_session.teacher_name

                if teacher not in doc.is_signed_by.all():
                    teacher_signature = SignatureModel.objects.get(signature_owner=teacher)
                    doc = self.sign_pdf(doc, user_signature_file_path, user, formation_session, teacher_signature.signature)
                else:
                    doc = self.sign_pdf(doc, user_signature_file_path, user, formation_session, None)


                doc.is_signed = True
                doc.is_signed_by.add(self.request.user)
                doc.is_signed_by.add(teacher)
                doc.save()
            except SignatureModel.DoesNotExist:
                messages.error(self.request,
                               _("Vous devez d'abord enregistrer votre signature"))
                return redirect('save_signature')

        return redirect('main:home')

    def sign_pdf(self, source_file, signature, user, formation_session, teacher_signature):
        des_file = source_file.actual_file
        img_filename = signature


        image_file = os.path.join(STATIC_ROOT, 'assets/images/electronic_signature.png')

        document = fitz.open(source_file.actual_file.file)
        page = document[0]
        w_page = page.rect.width
        h_page = page.rect.height
        num_signed_trainees = source_file.numb_of_signed_trainees
        num_trainees = formation_session.num_present_trainee
        # http://pymupdf.readthedocs.io/en/latest/rect/
        # Set position and size according to your needs
        if 'Emargement' in source_file.original_filename:
            y_zero = h_page * (0.5256 + num_signed_trainees * (0.2444 / num_trainees))
            y_one = (0.2444 * h_page) / num_trainees + y_zero - 4

            img_rect_one_left = fitz.Rect(round(w_page * 0.36), y_zero, round(w_page * 0.56), y_one)
            img_one_right = fitz.Rect(round(w_page * 0.66), y_zero, round(w_page * 0.86), y_one)
            img_2fa_one_left = fitz.Rect(round(w_page * 0.36), y_zero, round(w_page * 0.56), y_one)
            img_2fa_one_right = fitz.Rect(round(w_page * 0.66), y_zero, round(w_page * 0.86), y_one)
            source_file.numb_of_signed_trainees = num_signed_trainees + 1
            source_file.save()
            page.insertImage(img_rect_one_left, filename=img_filename)
            page.insertImage(img_one_right, filename=img_filename)
            page.insertImage(img_2fa_one_left, filename=image_file)
            page.insertImage(img_2fa_one_right, filename=image_file)
            #insert teacher signature
            if teacher_signature != None:
                img_teacher_signature = fitz.Rect(round(w_page * 0.14), h_page * 0.85, round(w_page * 0.34), h_page * 0.91)
                rect_title = (round(w_page * 0.14), h_page * 0.79, round(w_page * 0.34), h_page * 0.84)
                rect_first_name_teacher = (round(w_page * 0.14), h_page * 0.81, round(w_page * 0.34), h_page * 0.86)
                rect_last_name_teacher = (round(w_page * 0.14), h_page * 0.83, round(w_page * 0.34), h_page * 0.88)

                page.insertImage(img_teacher_signature, filename=image_file)
                page.insertImage(img_teacher_signature, filename=teacher_signature)

                first_name_teacher = formation_session.teacher_name.first_name
                last_name_teacher = formation_session.teacher_name.last_name
                name_tea = page.insertTextbox(rect_first_name_teacher, first_name_teacher,
                                        fontsize=11,
                                        align=1)

                las_name_tea = page.insertTextbox(rect_last_name_teacher, last_name_teacher,
                                              fontsize=11,
                                              align=1)
                title = page.insertTextbox(rect_title, "Le formateur:",
                                              fontsize=13,
                                              align=1)
            # See http://pymupdf.readthedocs.io/en/latest/document/#Document.save and
            # http://pymupdf.readthedocs.io/en/latest/document/#Document.saveIncr for
            # additional parameters, especially if you want to overwrite existing PDF
            # instead of writing new PDF
            first_name = user.first_name
            last_name = user.last_name
            y_one_f_name = y_one / 2 + y_zero / 2
            rect_name = (round(w_page * 0.124), y_zero, round(w_page * 0.297), y_one_f_name)
            rect_firstname = (round(w_page * 0.124), y_one_f_name, round(w_page * 0.297), y_one)
            rc = page.insertTextbox(rect_name, first_name,
                                    fontsize=13,
                                    align=1)
            rc = page.insertTextbox(rect_firstname, last_name,
                                    fontsize=13,
                                    align=1)
        elif 'BonDeCommande' in source_file.original_filename:
            img_rect_one_left = fitz.Rect(round(w_page * 0.14), h_page * 0.85, round(w_page * 0.34), h_page * 0.91)

            page.drawRect(img_rect_one_left, color=(.25, 1, 0.25))
            source_file.numb_of_signed_trainees = num_signed_trainees + 1
            source_file.save()
            page.insertImage(img_rect_one_left, filename=img_filename)

        elif 'Compte_rendu_de_formation' in source_file.original_filename:
            img_rect_one_left = fitz.Rect(round(w_page * 0.6), h_page * 0.85, round(w_page * 0.8), h_page * 0.91)

            page.drawRect(img_rect_one_left, color=(.25, 1, 0.25))
            source_file.numb_of_signed_trainees = num_signed_trainees + 1
            source_file.save()
            page.insertImage(img_rect_one_left, filename=img_filename)

        elif 'Contrat_De_Partenariat' in source_file.original_filename:
            page = document[2]
            w_page = page.rect.width
            h_page = page.rect.height
            img_rect_one_left = fitz.Rect(round(w_page * 0.14), h_page * 0.75, round(w_page * 0.34), h_page * 0.81)

            page.drawRect(img_rect_one_left, color=(.25, 1, 0.25))
            source_file.numb_of_signed_trainees = num_signed_trainees + 1
            source_file.save()
            page.insertImage(img_rect_one_left, filename=img_filename)

        dst_pdf_filename = f"{source_file.original_filename[0:25]}_signedby_{user.first_name}_" \
                           f"{user.last_name}_{source_file.numb_of_signed_trainees}.pdf"

        document.save(dst_pdf_filename)
        result = ContentFile(document.convert_to_pdf(), name=dst_pdf_filename)
        source_file.actual_file = result
        source_file.save()
        document.close()
        messages.success(self.request, _("Merci, votre émargement est désormais signé !"))
        return source_file
