from reportlab.platypus import Table, Paragraph, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from main.models.company import Company
from main.models.formationsession import FormationSession
from signature.models import SignatureModel


def genEmargementFirst(width, height, formation_id, day, event):
    widthList = [
        width * 0.1,
        width * 0.8,
        width * 0.1,
    ]
    heightList = [
        height * 0.0417,
        height * 0.1875,
        height * 0.07,
        height * 0.106,
        height * 0.336,
        height * 0.1666,
    ]

    res = Table([
        ['', _genTitle(widthList[1], heightList[0]), ''],
        ['', _genDescription(widthList[1], heightList[1], formation_id), ''],
        ['', _genTitleDate(widthList[1], heightList[2], formation_id, day), ''],
        ['', _genTableTitle(widthList[1], heightList[3], event), ''],
        ['', _genTableContent(widthList[1], heightList[4], formation_id), ''],
        ['', _genSignature(widthList[1], heightList[5],formation_id), ''],
    ],
        colWidths=widthList,
        rowHeights=heightList)

    res.setStyle([
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('BOTTOMPADDING', (1, 4), (1, 4), -0.028 * height),
        ('BOTTOMPADDING', (1, 3), (1, 3), -0.03 * height),
        ('ALIGN', (1, 2), (1, 2), 'CENTER'),
    ])
    return res


def _genDescription(width, height, formation_id):
    widthList = [
        width * 0.5,
        width * 0.5,
    ]

    textleftstyle = ParagraphStyle('textleft')
    textleftstyle.textColor = colors.HexColor('#808080')
    textleftstyle.fontSize = 8
    formation_session = FormationSession.objects.get(id=formation_id)
    client_company = formation_session.client_account
    millforma = Company.objects.get(name="Mill Forma")
    if client_company.adresse != None:
        client_company_address = client_company.adresse.string()
    else:
        client_company_address = "Non renseignée"

    textleft = Paragraph("<font color='black'><b><u>L'ORGANISME DE FORMATION</u></b></font>" + "<br/>"
                         + "Raison Sociale :" + "<font color='black'>" + millforma.raison_sociale + "</font>" + "<br/>"
                         + "Numéro de déclaration d'activité :" + "<font color='black'>" + millforma.num_decla_activite
                         + "</font>" + "<br/>"
                         + "Siret :" + "<font color='black'>" + millforma.num_siret + "</font>" + "<br/>"
                         + "Adresse :" + "<font color='black'>" + millforma.adresse.string() + "</font>" + "<br/>"
                         + "<font color='black'><b><u>L'ENTREPRISE</u></b></font>" + "<br/>"
                         + "Raison Sociale :" + "<font color='black'>" + client_company.raison_sociale + "</font>"
                         + "<br/>"
                         + "Siret :" + "<font color='black'>" + client_company.num_siret + "</font>" + "<br/>"
                         + "Adresse : " + "<font color='black'>" + client_company_address + "</font>" + "<br/>"
                         ,
                         textleftstyle)

    textrightstyle = ParagraphStyle('textright')
    textrightstyle.fontSize = 8
    textrightstyle.textColor = colors.HexColor('#808080')
    textright = Paragraph(
        "Référence OPCO : " + "<font color='black'>" + formation_session.old_num_formation + "</font>" + "<br/>"
        + "Intitulé de la formation : " + "<font color='black'>" + formation_session.name + "</font>" + "<br/>"
        + "Date de la session : " + "<font color='black'>" + formation_session.date_start.strftime(
            '%Y-%m-%d') + "</font>" + " au " + "<font color='black'>" + formation_session.date_autorised_end.strftime(
            '%Y-%m-%d') + "</font>" + "<br/>"
        + "Lieu de la formation : " + "<font color='black'>" + str(
            formation_session.training_site) + "</font>" + "<br/>" +
        "Nom du formateur : " + "<font color='black'>" + formation_session.teacher_name.last_name + " " +
        formation_session.teacher_name.first_name + "</font>",
        textrightstyle)

    res = Table([
        [textleft, textright]
    ],
        widthList,
        height)

    res.setStyle([

        ('BOTTOMPADDING', (1, 0), (1, 0), 0.35 * height),
        # ('BOTTOMPADDING', (0, 0), (0, 0), 0.34 * height),
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
        # ('LEFTPADDING', (1, 0), (1, 0), 0.1 * widthList[1]),

    ])
    return res


