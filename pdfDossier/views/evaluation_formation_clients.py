import io
import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.platypus import Table



def genEvaluationFormationClients(width, height):
    widthList = [
        width * 0.1,
        width * 0.8,
        width * 0.1,
    ]
    heightList = [
        height * 0.1126,
        height * 0.0713,
        height * 0.359,
        height * 0.0713,
        height * 0.3958,
    ]

    res = Table([
        ['', _genTitre(widthList[1], heightList[0]), ''],
        ['', _genContenuFirst(widthList[1], heightList[1]), ''],
        ['', _genTableau(widthList[1], heightList[2]), ''],
        ['', _genContenuSecond(widthList[1], heightList[3]), ''],
        ['', _genContenuThird(widthList[1], heightList[4]), ''],
    ],
        colWidths=widthList,
        rowHeights=heightList)
    res.setStyle([

        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('BOTTOMPADDING', (1, 1), (1, 1), heightList[1]*0.4),
        ('BOTTOMPADDING', (1, 3), (1, 3), heightList[3] * 0.4),

    ])
    return res


def _genTitre(width, height):

    textstyle = ParagraphStyle('text')
    textstyle.fontSize=16
    textstyle.leading = 16


    text = Paragraph("<para alignment='center'>EVALUATION DE LA FORMATION PAR LES ORGANISMES CLIENTS</para>",
                          textstyle)
    res = Table([
        [text]
    ],
        width,
    )

    res.setStyle([
        ('ALIGN', (0, 1), (0, 1), 'CENTER'),

        ('GRID', (0, 0), (-1, -1), 1, 'black'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0.2* height),
    ])
    return res

def _genContenuFirst(width, height):

    textstyle = ParagraphStyle('textfirst')

    textstyle.fontSize = 12

    textfirst = Paragraph("<b>Organisme: </b>",textstyle)

    res = Table([

        [textfirst],

    ],
        width,
        height,
       )

    res.setStyle([


    ])
    return res

def _genContenuSecond(width, height):
    textstyle = ParagraphStyle('textsecond')
    textstyle.fontSize = 12

    textsecond = Paragraph("Vos suggestions d’améliorations ou autres commentaires :" + "<br/>",
                          textstyle)

    res = Table([
        [textsecond],
    ],
        width,
        height)

    res.setStyle([


    ])
    return res

def _genTableau(width, height):
    widthList = [
        width * 0.8,
        width * 0.2,


    ]
    heightList = [
        height * 0.11,
        height * 0.11,
        height * 0.11,
        height * 0.11,
        height * 0.11,
        height * 0.11,
        height * 0.11,
        height * 0.11,
        height * 0.12,
    ]
    textstyle = ParagraphStyle('text')


    textstyle.fontSize = 9

    textzeroleft = Paragraph("<b>Quelle est votre appréciation sur :</b>",textstyle)
    textzerofour = Paragraph("Note sur 5",textstyle)

    textoneleft = Paragraph("La disponibilité et clarté de l’offre",textstyle)
    textoneright = Paragraph("", textstyle)

    texttwoleft = Paragraph("Les formalités d’inscription",textstyle)
    texttworight = Paragraph("", textstyle)

    textthreeleft = Paragraph("Les informations transmises préalablement à la formation",textstyle)
    textthreeright = Paragraph("", textstyle)

    textfourleft = Paragraph("Le respect des éléments contractuels",textstyle)
    textfourright = Paragraph("", textstyle)

    textfiveleft = Paragraph("L’utilité de la formation dans le développement de la compétence des stagiaires"
                             ,textstyle)
    textfiveright = Paragraph("", textstyle)

    textsixleft = Paragraph("La cohérence de la formation par rapport aux attentes",textstyle)
    textsixright = Paragraph("", textstyle)

    textsevenleft = Paragraph("La qualité de l’animation",textstyle)
    textsevenright = Paragraph("", textstyle)

    texteightleft = Paragraph("Les informations figurant sur la convention",textstyle)
    texteightright = Paragraph("", textstyle)


    res = Table([
        [textzeroleft,textzerofour],
        [textoneleft,textoneright],
        [texttwoleft,texttworight],
        [textthreeleft,textthreeright],
        [textfourleft,textfourright],
        [textfiveleft,textfiveright],
        [textsixleft,textsixright],
        [textsevenleft,textsevenright],
        [texteightleft,texteightright],
    ],
        widthList,
        heightList)

    res.setStyle([

        ('GRID', (0, 0), (-1, -1), 1 , 'black'),

        #('LEFTPADDING', (1, 0), (4, 0), 0.45 * widthList[1]),
        ('VALIGN', (0, 0), (4, 0), 'MIDDLE')


    ])
    return res

def _genContenuThird(width, height):

    res = Table([

        [''],

    ],
        width,
        height
       )

    res.setStyle([
        ('GRID',(0, 0),(-1, -1),1,'black'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),


    ])
    return res

