from django.utils import timezone
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Table, Paragraph, Image
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import ListFlowable, ListItem
from main.models.company import Company
from main.models.formationsession import FormationSession


def genConventionFormationFirst(width, height, formation_id):
    widthList = [
        width * 0.1,
        width * 0.8,
        width * 0.1,
    ]
    heightList = [
        height * 0.112,
        height * 0.5328,
        height * 0.3552,
    ]

    res = Table([

        ['', _genTitle(widthList[1], heightList[0]), ''],
        ['', _genEntre(widthList[1], heightList[1], formation_id), ''],
        ['', _genTableau(widthList[1], heightList[2], formation_id), ''],

    ],
        colWidths=widthList,
        rowHeights=heightList)
    res.setStyle([
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('BOTTOMPADDING', (1, 0), (1, 0), 0.35 * heightList[0]),
    ])
    return res


def _genTitle(width, height):
    textstyle = ParagraphStyle('text')
    textstyle.fontSize = 17

    textstyle.alignment = TA_CENTER

    text = Paragraph(
        "CONVENTION DE FORMATION PROFESSIONNELLE" + "<br/>" + "<br/>" +
        "(Articles L. 6353-1 à L. 6353-2 du Code du travail)",
        textstyle)
    res = Table([
        [text]
    ],
        width,
    )

    res.setStyle([

        ('BOTTOMPADDING', (0, 0), (-1, -1), 0.2 * height),
    ])
    return res


