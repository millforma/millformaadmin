from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Table, Paragraph, Image
from main.models.formationsession import FormationSession


def genConvocation(width, height, trainee, formation_id):
    widthList = [
        width * 0.1,
        width * 0.8,
        width * 0.1,
    ]
    heightList = [
        height * 0.07,
        height * 0.116,
        height * 0.116,
        height * 0.209,
        height * 0.186,
        height * 0.229,
        height * 0.094,

    ]

    res = Table([

        ['', _genTitreFirst(widthList[1], heightList[0]), ''],
        ['', _genContenuFirst(widthList[1], heightList[1], trainee), ''],
        ['', _genTitreSecond(widthList[1], heightList[2], formation_id), ''],
        ['', _genTableFirst(widthList[1], heightList[3], formation_id), ''],
        ['', _genContenuSecond(widthList[1], heightList[4]), ''],
        ['', _genContenuThird(widthList[1], heightList[5]), ''],
        ['', _genSignature(widthList[1], heightList[6]), ''],

    ],
        colWidths=widthList,
        rowHeights=heightList)
    res.setStyle([

        ('LEFTPADDING', (1, 3), (1, 3), 0.15 * widthList[1]),
        ('BOTTOMPADDING', (1, 1), (1, 1), 0.1 * heightList[1]),
        ('BOTTOMPADDING', (1, 2), (1, 2), 0.4 * heightList[1]),
        ('BOTTOMPADDING', (1, 3), (1, 3), 0.25 * heightList[1]),

    ])
    return res


def _genTitreFirst(width, height):
    textstyle = ParagraphStyle('text')
    textstyle.fontSize = 13
    textstyle.textColor = colors.HexColor('#FFFFFF')

    text = Paragraph("<para alignment='center'><b>CONVOCATION</b></para>", textstyle)
    res = Table([
        [text]
    ],
        width,
        height,
    )
    bluecolor = colors.HexColor('#215768')
    res.setStyle([

        ('BACKGROUND', (0, 0), (-1, -1), bluecolor),
        ('VALIGN', (0, 0), (0, 0), 'MIDDLE')

    ])
    return res


def _genTitreSecond(width, height, formation_id):
    textwhitestyle = ParagraphStyle('textwhite')
    textwhitestyle.fontSize = 13
    textwhitestyle.fontColor = colors.HexColor('#FFFFFF')
    textwhitestyle.alignment = TA_CENTER
    formation_session = FormationSession.objects.get(id=formation_id)

    textfirst = Paragraph("<font color='white'><b>FORMATION :</b></font>" + "<br/>" + formation_session.name,
                          textwhitestyle)
    res = Table([
        [textfirst],

    ],
        width,
        height,
    )
    bluecolor = colors.HexColor('#215768')
    res.setStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 0), (0, 0), bluecolor),

        ('VALIGN', (0, 0), (0, 0), 'MIDDLE')

    ])
    return res


