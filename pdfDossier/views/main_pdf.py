import io
import zipfile
import docx
import os
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table

from main.models.file.document_type import DocumentType
from main.models.file.pdf_document import PdfDocument
from main.models.formationsession import FormationSession
from pdfDossier.views.bondecommande import genBondecommandeTable
from pdfDossier.views.compte_rendu_formation import genCompteRenduFormation
from pdfDossier.views.contrat_de_partenariat_formateur import genContratFormateurFirstPageTable, \
    genContratFormateurSecondPageTable, genContratFormateurThirdPageTable
from pdfDossier.views.convention_de_formation import genConventionFormationFirst, genConventionFormationSecond, \
    genConventionFormationThird, genConventionFormationFourth
from pdfDossier.views.convocation import genConvocation

from pdfDossier.views.footer import genFooterTable
from pdfDossier.views.header import genHeaderTable, genHeaderReglementTable

from pdfDossier.views.reglement_interieur import genReglementInterieurFirstPageTable, genReglementInterieurSecondPageTable


def save_file_in_db(pdffile, formation_session, name, user,doc_type):
    file = ContentFile(pdffile, name=name)
    try:
        PdfDocument.objects.get(formation_session=formation_session, original_filename=name)
    except ObjectDoesNotExist:
        try:
            type = DocumentType.objects.get(name=doc_type)
        except DocumentType.DoesNotExist:
            type = DocumentType.objects.create(name=doc_type)
        temp = PdfDocument.objects.create(formation_session=formation_session, actual_file=file, original_filename=name,
                                          creator=user.person,type_of_document=type)
        temp.save()
    except MultipleObjectsReturned:
        print("Already created pdf for this formation")
    else:
        pass


def generate_zip(files):
    mem_zip = io.BytesIO()

    with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.writestr(f[0], f[1])

    return mem_zip.getvalue()


