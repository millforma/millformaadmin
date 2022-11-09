import json
import re
from django.utils import timezone
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Table, Paragraph, Image
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import ListFlowable, ListItem
from main.models.company import Company
from main.models.formationsession import FormationSession


def genDeroulePedagogiqueFirst(width, height, formation_id):
    widthList = [
        width * 0.1,
        width * 0.8,
        width * 0.1,
    ]
    heightList = [
        height * 0.1086,
        height * 0.04347,
        height * 0.1386,
        height * 0.0869,
        height * 0.62243,

    ]

    res = Table([

        ['', _genTitle(widthList[1], heightList[0], formation_id), ''],
        ['', _genTitletwo(widthList[1], heightList[1], formation_id), ''],
        ['', _genTableau(widthList[1], heightList[2], formation_id), ''],
        ['', _genTitlethree(widthList[1], heightList[3], formation_id), ''],
        ['', _genTableautwo(widthList[1], heightList[4],formation_id), ''],

    ],
        colWidths=widthList,
        rowHeights=heightList)
    res.setStyle([
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),


    ])
    return res


def _genTitle(width, height, formation_id):
    textstyle = ParagraphStyle('text')
    textstyle.fontSize = 17

    text2style = ParagraphStyle('text2')
    text2style.fontSize = 12

    formation_session = FormationSession.objects.get(id=formation_id)

    textstyle.alignment = TA_CENTER
    text2style.alignment = TA_CENTER

    text1 = Paragraph(
        "<b>DEROULE PEDAGOGIQUE</b>" + "<br/>" + "<br/>",
        textstyle)

    text2 = Paragraph(
        "<b>INTITULE DE LA FORMATION :</b> " + str(formation_session.name),
        text2style
    )
    res = Table([
        [text1],
        [text2]
    ],
        width,
    )

    res.setStyle([


    ])
    return res


def _genTitletwo(width, height, formation_id):

    text1style = ParagraphStyle('texttwo')
    text1style.fontSize = 11
    text1style.leading = 15
    text1style.alignment = TA_CENTER
    formation_session = FormationSession.objects.get(id=formation_id)

    text1 = Paragraph(
        "<b>PROGRAMME</b>" + "<br/>",
        text1style)

    res = Table([
        [text1],
    ],
        width,
        height)

    res.setStyle([
        ('BOTTOMPADDING', (0, 0), (0, 0), 0.03 * height),
    ])
    return res

def _genTableau(width, height,formation_id):
    widthList = [
        width * 0.3,
        width * 0.7,
    ]
    heightList = [
        height * 0.2,
        height * 0.3,
        height * 0.3,
    ]
    formation_session = FormationSession.objects.get(id=formation_id)

    list_objectifs=list(formation_session.objectifs_peda.all())

    titleleftstyle = ParagraphStyle('titleleft')
    titleleftstyle.fontSize = 8


    titleleft = Paragraph("",
                          titleleftstyle)

    textleftstyle = ParagraphStyle('textleft')
    textleftstyle.fontSize = 9
    textleft = Paragraph("<b>Matin</b>", textleftstyle),

    titlerightstyle = ParagraphStyle('titleright')
    titlerightstyle.fontSize = 9
    titleright = Paragraph("<b>Objectifs</b>",
                           titlerightstyle)

    textrightstyle = ParagraphStyle('textright')
    textrightstyle.fontSize = 7

    textright = Paragraph(list_objectifs[0].description, textrightstyle),

    textrightstyle = ParagraphStyle('textright')
    textrightstyle.fontSize = 7
    textlefttwo = Paragraph("<b>Après-midi</b>", textrightstyle),
    if len(list_objectifs)>1:
        textrighttwo = Paragraph(list_objectifs[1].description, textrightstyle),
    else:
        textrighttwo = Paragraph(list_objectifs[0].description, textrightstyle),

    res = Table([
        [titleleft, titleright],
        [textleft, textright],
        [textlefttwo, textrighttwo],
    ],
        widthList,
        heightList)

    res.setStyle([

        ('GRID', (0, 0), (-1, -1), 1, 'black'),
        ('LEFTPADDING', (0, 0), (0, 0), 0.15 * width),
        ('LEFTPADDING', (1, 0), (1, 0), 0.08 * width),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')

    ])
    return res

