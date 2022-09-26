from django.contrib.auth.models import User
from reportlab.platypus import  Paragraph
from reportlab.lib.styles import ParagraphStyle
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table
from main.models.formationsession import FormationSession
from pdfDossier.views.footer import genFooterTable
from pdfDossier.views.header import genHeaderTable



def Generate_Qcm_Chaud_view(request, formation_id , trainee):
    width, height = A4
    files = []


    formation_session = FormationSession.objects.get(id=formation_id)




    buffer = io.BytesIO()
    ques_satisfaction_chaud = canvas.Canvas(buffer, pagesize=A4)
    ques_satisfaction_chaud.setTitle('Questionnaire de satisfaction à chaud')

    heightList_multiple_page = [height * 0.14,
                                height * 0.735,
                                height * 0.125,
                                ]

    quessatisfactionchaud = Table([
        [genHeaderTable(width, heightList_multiple_page[0])],
        [genQuesSatisfactionChaud(width, heightList_multiple_page[1], formation_id,trainee)],
        [genFooterTable(width, heightList_multiple_page[2])],
    ],
        colWidths=width,
        rowHeights=heightList_multiple_page
    )

    quessatisfactionchaud.setStyle([

        ('LEFTPADDING', (1, 1), (0, 2), 0.1475 * width),

    ])



    return quessatisfactionchaud


def genQuesSatisfactionChaud(width, height, formation_id,trainee):
    widthList = [
        width * 0.1,
        width * 0.8,
        width * 0.1,
    ]
    heightList = [
        height * 0.0525,
        height * 0.037,
        height * 0.21,
        height * 0.079,
        height * 0.263,
        height * 0.184,
        height * 0.1745,
    ]

    res = Table([

        ['', _genTitre(widthList[1], heightList[0]), ''],
        ['', _genRefAction(widthList[1], heightList[1]), ''],
        ['', _genTableauFirst(widthList[1], heightList[2], formation_id, trainee), ''],
        ['', _genTexteEntreDeux(widthList[1], heightList[3]), ''],
        ['', _genTableauSecond(widthList[1], heightList[4]), ''],
        ['', _genQuest(widthList[1], heightList[5]), ''],
        ['', _genTableauThird(widthList[1], heightList[6]), ''],
    ],
        colWidths=widthList,
        rowHeights=heightList)
    res.setStyle([

        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
    ])
    return res


def _genTitre(width, height):
    textstyle = ParagraphStyle('text')
    textstyle.fontSize = 12

    text = Paragraph("<para alignment='center'><b>Questionnaire de Satisfaction Client à Chaud</b></para>",
                     textstyle)
    res = Table([
        [text]
    ],
        width,
    )

    res.setStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, 'black'),
    ])
    return res


def _genRefAction(width, height):
    textstyle = ParagraphStyle('text')
    textstyle.fontSize = 11

    text = Paragraph("<b>Référence de l’action :</b>",
                     textstyle)
    res = Table([
        [text]
    ],
        width,
        height
    )

    res.setStyle([
    ])
    return res


def _genTableauFirst(width, height, formation_id,trainee):
    heightList = [
        height * 0.16,
        height * 0.16,
        height * 0.16,
        height * 0.16,
        height * 0.16,
        height * 0.16,
    ]
    textstyle = ParagraphStyle('text')
    formation_session = FormationSession.objects.get(id=formation_id)
    textstyle.fontSize = 9

    textzero = Paragraph("Intitulé de la formation :" + "<b><font color='black'>" +
                         formation_session.name + "</font></b>", textstyle)
    textone = Paragraph("Date :" + "<b><font color='black'>" + str(formation_session.date_start) + "</font></b>" +
                        "<font color='black'><b> au </b></font>" + "<b><font color='black'>" +
                        str(formation_session.date_end) + "</font></b>", textstyle)
    texttwo = Paragraph("Durée jours/heures :" + "<b><font color='black'>" + str(formation_session.training_duration)
                        + "</font></b>", textstyle)
    textthree = Paragraph("Lieu de la formation :" + "<b><font color='black'>" + str(formation_session.training_site)
                          + "</font></b>", textstyle)
    textfour = Paragraph("Nom/prénom des intervenants :" + "<b><font color='black'>" +
                         formation_session.teacher_name.last_name + " " + formation_session.teacher_name.first_name
                         + "</font></b>", textstyle)
    textfive = Paragraph("Nom/prénom du participant :" + "<b><font color='black'>" + str(trainee.last_name)+" "
                         +str(trainee.first_name) + "</font></b>", textstyle)

    res = Table([
        [textzero],
        [textone],
        [texttwo],
        [textthree],
        [textfour],
        [textfive],

    ],
        width,
        heightList)

    res.setStyle([

        ('GRID', (0, 0), (-1, -1), 1, 'black'),

    ])
    return res