def Generate_formation_files_view(request, formation_id):
    width, height = A4
    module_dir = os.path.dirname(__file__)
    formation_session = FormationSession.objects.get(id=formation_id)
    num_dossier=formation_session.old_num_formation
    files = []
    buffer = io.BytesIO()
    # Adding QCM Files
    compte_rendu = buffer.getvalue()
    buffer.close()
    compte_rendu_path=os.path.join(module_dir, 'word_files/COMPTE-RENDU DE FORMATION.docx')
    doc = docx.Document(compte_rendu_path)
    files.append(("COMPTE-RENDU DE FORMATION.docx", compte_rendu))

    buffer = io.BytesIO()
    # Adding QCM Files
    compte_rendu = buffer.getvalue()
    buffer.close()
    compte_rendu_path = os.path.join(module_dir, 'word_files/QCM EVALUATION DES ACQUIS.docx')
    doc = docx.Document(compte_rendu_path)
    files.append(("QCM EVALUATION DES ACQUIS.docx", compte_rendu))

    buffer = io.BytesIO()
    # Adding QCM Files
    compte_rendu = buffer.getvalue()
    buffer.close()
    compte_rendu_path = os.path.join(module_dir, 'word_files/QCM PREREQUIS MILL FORMA.docx')
    doc = docx.Document(compte_rendu_path)
    files.append(("QCM PREREQUIS MILL FORMA.docx", compte_rendu))

    buffer = io.BytesIO()
    # Adding QCM Files
    compte_rendu = buffer.getvalue()
    buffer.close()
    compte_rendu_path = os.path.join(module_dir, 'word_files/Questionnaire de Satisfaction Client a chaud MILL-FORMA.docx')
    doc = docx.Document(compte_rendu_path)
    files.append(("Questionnaire de Satisfaction Client a chaud MILL-FORMA.docx", compte_rendu))


    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    # Create the PDF object, using the buffer as its "file."
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.


    pdf_bondecommande = canvas.Canvas(buffer, pagesize=A4)
    pdf_bondecommande.setTitle('Ordre de Mission Mill Forma')

    heightList_solo_page = [height * 0.12,
                            height * 0.755,
                            height * 0.125,
                            ]

    mainTable = Table([
        [genHeaderTable(width, heightList_solo_page[0])],
        [genBondecommandeTable(width, heightList_solo_page[1], formation_id, user=request.user)],
        [genFooterTable(width, heightList_solo_page[2])],
    ],
        colWidths=width,
        rowHeights=heightList_solo_page
    )

    mainTable.setStyle([
        ('LEFTPADDING', (1, 1), (0, 2), 0.1475 * width),
    ])

    mainTable.wrapOn(pdf_bondecommande, 0, 0)
    mainTable.drawOn(pdf_bondecommande, 0, 0)

    pdf_bondecommande.showPage()
    pdf_bondecommande.save()
    bondecommande = buffer.getvalue()

    save_file_in_db(bondecommande, formation_session, "BonDeCommande.pdf", user=request.user,doc_type=10)

    buffer.close()
    files.append(("BonDeCommande.pdf", bondecommande))

    # ----------------------
    buffer = io.BytesIO()
    pdf_contrat_de_partenariat_formateur = canvas.Canvas(buffer, pagesize=A4)
    pdf_contrat_de_partenariat_formateur.setTitle('Contrat de partenariat formateur')

    heightList_multiple_page = [height * 0.12,
                                height * 0.88,
                                ]

    firstPage = Table([
        [genHeaderTable(width, heightList_multiple_page[0])],
        [genContratFormateurFirstPageTable(width, heightList_multiple_page[1], formation_id)],
    ],
        colWidths=width,
        rowHeights=heightList_multiple_page
    )
    secondPage = Table([

        [genContratFormateurSecondPageTable(width, heightList_multiple_page[1])],
    ],

    )
    thirdPage = Table([

        [genContratFormateurThirdPageTable(width, heightList_multiple_page[1])],
    ],

    )

    firstPage.setStyle([

        ('LEFTPADDING', (1, 1), (0, 2), 0.1475 * width),

    ])
    secondPage.setStyle([

        ('LEFTPADDING', (1, 1), (0, 2), 0.1475 * width),
    ])
    thirdPage.setStyle([

        ('LEFTPADDING', (1, 1), (0, 2), 0.1475 * width),
    ])

    firstPage.wrapOn(pdf_contrat_de_partenariat_formateur, 0, 0)
    firstPage.drawOn(pdf_contrat_de_partenariat_formateur, 0, 0)

    pdf_contrat_de_partenariat_formateur.showPage()

    secondPage.wrapOn(pdf_contrat_de_partenariat_formateur, 0, 0)
    secondPage.drawOn(pdf_contrat_de_partenariat_formateur, 0, 0)

    pdf_contrat_de_partenariat_formateur.showPage()

    thirdPage.wrapOn(pdf_contrat_de_partenariat_formateur, 0, 0)
    thirdPage.drawOn(pdf_contrat_de_partenariat_formateur, 0, 0)

    pdf_contrat_de_partenariat_formateur.showPage()

    pdf_contrat_de_partenariat_formateur.save()
    contratdepartenariat = buffer.getvalue()
    save_file_in_db(contratdepartenariat, formation_session, "Contrat_De_Partenariat.pdf", user=request.user,doc_type=2)
    buffer.close()
    files.append(("Contrat_De_Partenariat.pdf", contratdepartenariat))



    ######################################################################################################

    ####################################### REGLEMENT INTERIEUR ##########################################
    buffer = io.BytesIO()
    pdf_reglement_interieur = canvas.Canvas(buffer, pagesize=A4)
    pdf_reglement_interieur.setTitle('Reglement interieur')

    heightList_multiple_page = [height * 0.15,
                                height * 0.725,
                                height * 0.125,
                                ]

    firstPageReglementInterieur = Table([
        [genHeaderReglementTable(width, heightList_multiple_page[0])],
        [genReglementInterieurFirstPageTable(width, heightList_multiple_page[1])],
        [genFooterTable(width, heightList_multiple_page[2])],
    ],
        colWidths=width,
        rowHeights=heightList_multiple_page
    )
    secondPageReglementInterieur = Table([
        [genHeaderReglementTable(width, heightList_multiple_page[0])],
        [genReglementInterieurSecondPageTable(width, heightList_multiple_page[1])],
        [genFooterTable(width, heightList_multiple_page[2])],
    ],
        colWidths=width,
        rowHeights=heightList_multiple_page
    )

    firstPageReglementInterieur.setStyle([

        ('LEFTPADDING', (1, 1), (0, 2), 0.1475 * width),

    ])
    secondPageReglementInterieur.setStyle([

        ('LEFTPADDING', (1, 1), (0, 2), 0.1475 * width),

    ])

    firstPageReglementInterieur.wrapOn(pdf_reglement_interieur, 0, 0)
    firstPageReglementInterieur.drawOn(pdf_reglement_interieur, 0, 0)

    pdf_reglement_interieur.showPage()
    secondPageReglementInterieur.wrapOn(pdf_reglement_interieur, 0, 0)
    secondPageReglementInterieur.drawOn(pdf_reglement_interieur, 0, 0)

    pdf_reglement_interieur.showPage()

    pdf_reglement_interieur.save()
    reglementinterieur = buffer.getvalue()
    save_file_in_db(reglementinterieur, formation_session, "Reglement_interieur.pdf", user=request.user,doc_type=5)
    buffer.close()
    files.append(("Reglement_interieur.pdf", reglementinterieur))





    ####################################################################################################
    ####################################### CONVENTION DE FORMATION ######################################
    buffer = io.BytesIO()
    convention_de_formation = canvas.Canvas(buffer, pagesize=A4)
    convention_de_formation.setTitle('Convention de formation')

    heightList_solo_page = [height * 0.14,
                            height * 0.735,
                            height * 0.125,
                            ]

    ConventionFormationFirst = Table([
        [genHeaderTable(width, heightList_solo_page[0])],
        [genConventionFormationFirst(width, heightList_solo_page[1], formation_id)],
        [genFooterTable(width, heightList_solo_page[2])],
    ],
        colWidths=width,
        rowHeights=heightList_solo_page
    )
    ConventionFormationSecond = Table([
        [genHeaderTable(width, heightList_solo_page[0])],
        [genConventionFormationSecond(width, heightList_solo_page[1], formation_id)],
        [genFooterTable(width, heightList_solo_page[2])],
    ],
        colWidths=width,
        rowHeights=heightList_solo_page
    )
    ConventionFormationThird = Table([
        [genHeaderTable(width, heightList_solo_page[0])],
        [genConventionFormationThird(width, heightList_solo_page[1], formation_id)],
        [genFooterTable(width, heightList_solo_page[2])],
    ],
        colWidths=width,
        rowHeights=heightList_solo_page
    )
    ConventionFormationFourth = Table([
        [genHeaderTable(width, heightList_solo_page[0])],
        [genConventionFormationFourth(width, heightList_solo_page[1], formation_id)],
        [genFooterTable(width, heightList_solo_page[2])],
    ],
        colWidths=width,
        rowHeights=heightList_solo_page
    )

    ConventionFormationFirst.setStyle([

        ('LEFTPADDING', (1, 1), (0, 2), 0.1475 * width),

    ])
    ConventionFormationSecond.setStyle([

        ('LEFTPADDING', (1, 1), (0, 2), 0.1475 * width),

    ])
    ConventionFormationThird.setStyle([

        ('LEFTPADDING', (1, 1), (0, 2), 0.1475 * width),

    ])
    ConventionFormationFourth.setStyle([

        ('LEFTPADDING', (1, 1), (0, 2), 0.1475 * width),

    ])

    ConventionFormationFirst.wrapOn(convention_de_formation, 0, 0)
    ConventionFormationFirst.drawOn(convention_de_formation, 0, 0)

    convention_de_formation.showPage()

    ConventionFormationSecond.wrapOn(convention_de_formation, 0, 0)
    ConventionFormationSecond.drawOn(convention_de_formation, 0, 0)

    convention_de_formation.showPage()

    ConventionFormationThird.wrapOn(convention_de_formation, 0, 0)
    ConventionFormationThird.drawOn(convention_de_formation, 0, 0)

    convention_de_formation.showPage()

    ConventionFormationFourth.wrapOn(convention_de_formation, 0, 0)
    ConventionFormationFourth.drawOn(convention_de_formation, 0, 0)

    convention_de_formation.showPage()

    convention_de_formation.save()
    conventiondeformation = buffer.getvalue()
    save_file_in_db(conventiondeformation, formation_session, "Convention_de_formation.pdf",
                    user=request.user,doc_type=9)
    buffer.close()
    files.append(("Convention_de_formation.pdf", conventiondeformation))

    ########################################################################################################