def _genTitlethree(width, height, formation_id):

    text1style = ParagraphStyle('texttwo')
    text1style.fontSize = 11
    text1style.leading = 15
    text1style.alignment = TA_CENTER
    formation_session = FormationSession.objects.get(id=formation_id)

    text1 = Paragraph(
        "<b>SEQUENCE DU DEROULE PEDAGOGIQUE</b>" + "<br/>",
        text1style)

    res = Table([
        [text1],
    ],
        width,
        height)

    res.setStyle([
        ('BOTTOMPADDING', (0, 0), (0, 0), 0.03 * height),
    ])
    return res

def _genTableautwo(width, height,formation_id):
    widthList = [
        width * 0.1753,
        width * 0.2316,
        width * 0.1977,
        width * 0.1977,
        width * 0.1977,
    ]
    heightList = [
        height * 0.171875,
        height * 0.3984,
        height * 0.429725,
    ]
    formation_session = FormationSession.objects.get(id=formation_id)

    list_objectifs = list(formation_session.objectifs_peda.all())
    trainees=list(formation_session.trainee.all())
    titlestyle = ParagraphStyle('title')
    titlestyle.fontSize = 8

    titleleft = Paragraph("<b>Horaires</b>",
                          titlestyle)
    titleright = Paragraph("<b>Objectifs pédagogiques et opérationnels</b>",
                           titlestyle)

    titlerighttwo = Paragraph("<b>Ce que fait le formateur</b>",
                           titlestyle)
    titlerightthree = Paragraph("<b>Ce que font les participants</b>",
                           titlestyle)
    titlerightfour = Paragraph("<b>Méthodes, Exercices, Documents</b>",
                           titlestyle)


    textstyle = ParagraphStyle('text')
    textstyle.fontSize = 7
    objectifsstyle = ParagraphStyle('objectifsstyle')
    objectifsstyle.fontSize = 7

    textleft = Paragraph("<i>Avant la formation</i>", textstyle),
    if len(list_objectifs)>1:
        textright = Paragraph(list_objectifs[1].description, textstyle),
    else:
        textright = Paragraph(list_objectifs[0].description, textstyle),
    textrightone = Paragraph("Prendre connaissance des besoins des participants lors des audits téléphoniques. Remonter d’information à Mill-Forma Envoyer tous les documents obligatoires (CV, rib, Kbis, contrat de partenariat ainsi que l’ordre de mission signé) ", textstyle),
    textrighttwo = Paragraph("Faire remplir le QCM de prérequis", textstyle),
    textrightthree = Paragraph("Remontée d’information avant la demande de prise en charge afin de réadapter si besoins les programmes et durées de formation.", textstyle),
    trainees_str=''.join(str(trainee.user.last_name + " "+ trainee.user.first_name)for trainee in trainees)
    textlefttwo = Paragraph("<i>Ouverture d'une formation</i>", textstyle),
    texttworight = Paragraph("Receuillir les besoins des participants : "+"<br/>" + str(trainees_str), objectifsstyle),
    texttworightone = Paragraph("Accueillir les participants", textstyle),
    texttworighttwo = Paragraph("Se présenter", textstyle),
    texttworightthree = Paragraph("Exercices, tour de table …", textstyle),







    res = Table([
        [titleleft, titleright,titlerighttwo,titlerightthree,titlerightfour],
        [textleft, textright,textrightone,textrighttwo,textrightthree],
        [textlefttwo, texttworight,texttworightone,texttworighttwo,texttworightthree],
    ],
        widthList,
        heightList)

    res.setStyle([

        ('GRID', (0, 0), (-1, -1), 1, 'black'),

        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')

    ])
    return res



def genDeroulePedagogiqueSecond(width, height):
    widthList = [
        width * 0.1,
        width * 0.8,
        width * 0.1,
    ]


    res = Table([

        ['', _genTableauSecondPage(widthList[1], height), ''],

    ],
        colWidths=widthList,
        rowHeights=height)
    res.setStyle([
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('LEFTPADDING', (1, 2), (1, 2), 0.18 * width),

    ])
    return res

