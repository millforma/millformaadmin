from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Table, Paragraph
from main.models.formationsession import FormationSession


def genCompteRenduFormation(width, height, formation_id):
    widthList = [
        width * 0.1,
        width * 0.8,
        width * 0.1,
    ]
    heightList = [
        height * 0.065,
        height * 0.87,
        height * 0.065,
    ]

    res = Table([

        ['', _genTitre(widthList[1], heightList[0]), ''],
        ['', _genContenu(widthList[1], heightList[1], formation_id), ''],
        ['', _genSignature(widthList[1], heightList[1]), ''],

    ],
        colWidths=widthList,
        rowHeights=heightList)
    res.setStyle([

        ('ALIGN', (1, 0), (1, 0), 'CENTER'),

    ])
    return res


def _genTitre(width, height):
    textstyle = ParagraphStyle('text')
    textstyle.fontSize = 13

    text = Paragraph("<b><u>COMPTE-RENDU DE FORMATION</u></b>",
                     textstyle)
    res = Table([
        [text]
    ],
        0.47 * width,
    )

    res.setStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), height * 0.4),

    ])
    return res


def _genContenu(width, height, formation_id):
    formation_session = FormationSession.objects.get(id=formation_id)
    textstyle = ParagraphStyle('textleft')
    textstyle.fontSize = 9
    if formation_session.date_start != None:
        formation_session_date_start=formation_session.date_start.strftime('%Y-%m-%d')
    else:
        formation_session_date_start="Non renseignée"
    if formation_session.date_end != None:
        formation_session_date_end=formation_session.date_end.strftime('%Y-%m-%d')
    else:
        formation_session_date_end="Non renseignée"
    textleft = Paragraph(
        "Intitulé de la formation : " + formation_session.name + "<br/>"
        + "Nom du formateur : " + formation_session.teacher_name.last_name + " " +
        formation_session.teacher_name.first_name + "<br/>"
        + "Nombre de participants prévus : " + str(formation_session.trainee.count()) + "<br/>"
        + "Dates de formations : " + formation_session_date_start +
        " au " + formation_session_date_end + "<br/>"
        + "Nombre de participants présents : " + str(formation_session.num_present_trainee) + "<br/>"
        + "Durée de la formation : " + str(formation_session.training_duration) + "H" + "<br/>" + "<br/>"
        ,
        textstyle)

    textfullwidthstyle = ParagraphStyle('textright')
    textfullwidthstyle.fontSize = 11
    textright = Paragraph("<b>Profil des participants :</b>" + "<br/>" + "<br/>" + "<br/>"
                          + "---------------------------------------------------------------------------------------"
                          + "<br/>"
                          + "---------------------------------------------------------------------------------------"
                          + "<br/>" + "<br/>" + "<br/>"
                          + "<b>Méthodologie et déroulement de la formation :</b>" + "<br/>" + "<br/>" + "<br/>"
                          + "---------------------------------------------------------------------------------------"
                          + "<br/>"
                          + "---------------------------------------------------------------------------------------"
                          + "<br/>"
                          + "---------------------------------------------------------------------------------------"
                          + "<br/>" + "<br/>" + "<br/>"
                          + "<b>Comportement des participants </b>" + "(1 étant la plus mauvaise note):" + "<br/>"
                          + "<br/>" + "<br/>"
                          + "- Motivation : 1 - 2 - 3 – 4 " + "<br/>" + "<br/>"
                          + "- Assiduité : 1 - 2 – 3 – 4 " + "<br/>" + "<br/>"
                          + "- Participation : 1 - 2 – 3 – 4" + "<br/>" + "<br/>" + "<br/>" + "<br/>"
                          + "<b>Le groupe était-il de niveau homogène ? </b>" + "<br/>" + "<br/>"
                          + "OUI &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + "NON" + "<br/>" + "<br/>"
                          + "Autres observations :" + "<br/>" + "<br/>"
                          + "---------------------------------------------------------------------------------------"
                          + "<br/>"
                          + "---------------------------------------------------------------------------------------"
                          + "<br/>"
                          + "---------------------------------------------------------------------------------------"
                          + "<br/>" + "<br/>" + "<br/>",
                          textfullwidthstyle)

    res = Table([

        [textleft],
        [textright],
    ],
        width,
    )

    res.setStyle([

        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),

    ])
    return res


def _genSignature(width, height):
    widthList = [
        width * 0.5,
        width * 0.5,
    ]

    textrightstyle = ParagraphStyle('textright')
    textrightstyle.fontSize = 12

    textright = Paragraph("<u><b>Signature Formateur</b></u>",
                          textrightstyle)

    res = Table([
        ['', textright, ]
    ],
        widthList,
        height)

    res.setStyle([

        ('LEFTPADDING', (1, 0), (1, -1), 0.1 * width),

        ('BOTTOMPADDING', (1, 0), (1, -1), 0.05 * height),

    ])
    return res