def _genEntre(width, height, formation_id):
    text1style = ParagraphStyle('texttwo')
    text1style.fontSize = 11
    text1style.leading = 15
    formation_session = FormationSession.objects.get(id=formation_id)
    client_company = formation_session.client_account
    millforma = Company.objects.get(name="Mill Forma")
    if client_company.adresse != None:
        client_company_address = client_company.adresse.string()
    else:
        client_company_address = "Non renseignée"

    text1 = Paragraph(
        "<b>Entre :</b>" + "<br/>" + "<br/>" +
        "L’organisme de formation :" + millforma.name + "<br/>"
        + "Raison Sociale :" + millforma.raison_sociale + "<br/>"
        + "Numéro de déclaration d’activité de l’organisme de formation : " + millforma.num_decla_activite + "<br/>"
        + "Numéro SIRET de l’organisme de formation : " + millforma.num_siret + "<br/>"
        + "Adresse de l’organisme de formation : " + millforma.adresse.string() + "<br/>"
        + "Code APE :  " + millforma.code_ape + "<br/>"
        + "<br/>" + "<br/>"
        + "<b>Et :</b>" + "<br/>" +
        "L’entreprise :" + client_company.name + "<br/>"
        + "Adresse de l’entreprise : " + client_company_address + "<br/>"
        + "SIRET de L’entreprise : " + client_company.num_siret + "<br/>"
        + "Code APE de L’entreprise : " + client_company.num_decla_activite + "<br/>"
        + "<br/>" + "<br/>"
        + "Pour le(s) bénéficiaire(s) : (Ci-après dénommé(s) le(s) stagiaire(s))" + "<br/>",
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


def _genTableau(width, height, formation_id):
    widthList = [
        width * 0.5,
        width * 0.5,
    ]

    formation_session = FormationSession.objects.get(id=formation_id)
    number_of_trainee = formation_session.trainee.count()
    heightList = [1 / (number_of_trainee + 1) * height for i in range(number_of_trainee + 1)]

    data = [[None for j in range(2)] for i in range(number_of_trainee + 1)]
    data[0][0] = "Stagiaire"
    data[0][1] = "Fonction"
    i = 1
    for trainee in formation_session.trainee.all():
        columnData = str(trainee.user.first_name + " " + trainee.user.last_name)
        data[i][0] = columnData
        i += 1

    res = Table(data,
                widthList,
                heightList,
                )

    res.setStyle([
        ('GRID', (0, 0), (-1, -1), 1, 'black'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

    ])
    return res


def genConventionFormationSecond(width, height, formation_id):
    widthList = [
        width * 0.1,
        width * 0.8,
        width * 0.1,
    ]

    res = Table([
        ['', _genPagetwoMain(widthList[1], height, formation_id), ''],

    ],
        colWidths=widthList, )
    res.setStyle([
        # ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('BOTTOMPADDING', (1, 0), (1, 0), 0.1 * height),

    ])
    return res


def _genPagetwoMain(width, height, formation_id):
    text1style = ParagraphStyle('text')
    text1style.fontSize = 11
    # text1style.leading = 15
    formation_session = FormationSession.objects.get(id=formation_id)
    if formation_session.date_autorised_start != None:
        formation_session_date_start = formation_session.date_autorised_start.strftime('%Y-%m-%d')
    else:
        formation_session_date_start = "Non renseignée"
    if formation_session.date_autorised_end != None:
        formation_session_date_end = formation_session.date_autorised_end.strftime('%Y-%m-%d')
    else:
        formation_session_date_end = "Non renseignée"

    client_company = formation_session.client_account
    millforma = Company.objects.get(name="Mill Forma")
    if formation_session.prerequis_formation == True:
        prerequis = "Oui"
    else:
        prerequis = "Non"

    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontSize = 11

    text1 = Paragraph(
        "<b>1 - OBJET :</b>" + "<br/>" + "<br/>" +
        "L’action de formation entre dans la catégorie : Action d'adaptation et de développement des compétences "
        "prévue à l’article L.6313-1 de la sixième partie du Code du travail. " + "<br/>" + "<br/>"
        + "En exécution de la présente convention, l’organisme de formation s’engage à organiser l’action de "
          "formation professionnelle intitulée :"
        + formation_session.name + "<br/>" + "<br/>" + "<br/>" +
        "<b>2 - NATURE ET CARACTERISTIQUES DE L’ACTION DE FORMATION :</b>" + "<br/>" + "<br/>"
        + "Action de formation concourant au développement des compétences " + "<br/>" + "La durée de la formation"
                                                                                         " est fixée à " + str(
            formation_session.training_duration) + "H" + "<br/>"
        + "Horaires de Stage :  " + "-----------------------------------------------" + "<br/>"
        + "<i>Pour les formations INTRA-ENTREPRISE, les horaires peuvent varier selon les besoins de l’entreprise."
          " La feuille d’émargement attestera des horaires réellement réalisés.</i>" + "<br/>" + "<br/>" + "<br/>"
        + "<b>Le programme détaillé de l’action de formation figure en annexe de la présente convention. </b>" +
        "<br/>" + "<br/>"
        + "<b>3 - NIVEAU DE CONNAISSANCES PREALABLES NECESSAIRE </b>" + "<br/>" + "<br/>" +
        prerequis + "<br/>" + "<br/>" +
        "<b>4 - ORGANISATION DE L’ACTION DE FORMATION</b>" + "<br/>" + "<br/>"
        + "L’action de formation aura lieu du : " + formation_session_date_end + " au " + formation_session_date_end +
        "<br/>" + "<br/>"
        + "Lieu de formation :" + str(formation_session.training_site) + "<br/>"
        + "La Formation est-elle en FOAD ? " + str(formation_session.foad) + "<br/>"
        + "Les conditions générales dans lesquelles la formation est dispensée, notamment les moyens pédagogiques"
          " et techniques, sont les suivantes :" + "<br/>" + "<br/>"
        ,
        text1style)
    text2 = ListFlowable(
        [
            ListItem(Paragraph(
                "Réflexions et travaux sur des cas pratiques",
                style), leftIndent=45),
            ListItem(Paragraph(
                "Apport théorique",
                style), leftIndent=45),
            ListItem(Paragraph(
                "Questionnaire et exercices",
                style), leftIndent=45),
            ListItem(Paragraph(
                "Tests de contrôle de connaissances à chaque étape", style),
                leftIndent=45),
            ListItem(Paragraph(
                "Retours d'expériences",
                style), leftIndent=45),
        ],
        bulletType='bullet',
        start='bulletchar',
        bulletFontSize=11,
    )

    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontSize = 11
    # style.leading = 15

    res = Table([
        [text1],
        [text2],
    ],
        width,
    )

    res.setStyle([

        # ('BOTTOMPADDING', (0, 0), (-1, -1), 0.2* height),
    ])
    return res


def genConventionFormationThird(width, height, formation_id):
    widthList = [
        width * 0.1,
        width * 0.8,
        width * 0.1,
    ]

    res = Table([

        ['', _genPagethreeMain(widthList[1], height, formation_id), ''],

    ],
        colWidths=widthList, )
    res.setStyle([
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        # ('BOTTOMPADDING', (1, 1), (1, 1), 0.6 * heightList[1]),
        # -('BOTTOMPADDING', (1, 2), (1, 2), 0.2 * heightList[1]),

    ])
    return res


def _genPagethreeMain(width, height, formation_id):
    textstyle = ParagraphStyle('texttwo')
    textstyle.fontSize = 11
    textstyle.leading = 15

    text1style = ParagraphStyle('texttwo')
    text1style.fontSize = 11
    text1style.leading = 15

    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontSize = 11
    # style.leading = 15
    formation_session = FormationSession.objects.get(id=formation_id)

    if formation_session.date_autorised_start != None:
        formation_session_date_start = formation_session.date_autorised_start.strftime('%Y-%m-%d')
    else:
        formation_session_date_start = "Non renseignée"
    if formation_session.date_autorised_end != None:
        formation_session_date_end = formation_session.date_autorised_end.strftime('%Y-%m-%d')
    else:
        formation_session_date_end = "Non renseignée"

    client_company = formation_session.client_account
    millforma = Company.objects.get(name="Mill Forma")


    text1 = Paragraph(
        "Si la formation se déroule en intra dans les locaux du client, Il est de sa responsabilité de vérifier "
        "l'accès aux besoins suivant : " + "<br/>",
        textstyle)

    textstyle = ParagraphStyle('text')
    textstyle.fontSize = 11
    textstyle.leading = 15

    text2 = ListFlowable(
        [
            ListItem(Paragraph(
                "Capacité d’accueil de la salle nécessaire pour la formation ",
                style), leftIndent=45),
            ListItem(Paragraph(
                "Disposition de la salle",
                style), leftIndent=45),
            ListItem(Paragraph(
                "Matériel nécessaire pour la formation",
                style), leftIndent=45),
            ListItem(Paragraph(
                "Autres outils et équipements nécessaires", style),
                leftIndent=45),
        ],
        bulletType='bullet',
        start='bulletchar',
        bulletFontSize=11,

    )
    text3 = Paragraph(
        "Le détail des Conditions générales de vente est disponible sur le site internet. (www.mill-forma.fr)"
        + "<br/>" +
        "La signature de cette convention vaut acceptation des CGVs." + "<br/>" + "<br/>" +
        "<b>5 - MOYENS PERMETTANT D’APPRECIER LES RESULTATS DE L’ACTION</b>" + "<br/>" ,
        textstyle)

    text4 = ListFlowable(
        [
            ListItem(Paragraph(
                "QCM",
                style), leftIndent=45),
            ListItem(Paragraph(
                "Grille d’évaluation",
                style), leftIndent=45),
            ListItem(Paragraph(
                "Travaux pratiques",
                style), leftIndent=45),
            ListItem(Paragraph(
                "Tests de contrôle de connaissances à chaque étape", style),
                leftIndent=45),
            ListItem(Paragraph(
                "Entretiens avec le formateur", style),
                leftIndent=45),
        ],
        bulletType='bullet',
        start='bulletchar',
        bulletFontSize=11,

    )
    text5 = Paragraph("<br/>" + "<br/>" + "<b>6 - SANCTION DE LA FORMATION</b>" + "<br/>" + "<br/>" +
                      "En application de l’article L.6353-1 du Code du travail, une attestation mentionnant les "
                      "objectifs, la nature et la durée de l’action et les résultats de l’évaluation des acquis de "
                      "la formation sera remise au stagiaire à l’issue de la formation." + "<br/>",
                      textstyle)
    text6 = Paragraph(
        "<b>7 - MOYENS PERMETTANT DE SUIVRE L’EXECUTION DE L’ACTION</b>" + "<br/>" + "<br/>" +
        "Feuilles de présence signées par le stagiaire et le formateur et par demi-journée de formation"
        + "<br/>" + "<br/>" +
        "<b>8 - NON REALISATION DE LA PRESTATION DE FORMATION</b>" + "<br/>" + "<br/>" +
        "En application de l’article L. 6354-1 du Code du travail, il est convenu entre les signataires de"
        " la présente convention, que faute de réalisation totale ou partielle de la prestation de formation,"
        " l’organisme prestataire doit rembourser au cocontractant les sommes indûment perçues de ce fait."
        + "<br/>" + "<br/>" ,
        textstyle)
    res = Table([
        [text1],
        [text2],
        [text3],
        [text4],
        [text5],
        [text6],


    ],
        width,
    )

    res.setStyle([

    ])
    return res


def genConventionFormationFourth(width, height, formation_id):
    widthList = [
        width * 0.1,
        width * 0.8,
        width * 0.1,
    ]
    heightList = [
        height * 0.85,
        height * 0.15,
    ]

    res = Table([
        ['', _genPagefourthMain(widthList[1], heightList[0], formation_id), ''],
        ['', _genSignature(widthList[1], heightList[1]), ''],
    ],
        colWidths=widthList, )
    res.setStyle([
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        # ('BOTTOMPADDING', (1, 1), (1, 1), 0.6 * heightList[1]),
        # -('BOTTOMPADDING', (1, 2), (1, 2), 0.2 * heightList[1]),

    ])
    return res


def _genPagefourthMain(width, height, formation_id):
    textstyle = ParagraphStyle('texttwo')
    textstyle.fontSize = 11
    textstyle.leading = 15

    text1style = ParagraphStyle('texttwo')
    text1style.fontSize = 11
    text1style.leading = 15

    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontSize = 11
    # style.leading = 15
    formation_session = FormationSession.objects.get(id=formation_id)
    client_company = formation_session.client_account
    millforma = Company.objects.get(name="Mill Forma")

    if formation_session.teacher_price == None:
        teacher_price = "Non renseigné"
        tva = "Prix Formateur non renseigné"
    else:
        teacher_price = float(formation_session.teacher_price)
        tva = float(formation_session.teacher_price) * 0.2
    text1 = Paragraph("9 - DISPOSITIONS FINANCIERES" + "<br/>" + "<br/>" +
                      "Le paiement des frais de formation se fera directement à l’organisme (subrogation de paiement)"
                      + "<br/>" +"Le prix de l’action de formation est fixé à :" + "<br/>" + "<br/>",
        textstyle)
    text2 = Paragraph(
        "TOTAL HT : " + str(teacher_price) + "€ HT." + "<br/>" +
        "TVA (20%) : " + str(tva) + "€." + "<br/>" +
        "TOTAL TTC : " + str(teacher_price + tva) + "€" + "<br/>" + "<br/>",
        textstyle)

    text3 = Paragraph(
        "<b>10 - INTERRUPTION DU STAGE</b>" + "<br/>" + "<br/>" +
        """En cas de cessation anticipée de la formation du fait de l’organisme de formation ou en cas de renoncement 
        par l’entreprise bénéficiaire pour un autre motif que la force majeure dûment reconnue, la présente 
        convention est résiliée selon les modalités financières suivantes : Aucun versement.""" + "<br/>"
        + """Si le stagiaire est empêché de suivre la formation par suite de force majeure dûment reconnue, 
        la convention de formation professionnelle est résiliée. Dans ce cas, seules les prestations effectivement 
        dispensées sont dues au prorata temporis de leur valeur prévue au présent contrat.""" + "<br/>" + "<br/>" +
        "<b>11 - CAS DE DIFFEREND</b>" + "<br/>" + "<br/>" +
        """Si une contestation ou un différend n’ont pu être réglés à l’amiable, seul le tribunal de 
        commerce dans le ressort de la juridiction du siège social du centre de formation sera compétent 
        pour régler le litige.""" + "<br/>" + "<br/>",
        textstyle)

    res = Table([
        [text1],
        [text2],
        [text3],

    ],
        width,
    )

    res.setStyle([

    ])
    return res


def _genSignature(width, height):
    widthList = [
        width * 0.5,
        width * 0.5,
    ]

    textleftstyle = ParagraphStyle('textleft')
    textleftstyle.fontSize = 7.1
    textleft = Paragraph("<br/>" + "Fait à paris, LE " + timezone.now().strftime('%Y-%m-%d') + "<br/>"
                         + "En double exemplaire" + "<br/>" + "<br/>"
                         + "Le Prestataire" + "<br/>"
                         + "«Bon pour accord»",
                         textleftstyle)

    textrightstyle = ParagraphStyle('textright')
    textrightstyle.fontSize = 7.1

    textright = Paragraph("MILL-FORMA" + "<br/>"
                          + "William Berdugo" + "<br/>"
                          + "«Bon pour accord»",
                          textrightstyle)
    rightImgPath = 'https://mill-forma.fr/wp-content/uploads/2021/10/si_ca.png'
    rightImgWidth = widthList[1]
    signature = Image(
        rightImgPath, rightImgWidth, height, kind='proportional')
    res = Table([
        [textleft, textright, signature]
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