def _genTableauSecondPage(width, height):
    widthList = [
        width * 0.1753,
        width * 0.2316,
        width * 0.1977,
        width * 0.1977,
        width * 0.1977,
    ]
    heightList = [
        height * 0.25,
        height * 0.1875,
        height * 0.1875,
        height * 0.1875,
        height * 0.1875,
    ]
    titlestyle = ParagraphStyle('title')
    titlestyle.fontSize = 8

    titleleft = Paragraph("<i>Module</i>",
                          titlestyle)
    titleright = Paragraph("(Voir programme de formation)",
                           titlestyle)

    titlerighttwo = Paragraph("Présenter le programme et le déroulement de la formation (horaires, modalités pratiques…)"
                              " Recueillir les observations des participants, répondre aux questions Vérifier l’adhésion"
                              " des participants",titlestyle)

    titlerightthree = Paragraph("Écouter, poser des questions… Faire part de ses souhaits et attentes",titlestyle)
    titlerightfour = Paragraph("Interactions avec les participants",
                           titlestyle)


    textstyle = ParagraphStyle('text')
    textstyle.fontSize = 7


    textleft = Paragraph("<i>En début de formation</i>", textstyle),
    textright = Paragraph("Animer les séquences prévues de la formation", textstyle),
    textrightone = Paragraph("Présenter les séquences détaillées du programme ", textstyle),
    textrighttwo = Paragraph("Suivre assidûment la formation Signer les émargements", textstyle),
    textrightthree = Paragraph("Exercices, Interactions avec les participants", textstyle),

    textlefttwo = Paragraph("<i>Durant la formation</i>", textstyle),
    texttworight = Paragraph("Animer les séquences prévues de la formation", textstyle),
    texttworightone = Paragraph("Proposer un exercice d’application pratique de la séquence type (consignes, application, débriefing)", textstyle),
    texttworighttwo = Paragraph("Écouter, poser des questions… Faire part de ses souhaits et attentes", textstyle),
    texttworightthree = Paragraph("Exercices, Interactions avec les participants", textstyle),

    textleftthree = Paragraph("<i>Clôture de la formation </i>", textstyle),
    textthreeright = Paragraph("Évaluer l’atteinte des objectifs par les participants Recueillir la perception des participants sur la formation (voir QCM prérequis)", textstyle),
    textthreerightone = Paragraph("Faire remplir l’ensemble des QCM", textstyle),
    textthreerighttwo = Paragraph("Signer les émargements Remplir questionnaire ", textstyle),
    textthreerightthree = Paragraph("Remplir les documents Mill Forma et vérifier l’exactitude des feuilles d’émargement", textstyle),

    textleftfour = Paragraph("<i>Durant la formation</i>", textstyle),
    textfourright = Paragraph("Évaluer l’atteinte des objectifs par les participants Recueillir la perception des participants sur la formation (voir QCM prérequis)", textstyle),
    textfourrightone = Paragraph("Remettre à Mill Forma l’ensemble des documents demandés ainsi que sa facture ", textstyle),
    textfourrighttwo = Paragraph("Faire remplir par sa société le questionnaire à chaud ", textstyle),
    textfourrightthree = Paragraph("Remplir les documents Mill Forma et vérifier l’exactitude des feuilles d’émargement", textstyle),







    res = Table([
        [titleleft, titleright,titlerighttwo,titlerightthree,titlerightfour],
        [textleft, textright,textrightone,textrighttwo,textrightthree],
        [textlefttwo, texttworight,texttworightone,texttworighttwo,texttworightthree],
        [textleftthree, textthreeright, textthreerightone, textthreerighttwo, textthreerightthree],
        [textleftfour, textfourright, textfourrightone, textfourrighttwo, textfourrightthree],
    ],
        widthList,
        heightList)

    res.setStyle([

        ('GRID', (0, 0), (-1, -1), 1, 'black'),

        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')

    ])
    return res
