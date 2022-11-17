import io
import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.platypus import Table

from main.models.company import Company
from main.models.formationsession import FormationSession





def genQcmPrerequisMillForma(width, height, formation_id):
    widthList = [
        width * 0.1,
        width * 0.8,
        width * 0.1,
    ]
    heightList = [
        height * 0.35,
        height * 0.133,
        height * 0.075,
        height * 0.445,

    ]

    res = Table([
        ['', _genDescription(widthList[1], heightList[0], formation_id), ''],
        ['', _genTitre(widthList[1], heightList[1], formation_id), ''],
        ['', _genContenuFirst(widthList[1], heightList[2]), ''],
        ['', _genContenuSecond(widthList[1], heightList[3]), ''],

    ],
        colWidths=widthList,
        rowHeights=heightList)
    res.setStyle([

        ('ALIGN', (1, 0), (1, 0), 'CENTER'),

    ])
    return res


def _genTitre(width, height, formation_id):
    textstyle = ParagraphStyle('text')
    textstyle.fontSize = 15
    textstyle.leading = 15
    formation_session = FormationSession.objects.get(id=formation_id)
    textstyle.fontColor = colors.HexColor('#FFFFFF')
    textstyle.alignment = TA_CENTER
    text = Paragraph("<font color='white'>EXERCICE D’EVALUATION DE SORTIE DE FORMATION (ACQUIS) :</font>" +
                     "<font color='white'>" + formation_session.name + "</font>",
                     textstyle)
    res = Table([
        [text]
    ],
        width,
    )
    bluecolor = colors.HexColor('#215768')
    res.setStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 0), (0, 0), bluecolor),
        ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),

    ])
    return res


def _genDescription(width, height, formation_id):
    widthList = [
        width * 0.5,
        width * 0.5,
    ]

    textleftstyle = ParagraphStyle('textleft')
    textleftstyle.textColor = colors.HexColor('#808080')
    textleftstyle.fontSize = 11
    formation_session = FormationSession.objects.get(id=formation_id)
    client_company = formation_session.client_account
    millforma = Company.objects.get(name="Mill Forma")

    if formation_session.date_autorised_start != None:
        formation_session_date_start = formation_session.date_autorised_start.strftime('%Y-%m-%d')
    else:
        formation_session_date_start = "Non renseignée"
    if formation_session.date_autorised_end != None:
        formation_session_date_end = formation_session.date_autorised_end.strftime('%Y-%m-%d')
    else:
        formation_session_date_end = "Non renseignée"

    textleft = Paragraph("<font color='black'><b><u>L'ORGANISME DE FORMATION</u></b></font>" + "<br/>" + "<br/>"
                         + "Raison Sociale :" + "<font color='black'>" + str(millforma.raison_sociale) + "</font>" + "<br/>"
                         + "Numéro de déclaration d'activité :" + "<font color='black'>" + str(millforma.num_decla_activite)
                         + "</font>" + "<br/> "
                         + "Siret :" + "<font color='black'>" + str(millforma.num_siret) + "</font>" + "<br/>"
                         + "Adresse :" + "<font color='black'>" + millforma.adresse.string() + "</font>" + "<br/>"
                         + "<font color='black'> Ci-après « le donneur d'ordre »</font>",
                         textleftstyle)

    textrightstyle = ParagraphStyle('textright')
    textrightstyle.fontSize = 11
    textrightstyle.textColor = colors.HexColor('#808080')
    textright = Paragraph("<font color='black'><b><u>Intitulé de la formation : </u></b></font>" + "<br/>" + "<br/>"
                          + "<font color='black'>" + formation_session.name + "</font>" + "<br/>"
                          + "Date de la session :" + "<font color='black'>" + str(formation_session_date_start) + "</font>"
                          + "<font color='black'><b> au </b></font>" + "<font color='black'>" + str(formation_session_date_end)
                          + "</font>" + "<br/>"
                          + """Horaires de formation matin et après-midi : De 08H30 à 12H30 et de 13H30 à 17H30 """
                          + "<br/>"
                          + "Lieu de la formation : " + "<font color='black'>" + str(formation_session.training_site)
                          + "</font>" + "<br/>" + "<br/>" +
                          "<font color='black'><u><b>Stagiaire (NOM, PRENOM et signature)</b></u></font>",
                          textrightstyle)

    res = Table([
        [textleft, textright]
    ],
        widthList,
        height)

    res.setStyle([

        ('BOTTOMPADDING', (1, 0), (1, 0), 0.24 * height),
        ('BOTTOMPADDING', (0, 0), (0, 0), 0.34 * height),
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (1, 0), (1, 0), 0.1 * widthList[1]),

    ])
    return res


def _genContenuFirst(width, height):
    textstyle = ParagraphStyle('textfirst')

    textstyle.fontSize = 9

    textfirst = Paragraph("<u><b>(Supprimer cette phrase et personnaliser le nombre de questions et réponses selon"
                          " votre formation)</b></u>", textstyle)

    res = Table([

        [textfirst],

    ],
        width,
        height,
    )

    res.setStyle([

        ('ALIGN', (0, 1), (0, 1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (0, 0), 0.4 * height),
        ('VALIGN', (0, 1), (0, 1), 'MIDDLE')

    ])
    return res


def _genContenuSecond(width, height):
    heightList = [
        height * 0.5,
        height * 0.5,

    ]
    textstyle = ParagraphStyle('textfirst')

    textstyle.fontSize = 12

    textfirst = Paragraph("<u><b>(Supprimer cette phrase et personnaliser le nombre de questions et réponses selon"
                          " votre formation)</b></u>", textstyle)


    res = Table([

        [''],
        [''],

    ],
        width,
        heightList,
    )

    res.setStyle([
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0.05 * height),
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    return res


def genQcmPrerequisMillFormaSecond(width, height):
    widthList = [
        width * 0.1,
        width * 0.4,
        width * 0.4,
        width * 0.1,
    ]

    res = Table([

        ['', _genContenuMainLeft(widthList[1], height), _genContenuMainRight(widthList[1], height),
         ''],

    ],
        colWidths=widthList,
        rowHeights=height)
    res.setStyle([
        ('INNERGRID', (1, 0), (2, -1), 1, colors.black),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),

    ])
    return res


def _genContenuMainLeft(width, height):
    heightList = [
        height * 0.25,
        height * 0.25,
        height * 0.25,
        height * 0.25,
    ]
    textstyle = ParagraphStyle('textfirst')

    textstyle.fontSize = 12

    textstyle.fontSize = 12


    res = Table([
        "",
        "",
        "",
        "",

    ],
        width,
        heightList,
    )

    res.setStyle([
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0.05 * height),
        ('LEFTPADDING', (1, 0), (1, 0), 0.15 * width),
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    return res


def _genContenuMainRight(width, height):
    heightList = [
        height * 0.25,
        height * 0.25,
        height * 0.25,
        height * 0.25,
    ]
    textstyle = ParagraphStyle('textfirst')

    textstyle.fontSize = 12
    list_answ = []
    textstyle.fontSize = 12


    res = Table([
        "",
        "",
        "",
        "",

    ],
        width,
        heightList,
    )

    res.setStyle([
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0.05 * height),
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),

    ])
    return res