####################################### COMPTE RENDU DE FORMATION######################################################
    buffer = io.BytesIO()
    compte_rendu_de_formation = canvas.Canvas(buffer, pagesize=A4)
    compte_rendu_de_formation.setTitle('Compte rendu de formation')

    heightList_multiple_page = [height * 0.14
        ,
                                height * 0.735,
                                height * 0.125,
                                ]

    compteRenduFormation = Table([
        [genHeaderTable(width, heightList_multiple_page[0])],
        [genCompteRenduFormation(width, heightList_multiple_page[1], formation_id)],
        [genFooterTable(width, heightList_multiple_page[2])],
    ],
        colWidths=width,
        rowHeights=heightList_multiple_page
    )

    compteRenduFormation.setStyle([

        ('LEFTPADDING', (1, 1), (0, 2), 0.1475 * width),

    ])

    compteRenduFormation.wrapOn(compte_rendu_de_formation, 0, 0)
    compteRenduFormation.drawOn(compte_rendu_de_formation, 0, 0)

    compte_rendu_de_formation.showPage()

    compte_rendu_de_formation.save()
    compterendudeformation = buffer.getvalue()
    save_file_in_db(compterendudeformation, formation_session, "Compte_rendu_de_formation.pdf", user=request.user,doc_type=6)
    buffer.close()
    files.append(("Compte_rendu_de_formation.pdf", compterendudeformation))

    ######################################################################################################################
    ####################################### CONVOCATION #########################################################
    formation_session = FormationSession.objects.get(id=formation_id)

    for trainee in formation_session.trainee.all():
        buffer = io.BytesIO()
        convocation = canvas.Canvas(buffer, pagesize=A4)
        convocation.setTitle('Convocation')

        heightList_solo_page = [height * 0.14,
                                height * 0.735,
                                height * 0.125,
                                ]

        Convocation = Table([
            [genHeaderTable(width, heightList_multiple_page[0])],
            [genConvocation(width, heightList_multiple_page[1], trainee, formation_id)],
            [genFooterTable(width, heightList_multiple_page[2])],
        ],
            colWidths=width,
            rowHeights=heightList_multiple_page
        )

        Convocation.setStyle([

            ('LEFTPADDING', (1, 1), (0, 2), 0.1475 * width),

        ])

        Convocation.wrapOn(convocation, 0, 0)
        Convocation.drawOn(convocation, 0, 0)

        convocation.showPage()

        convocation.save()
        name_of_trainee = trainee.user.first_name + trainee.user.last_name
        file_name = f"Convocation_{name_of_trainee}.pdf"
        convoc = buffer.getvalue()
        save_file_in_db(convoc, formation_session, file_name, user=request.user,doc_type=3)

        buffer.close()

        files.append((file_name, convoc))
    #############################################################################################################


    full_zip_in_memory = generate_zip(files)
    name_folder=str(num_dossier)+"_dossier_formation.zip"
    response = HttpResponse(full_zip_in_memory, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(name_folder)

    return response