def _genTitle(width, height):
    textstyle = ParagraphStyle('text')
    textstyle.fontSize = 17
    textstyle.leading = 17

    text = Paragraph("<para alignment='center'>FEUILLE(S) D’ÉMARGEMENT</para>",
                     textstyle)
    res = Table([
        [text]
    ],
        width,
    )

    res.setStyle([
        ('ALIGN', (0, 1), (0, 1), 'CENTER'),

        ('GRID', (0, 0), (-1, -1), 1, 'black'),
        # ('BOTTOMPADDING', (0, 0), (-1, -1), 0.2* height),
    ])
    return res


def _genTitleDate(width, height, formation_id, day):
    textstyle = ParagraphStyle('text')
    textstyle.fontSize = 17
    textstyle.leading = 17
    formation_session = FormationSession.objects.get(id=formation_id)

    text = Paragraph("<para alignment='center'>Le :  " + day.strftime('%d-%m-%Y') + "</para>",
                     textstyle)
    res = Table([
        [text]
    ],
        width * 0.5,
    )

    res.setStyle([
        ('ALIGN', (0, 1), (0, 1), 'CENTER'),

        ('GRID', (0, 0), (-1, -1), 1, 'black'),
        # ('BOTTOMPADDING', (0, 0), (-1, -1), 0.2* height),
    ])
    return res


def _genTableTitle(width, height, event):
    widthList = [
        width * 0.222,
        width * 0.389,
        width * 0.389,
    ]

    textstyle = ParagraphStyle('text')

    textstyle.fontSize = 9
    delta = event.end_time - event.start_time
    numb_hours = delta
    textzeroleft = Paragraph("<b>Nom/Prénom</b>" + "<br/>" + "stagiaire", textstyle)
    textzerotwo = Paragraph(
        "<b>Début</b>" + "<br/>" + "<br/>" + "Horaires : " + str(event.start_time) + "<br/>" + "<br/>",
        textstyle)
    textzeroone = Paragraph(
        "<b>Fin</b>" + "<br/>" + "<br/>" + "Horaires : " + str(event.end_time) + "<br/>" + "<br/>"
        + "Nombre d'heures : " + str(numb_hours),
        textstyle)
    # textoneleft = Paragraph("<b>Signature Stagiaire</b>", textstyle)

    res = Table([
        [textzeroleft, textzerotwo, textzeroone],
    ],
        widthList,
        height,
    )

    res.setStyle([
        ('GRID', (0, 0), (-1, -1), 1, 'black'),
        ('VALIGN', (0, 0), (4, 0), 'MIDDLE'),

    ])
    return res


def _genTableContent(width, height, formation_id):
    widthList = [
        width * 0.222,
        width * 0.389,
        width * 0.389,
    ]

    formation_session = FormationSession.objects.get(id=formation_id)
    number_of_trainee = formation_session.trainee.count()
    heightList = [1 / number_of_trainee * height for i in range(number_of_trainee)]

    data = [[None for j in range(3)] for i in range(number_of_trainee)]
    i = 0
    # for trainee in formation_session.trainee.all():
    #    columnData = str(trainee.user.first_name + " " + trainee.user.last_name)
    #    data[i][0] = columnData
    #    i += 1

    res = Table(data,
                widthList,
                heightList,
                )

    res.setStyle([
        ('GRID', (0, 0), (-1, -1), 1, 'black'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

    ])
    return res


def _genSignature(width, height, formation_id):
    widthList = [
        width * 0.5,
        width * 0.5,
    ]

    formation = FormationSession.objects.get(id=formation_id)
    teacher = formation.teacher_name



    textrightstyle = ParagraphStyle('textright')
    textrightstyle.fontSize = 7.1

    textright = Paragraph("MILL-FORMA" + "<br/>"
                          + "William Berdugo" + "<br/>",
                          textrightstyle)

    rightImgPath = 'https://mill-forma.fr/wp-content/uploads/2021/10/si_ca.png'
    rightImgWidth = widthList[1] * 0.5

    textleft = Paragraph("Le formateur" + "<br/>"
                         + str(teacher.last_name) +" "+ str(teacher.first_name)+ "<br/>",
                         textrightstyle)

    signature = Image(
        rightImgPath, rightImgWidth, height, kind='proportional')

    signature_teacher = SignatureModel.objects.get(signature_owner=teacher)
    signature_formateur = Image(
        signature_teacher.signature, rightImgWidth, height, kind='proportional')

    res = Table([
        [signature_formateur, textright, signature]
    ],
        widthList,
        height)

    res.setStyle([

        ('RIGHTPADDING', (0, 0), (0, -1), 0.3 * width),
        ('LEFTPADDING', (1, 0), (1, -1), 0.3 * width),
        ('LEFTPADDING', (2, 0), (2, 0), -0.75 * widthList[1]),
        ('BOTTOMPADDING', (1, 0), (1, -1), 0.15 * height),

    ])
    return res
