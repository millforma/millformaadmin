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
from pdfDossier.views.deroule_pedagogique import genDeroulePedagogiqueFirst, genDeroulePedagogiqueSecond
from pdfDossier.views.evaluation_formation_clients import genEvaluationFormationClients

from pdfDossier.views.footer import genFooterTable
from pdfDossier.views.header import genHeaderTable, genHeaderReglementTable
from pdfDossier.views.qcm_prerequis_mill_forma import genQcmPrerequisMillForma, genQcmPrerequisMillFormaSecond
from pdfDossier.views.ques_satisfation_a_chaud import genQuesSatisfactionChaud

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

def Generate_convocations(request, formation_id):
    width, height = A4
    module_dir = os.path.dirname(__file__)
    formation_session = FormationSession.objects.get(id=formation_id)
    num_dossier=formation_session.old_num_formation
    files = []
    heightList_multiple_page = [height * 0.14,
                                height * 0.735,
                                height * 0.125,
                                ]
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
        name_of_trainee = trainee.user.first_name +' '+ trainee.user.last_name
        file_name = f"Convocation_{name_of_trainee}.pdf"
        convoc = buffer.getvalue()
        save_file_in_db(convoc, formation_session, file_name, user=request.user,doc_type=3)

        buffer.close()

        files.append((file_name, convoc))
    #############################################################################################################
    full_zip_in_memory = generate_zip(files)
    name_folder = "Convocations.zip"
    response = HttpResponse(full_zip_in_memory, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(name_folder)

    return response

def Generate_convention(request, formation_id):
    width, height = A4
    module_dir = os.path.dirname(__file__)
    formation_session = FormationSession.objects.get(id=formation_id)
    num_dossier=formation_session.old_num_formation
    files = []
    heightList_multiple_page = [height * 0.14,
                                height * 0.735,
                                height * 0.125,
                                ]
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
        [genConventionFormationSecond(width, heightList_multiple_page[1], formation_id)],
        [genFooterTable(width, heightList_solo_page[2])],
    ],
        colWidths=width,
        rowHeights=heightList_solo_page
    )
    ConventionFormationThird = Table([
        [genHeaderTable(width, heightList_solo_page[0])],
        [genConventionFormationThird(width, heightList_multiple_page[1], formation_id)],
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
                    user=request.user, doc_type=9)
    buffer.close()
    files.append(("Convention_de_formation.pdf", conventiondeformation))

    ########################################################################################################
    full_zip_in_memory = generate_zip(files)
    name_folder ="Convention_de_formation.zip"
    response = HttpResponse(full_zip_in_memory, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(name_folder)

    return response



def Generate_formation_files_view(request, formation_id):
    width, height = A4
    module_dir = os.path.dirname(__file__)
    formation_session = FormationSession.objects.get(id=formation_id)
    num_dossier=formation_session.old_num_formation
    files = []


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
    files.append(("Bon_de_commande.pdf", bondecommande))

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
    save_file_in_db(contratdepartenariat, formation_session, "Contrat_de_partenariat.pdf", user=request.user,doc_type=2)
    buffer.close()
    files.append(("Contrat_de_partenariat.pdf", contratdepartenariat))



    ######################################################################################################
    ####################################### QUESTIONNAIRE DE SATISFACTION A CHAUD#########################################
    for trainee in formation_session.trainee.all():
        buffer = io.BytesIO()
        ques_satisfaction_chaud = canvas.Canvas(buffer, pagesize=A4)
        ques_satisfaction_chaud.setTitle('Questionnaire de satisfaction à chaud')

        heightList_multiple_page = [height * 0.14,
                                    height * 0.735,
                                    height * 0.125,
                                    ]

        quessatisfactionchaud = Table([
            [genHeaderTable(width, heightList_multiple_page[0])],
            [genQuesSatisfactionChaud(width, heightList_multiple_page[1], formation_id,trainee.user)],
            [genFooterTable(width, heightList_multiple_page[2])],
        ],
            colWidths=width,
            rowHeights=heightList_multiple_page
        )

        quessatisfactionchaud.setStyle([

            ('LEFTPADDING', (1, 1), (0, 2), 0.1475 * width),

        ])

        quessatisfactionchaud.wrapOn(ques_satisfaction_chaud, 0, 0)
        quessatisfactionchaud.drawOn(ques_satisfaction_chaud, 0, 0)

        ques_satisfaction_chaud.showPage()

        ques_satisfaction_chaud.save()
        quessatisfachaud = buffer.getvalue()
        name_file="Questionnaire_de_satisfaction_a_chaud_"+str(trainee.user.last_name)+str(trainee.user.first_name)+".pdf"
        save_file_in_db(quessatisfachaud, formation_session, name_file,
                        user=request.user,doc_type=4)
        buffer.close()
        files.append((name_file, quessatisfachaud))

    # ##################################################################################################################
        ####################################### DEROULE PEDA######################################################
        buffer = io.BytesIO()
        deroule_peda = canvas.Canvas(buffer, pagesize=A4)
        deroule_peda.setTitle('Déroulé pédagogique')

        heightList_multiple_page = [height * 0.14,
                                    height * 0.735,
                                    height * 0.125,
                                    ]

        firstPagederoulePeda = Table([
            [genHeaderTable(width, heightList_multiple_page[0])],
            [genDeroulePedagogiqueFirst(width, heightList_multiple_page[1], formation_id)],
            [genFooterTable(width, heightList_multiple_page[2])],
        ],
            colWidths=width,
            rowHeights=heightList_multiple_page
        )
        secondPagederoulePeda = Table([
            [genHeaderTable(width, heightList_multiple_page[0])],
            [genDeroulePedagogiqueSecond(width, heightList_multiple_page[1])],
            [genFooterTable(width, heightList_multiple_page[2])],
        ],
            colWidths=width,
            rowHeights=heightList_multiple_page
        )
        firstPagederoulePeda.setStyle([

            ('LEFTPADDING', (1, 1), (0, 2), 0.1475 * width),

        ])
        secondPagederoulePeda.setStyle([

            ('LEFTPADDING', (1, 1), (0, 2), 0.1475 * width),

        ])

        firstPagederoulePeda.wrapOn(deroule_peda, 0, 0)
        firstPagederoulePeda.drawOn(deroule_peda, 0, 0)

        deroule_peda.showPage()

        secondPagederoulePeda.wrapOn(deroule_peda, 0, 0)
        secondPagederoulePeda.drawOn(deroule_peda, 0, 0)

        deroule_peda.showPage()

        deroule_peda.save()
        deroulepeda = buffer.getvalue()
        save_file_in_db(deroulepeda, formation_session, "Deroule_pedagogique.pdf", user=request.user,
                        doc_type=6)
        buffer.close()
        files.append(("Deroule_pedagogique.pdf", deroulepeda))

        ######################################################################################################################
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
    ####################################### QCM PREREQUIS MILL FORMA ######################################
    buffer = io.BytesIO()
    qcm_prerequis_mill_forma = canvas.Canvas(buffer, pagesize=A4)
    qcm_prerequis_mill_forma.setTitle('Qcm Prerequis Mill Forma')

    heightList_solo_page = [height * 0.14,
                            height * 0.735,
                            height * 0.125,
                            ]

    QcmPrerequisMillFormaFirst = Table([
        [genHeaderTable(width, heightList_solo_page[0])],
        [genQcmPrerequisMillForma(width, heightList_solo_page[1], formation_id)],
        [genFooterTable(width, heightList_solo_page[2])],
    ],
        colWidths=width,
        rowHeights=heightList_solo_page
    )
    QcmPrerequisMillFormaSecond = Table([
        [genHeaderTable(width, heightList_solo_page[0])],
        [genQcmPrerequisMillFormaSecond(width, heightList_solo_page[1])],
        [genFooterTable(width, heightList_solo_page[2])],
    ],
        colWidths=width,
        rowHeights=heightList_solo_page
    )

    QcmPrerequisMillFormaFirst.setStyle([

        ('LEFTPADDING', (1, 1), (0, 2), 0.1475 * width),

    ])
    QcmPrerequisMillFormaSecond.setStyle([

        ('LEFTPADDING', (1, 1), (0, 2), 0.1475 * width),

    ])

    QcmPrerequisMillFormaFirst.wrapOn(qcm_prerequis_mill_forma, 0, 0)
    QcmPrerequisMillFormaFirst.drawOn(qcm_prerequis_mill_forma, 0, 0)

    qcm_prerequis_mill_forma.showPage()

    QcmPrerequisMillFormaSecond.wrapOn(qcm_prerequis_mill_forma, 0, 0)
    QcmPrerequisMillFormaSecond.drawOn(qcm_prerequis_mill_forma, 0, 0)
    qcm_prerequis_mill_forma.showPage()

    qcm_prerequis_mill_forma.save()
    qcmprerequis = buffer.getvalue()
    save_file_in_db(qcmprerequis, formation_session, "Questionnaire_prerequis.pdf", user=request.user,doc_type=4)
    buffer.close()
    files.append(("Questionnaire_prerequis.pdf", qcmprerequis))

    #######################################################################################################################
    ####################################### EVALUATION FORMATION SATISFACTION CLIENTS######################################
    buffer = io.BytesIO()
    evaluation_satisfactions_clients = canvas.Canvas(buffer, pagesize=A4)
    evaluation_satisfactions_clients.setTitle('Evaluation satisfaction clients')

    heightList_solo_page = [height * 0.14,
                            height * 0.735,
                            height * 0.125,
                            ]

    EvaluationFormationClients = Table([
        [genHeaderTable(width, heightList_solo_page[0])],
        [genEvaluationFormationClients(width, heightList_solo_page[1])],
        [genFooterTable(width, heightList_solo_page[2])],
    ],
        colWidths=width,
        rowHeights=heightList_solo_page
    )

    EvaluationFormationClients.setStyle([

        ('LEFTPADDING', (1, 1), (0, 2), 0.1475 * width),

    ])

    EvaluationFormationClients.wrapOn(evaluation_satisfactions_clients, 0, 0)
    EvaluationFormationClients.drawOn(evaluation_satisfactions_clients, 0, 0)

    evaluation_satisfactions_clients.showPage()

    evaluation_satisfactions_clients.save()

    evaluationsatisf = buffer.getvalue()
    save_file_in_db(evaluationsatisf, formation_session, "Evaluation_satisfactions_clients.pdf", user=request.user,doc_type=4)
    buffer.close()
    files.append(("Evaluation_satisfactions_clients.pdf", evaluationsatisf))

    #######################################################################################################################


    full_zip_in_memory = generate_zip(files)
    name_folder=str(num_dossier)+"_dossier_formation.zip"
    response = HttpResponse(full_zip_in_memory, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(name_folder)

    return response