def _genContenuFirst(width, height, trainee):
    textstyle = ParagraphStyle('textfirst')
    textstyle.fontSize = 12

    textfirst = Paragraph("Le 16/08/2021," + "<br/>" + "À l’attention de : " + trainee.user.first_name +
                          trainee.user.last_name,
                          textstyle)

    res = Table([

        [textfirst],

    ],
        width,
        height * 0.5,
    )

    res.setStyle([

        ('ALIGN', (0, 1), (0, 1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (0, 0), 0.4 * height),
        ('VALIGN', (0, 1), (0, 1), 'MIDDLE')

    ])
    return res


def _genContenuSecond(width, height):
    widthList = [
        width * 0.2,
        width * 0.8,
    ]
    heightList = [
        height * 0.5,
        height * 0.5,
    ]

    textrightstyle = ParagraphStyle('textright')
    textrightstyle.fontSize = 12

    textright = Paragraph("Itinéraires par les transports en commun : " + "<br/>" + "<br/>" +
                          "<font color='blue'><link href='https://www.ratp.fr/itineraires'>"
                          "https://www.ratp.fr/itineraires</link></font>" + "<br/>",
                          textrightstyle)
    textrighttwo = Paragraph("Règlement intérieur de formation : " + "<br/>" + "<br/>" +
                             "<font color='blue'><link href='https://mill-forma.fr/wp-content/uploads/2021/06/"
                             "Reglement-interieur-stagiaires.pdf'>https://www.ratp.fr/itineraires</link></font>",
                             textrightstyle)
    lefttopImgPath = "https://mill-forma.fr/wp-content/uploads/2021/10/ratp.png"
    lefttopImgWidth = width * 0.2
    lefttop = Image(
        lefttopImgPath, lefttopImgWidth, height * 0.5, kind='proportional')
    leftbottomImgPath = "https://mill-forma.fr/wp-content/uploads/2021/10/reglement.png"
    leftbottomImgwidth = width * 0.2
    leftbottom = Image(
        leftbottomImgPath, leftbottomImgwidth, height * 0.5, kind='proportional')
    res = Table([
        [lefttop, textright],
        [leftbottom, textrighttwo],
    ],
        widthList,
        heightList)

    res.setStyle([
        ('BOTTOMPADDING', (1, 0), (1, 1), 0.3 * heightList[1]),

    ])
    return res


def _genContenuThird(width, height):
    textstyle = ParagraphStyle('text')
    textstyle.fontSize = 12
    text = Paragraph(
        "<br/>" + "<br/>" + """Horaires réglementaires : De 08H30 à 12H30 et de 13H30 à 17H30""" + "<br/>" + "<br/>" +
        """Objectifs pédagogiques et opérationnels de la formation : voir programme""" + "<br/>" + "<br/>" +
        """Vous serez accueillis par votre formateur.""" + "<br/>" + "<br/>" +
        """Vous pouvez nous contacter au <b>06 59 02 02 02</b> si vous souhaitez des informations supplémentaires."""
        + "<br/>" + "<br/>" +
        """Nous vous souhaitons une bonne et agréable formation."""
        ,
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


def _genTableFirst(width, height, formation_id):
    widthList = [
        width * 0.7,

    ]
    heightList = [
        height * 0.25,
        height * 0.75,
    ]
    formation_session = FormationSession.objects.get(id=formation_id)
    titlestyle = ParagraphStyle('titleleft')
    titlestyle.fontSize = 13

    title = Paragraph("<para alignment='center'>Détails de la formation</para>",
                      titlestyle)
    text = Paragraph("<b>Adresse : </b>" + str(formation_session.training_site) + "<br/>" + "<br/>" + "<br/>" +
                     "Date de début de la formation : " + str(formation_session.date_start) + "<br/>" + "<br/>" +
                     "<b>Horaire du premier jour :</b>" + " Vu avec le formateur",
                     titlestyle)
    res = Table([

        [title],
        [text],
    ],
        widthList[0],
        heightList,
    )

    res.setStyle([

        ('GRID', (0, 0), (-1, -1), 1, 'black'),
        ('BACKGROUND', (0, 0), (0, 0), 'grey'),
        ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 1), (0, 1), 0.15 * heightList[1]),

    ])
    return res


def _genSignature(width, height):
    widthList = [
        width * 0.5,
        width * 0.5,
    ]

    textrightstyle = ParagraphStyle('textright')
    textrightstyle.fontSize = 7.1

    textright = Paragraph("MILL-FORMA" + "<br/>"
                          + "William Berdugo" + "<br/>",
                          textrightstyle)
    rightImgPath = 'https://mill-forma.fr/wp-content/uploads/2021/10/si_ca.png'
    rightImgWidth = widthList[1]
    signature = Image(
        rightImgPath, rightImgWidth, height, kind='proportional')
    res = Table([
        ['', textright, signature]
    ],
        widthList,
        height)

    res.setStyle([

        ('RIGHTPADDING', (0, 0), (0, -1), 0.3 * width),
        ('LEFTPADDING', (1, 0), (1, -1), 0.3 * width),
        ('LEFTPADDING', (2, 0), (2, 0), -0.75 * widthList[1]),
        ('BOTTOMPADDING', (2, 0), (2, 0), -0.4 * height),
        ('BOTTOMPADDING', (1, 0), (1, -1), 0.15 * height),

    ])
    return res