def _genTexteEntreDeux(width, height):
    textstyle = ParagraphStyle('text')
    textstyle.fontSize = 9
    text = Paragraph(
        """Nous allons vous proposer quelques questions qui ont pour objet de mesurer la pertinence et la qualité de
         la formation que vous avez suivi ainsi que l’impact qui en a résulté.""" + "<br/>" +
        """<i>Cocher la case qui correspond à votre niveau de satisfaction</i>""",
        textstyle)
    res = Table([
        [text]
    ],
        width,
        height
    )

    res.setStyle([

    ])
    return res


def _genTableauSecond(width, height):
    widthList = [
        width * 0.6,
        width * 0.2,


    ]
    heightList = [
        height * 0.2,
        height * 0.16,
        height * 0.16,
        height * 0.16,
        height * 0.16,
        height * 0.16,
    ]
    textstyle = ParagraphStyle('text')
    textstyle.fontSize = 9

    textzeroleft = Paragraph("<b>Questions :</b>", textstyle)
    textzeroone = Paragraph("Note sur 5", textstyle)
    textoneleft = Paragraph("<b>1. Informations transmises avant la formation</b>", textstyle)


    texttwoleft = Paragraph("<b>2. Cohérence entre les objectifs et la formation</b>", textstyle)


    textthreeleft = Paragraph("<b>3. Cohérence entre vos attentes et la formation</b>", textstyle)


    textfourleft = Paragraph("<b>4. Les moyens pédagogiques</b>", textstyle)


    textfiveleft = Paragraph("<b>5. La pédagogie du formateur</b>", textstyle)


    res = Table([
        [textzeroleft,  textzeroone],
        [textoneleft],
        [texttwoleft],
        [textthreeleft],
        [textfourleft],
        [textfiveleft],

    ],
        widthList,
        heightList)

    res.setStyle([

        ('GRID', (0, 0), (-1, -1), 1, 'black'),

        ('LEFTPADDING', (1, 0), (4, 0), 0.45 * widthList[1]),
        ('VALIGN', (0, 0), (4, 0), 'MIDDLE')

    ])
    return res


def _genQuest(width, height):
    textstyle = ParagraphStyle('text')

    textstyle.fontSize = 9

    text = Paragraph(
            "<b> Niveau de satisfaction général sur 10.</b>" + "<br/>",
        textstyle)
    res = Table([

        [text],

    ],
        width,
    )

    res.setStyle([

        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),

    ])
    return res


def _genTableauThird(width, height):
    widthList = [
        width * 0.1,
        width * 0.1,
        width * 0.1,
        width * 0.1,
        width * 0.1,
        width * 0.1,
        width * 0.1,
        width * 0.1,
        width * 0.1,
        width * 0.1,
    ]
    heightList = [
        height * 0.3,
        height * 0.4,

    ]
    textstyle = ParagraphStyle('text')

    textstyle.fontSize = 9

    textzeroleft = Paragraph("<para alignment='center'><b>10</b></para>", textstyle)
    textoneleft = Paragraph("",textstyle)

    textzeroone = Paragraph("<para alignment='center'><b>9</b></para>", textstyle)
    textoneone = Paragraph("",textstyle)


    textzerotwo = Paragraph("<para alignment='center'><b>8</b></para>", textstyle)
    textonetwo = Paragraph("",textstyle)


    textzerothree = Paragraph("<para alignment='center'><b>7</b></para>", textstyle)
    textonethree = Paragraph("",textstyle)


    textzerofour = Paragraph("<para alignment='center'><b>6</b></para>", textstyle)
    textonefour = Paragraph("",textstyle)


    textzerofive = Paragraph("<para alignment='center'><b>5</b></para>", textstyle)
    textonefive = Paragraph("",textstyle)


    textzerosix = Paragraph("<para alignment='center'><b>4</b></para>", textstyle)
    textonesix = Paragraph("",textstyle)


    textzeroseven = Paragraph("<para alignment='center'><b>3</b></para>", textstyle)
    textoneseven = Paragraph("",textstyle)


    textzeroeight = Paragraph("<para alignment='center'><b>2</b></para>", textstyle)
    textoneeight = Paragraph("",textstyle)


    textzeronine = Paragraph("<para alignment='center'><b>1</b></para>", textstyle)
    textonenine = Paragraph("",textstyle)


    res = Table([
        [textzeroleft, textzeroone, textzerotwo, textzerothree, textzerofour, textzerofive, textzerosix, textzeroseven,
         textzeroeight, textzeronine],
        [textoneleft, textoneone, textonetwo, textonethree,textonefour, textonefive, textonesix, textoneseven,
         textoneeight, textonenine]

    ],
        widthList,
        heightList)

    res.setStyle([

        ('GRID', (0, 0), (-1, -1), 1, 'black'),

        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),


    ])
    return res
