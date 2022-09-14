from django.utils import timezone
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, Paragraph, Image
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import ListFlowable, ListItem
from reportlab.lib import colors
from main.models.company import Company
from main.models.formationsession import FormationSession


def genBondecommandeTable(width, height, formation_id, user):
    widthList = [
        width * 0.1,
        width * 0.8,
        width * 0.1,
    ]
    heightList = [
        height * 0.0266,
        height * 0.1734,
        height * 0.45,
        height * 0.2245,
        height * 0.1255,
    ]

    res = Table([

        ['', _genBondecommande(formation_id), ''],
        ['', _genCommande(widthList[1], heightList[1], formation_id, user), ''],
        ['', _genArticle(widthList[1], heightList[2], formation_id), ''],
        ['', _genTableau(widthList[1], heightList[3], formation_id), ''],
        ['', _genSignature(widthList[1], heightList[4]), ''],
    ],
        colWidths=widthList,
        rowHeights=heightList)
    res.setStyle([

        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
    ])
    return res


def _genBondecommande(formation_id):
    width, height = A4
    textstyle = ParagraphStyle('text')
    textstyle.fontSize = 7.1

    text = Paragraph("<b><u>Bon de commande</u></b>",
                     textstyle)
    res = Table([
        [text]
    ],
        0.15 * width,
    )

    res.setStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

    ])
    return res


def _genCommande(width, height, formation_id, user):
    widthList = [
        width * 0.5,
        width * 0.5,
    ]
    formation_session = FormationSession.objects.get(id=formation_id)
    client_company = formation_session.client_account
    millforma = Company.objects.get(name="Mill Forma")
    textleftstyle = ParagraphStyle('textleft')
    textleftstyle.textColor = colors.HexColor('#808080')
    textleftstyle.fontSize = 7.1

    textleft = Paragraph("<font color='black'><b><u>L'ORGANISME DE FORMATION</u></b></font>" + "<br/>"
                         + "Raison Sociale :" + millforma.raison_sociale + "<br/>"
                         + "Numéro de déclaration d'activité :" + millforma.num_decla_activite + "<br/>"
                         + "Siret :" + millforma.num_siret + "<br/>"
                         + "Adresse :" + millforma.adresse.string() + "<br/>"
                         + "<font color='black'> Ci-après « le donneur d'ordre »</font>",
                         textleftstyle)
    if client_company.adresse != None:
        client_company_address=client_company.adresse.string()
    else:
        client_company_address="Non renseignée"

    textrightstyle = ParagraphStyle('textright')
    textrightstyle.fontSize = 7.1
    textrightstyle.textColor = colors.HexColor('#808080')
    textright = Paragraph("<font color='black'><b><u>LE FORMATEUR</u></b></font>" + "<br/>"
                          + "Raison Sociale :" + client_company.raison_sociale + "<br/>"
                          + "Représenté par :" + client_company.contact.first_name +" "+
                          client_company.contact.last_name + "<br/>"
                          + "Siret :" + client_company.num_siret + "<br/>"
                          + "Adresse :" + client_company_address + "<br/>"
                          + "<font color='black'> Ci-après « le prestataire »</font>" + "<br/>" + "<br/>"
                          + "<font color='black'> Ci-après « le sous-traitant »</font>",
                          textrightstyle)

    res = Table([
        [textleft, textright]
    ],
        widthList,
        height)

    res.setStyle([

        ('BOTTOMPADDING', (0, 0), (0, 0), 0.24 * height),
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (1, 0), (1, 0), 0.1 * widthList[1]),

    ])
    return res


def _genArticle(width, height, formation_id):
    formation_session = FormationSession.objects.get(id=formation_id)
    millforma = Company.objects.get(name="Mill Forma")
    heightList = [
        height * 0.12,
        height * 0.11,
        height * 0.077,
        height * 0.423,
        height * 0.27,
    ]

    titlestyle = ParagraphStyle('textleft')
    titlestyle.fontSize = 8

    text1 = Paragraph("<b><u>Article 1: Nature du contrat :</u></b>",
                      titlestyle)

    text2style = ParagraphStyle('textright')
    text2style.fontSize = 8
    text2 = Paragraph(
        """Le présent contrat est conclu dans le cadre d'une prestation de formation ponctuelle réalisée par le 
        sous-traitant au bénéfice du donneur d'ordre""",
        text2style)

    text3 = Paragraph("<b><u>Article 2: Objet du contrat :</u></b>",
                      titlestyle)

    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontSize = 8.5
    style.textColor = colors.HexColor('#808080')
    if formation_session.teacher_price != None:
        teacher_price=formation_session.teacher_price
    else:
        teacher_price="Coût formateur non renseigné"
    if formation_session.date_autorised_start != None:
        formation_session_date_start=formation_session.date_autorised_start.strftime('%Y-%m-%d')
    else:
        formation_session_date_start="Non renseignée"
    if formation_session.date_autorised_end != None:
        formation_session_date_end=formation_session.date_autorised_end.strftime('%Y-%m-%d')
    else:
        formation_session_date_end="Non renseignée"
    text4 = ListFlowable(
        [
            ListItem(Paragraph("Intitulé de la formation :&nbsp;&nbsp;" + formation_session.name, style),
                     leftIndent=45),
            ListItem(Paragraph("Client :&nbsp;&nbsp;" + millforma.name, style), leftIndent=45),
            ListItem(Paragraph("Lieu de la formation :&nbsp;&nbsp;" + str(formation_session.training_site), style),
                     leftIndent=45),
            ListItem(Paragraph("Bénéficiaire :&nbsp;&nbsp;" + formation_session.client_account.name, style),
                     leftIndent=45),
            ListItem(
                Paragraph("Nombre de participant(s) :&nbsp;&nbsp;" + str(formation_session.trainee.count()), style),
                leftIndent=45),
            ListItem(Paragraph("Durée en heures :&nbsp;&nbsp;" + str(formation_session.training_duration) + "H", style),
                     leftIndent=45),
            ListItem(Paragraph("Dates :&nbsp;&nbsp;" + formation_session_date_start + " au " +
                               formation_session_date_end, style), leftIndent=45),
            ListItem(Paragraph("Soit un total de :&nbsp;&nbsp;" + str(teacher_price), style),
                     leftIndent=45),

        ],
        bulletType='bullet',
        start='bulletchar',
        bulletFontSize=9.4,

    )

    text5style = ParagraphStyle('textright')
    text5style.fontSize = 7.1
    text5 = Paragraph(
        "Le formateur s'engage à respecter les exigences du réferentiel Qualiopi, selon les directives du "
        "donneur d'ordre." + "<br/>" +
        """Mill Forma s'autorise à annuler les suivants la première journée de formation, s'il s'avérait 
        que les compétences du prestataire ne conviennet pas au client final et/ ou aux stagiaires.""" + "<br/>" +
        "Le prestataire pourra prétendre au paiement de sa facture 30 jours après avoir remis MILL FORMA" + "<br/>"
        + "<br/>",
        text5style)

    res = Table([
        [text1],
        [text2],
        [text3],
        [text4],
        [text5],

    ],
        width,
        heightList)

    res.setStyle([

    ])
    return res


def _genTableau(width, height, formation_id):
    widthList = [
        width * 0.5,
        width * 0.5,
    ]
    heightList = [
        height * 0.2,
        height * 0.8,
    ]
    titleleftstyle = ParagraphStyle('titleleft')
    titleleftstyle.fontSize = 8

    titleleft = Paragraph("<b>AVANT FORMATION</b>",
                          titleleftstyle)

    textleftstyle = ParagraphStyle('textleft')
    textleftstyle.fontSize = 9
    textleft = ListFlowable(
        [
            ListItem(Paragraph("L’ordre de mission signé par le prestataire", textleftstyle), leftIndent=35),
            ListItem(Paragraph("La présentation des méthodes et moyens pédagogiques", textleftstyle), leftIndent=35),
            ListItem(Paragraph("L’évaluation des prérequis", textleftstyle), leftIndent=35),
            ListItem(Paragraph("Avoir communiqué à Mill Forma une copie de son extrait K-bis / de son immatriculation",
                               textleftstyle), leftIndent=35),
            ListItem(Paragraph("Avoir communiqué un CV", textleftstyle), leftIndent=35),
            ListItem(Paragraph("Supports de cours (Extrait au minimum)", textleftstyle), leftIndent=35),

        ],
        bulletType='bullet',
        start='bulletchar'
              '',
        bulletFontSize=10,

    )

    titlerightstyle = ParagraphStyle('titleright')
    titlerightstyle.fontSize = 7.1
    titleright = Paragraph("<b>72 HEURES MAXIMUM APRÈS LA FORMATION</b>",
                           titlerightstyle)

    textrightstyle = ParagraphStyle('textright')
    textrightstyle.fontSize = 9
    textright = ListFlowable(
        [
            ListItem(Paragraph("L’évaluation des acquis", textleftstyle), leftIndent=35),
            ListItem(Paragraph("Questionnaire de satisfaction (fournie par Mill Forma)", textleftstyle), leftIndent=35),
            ListItem(Paragraph(
                "Les feuilles d’émargement journalières des stagiaires (Matin et après-midi) (fournie par Mill-Forma)",
                textleftstyle), leftIndent=35),
            ListItem(Paragraph("Le compte-rendu de la formation",
                               textleftstyle), leftIndent=35),
            ListItem(Paragraph("La facture du prestataire", textleftstyle), leftIndent=35),

        ],
        bulletType='bullet',
        start='bulletchar',
        bulletFontSize=10,

    )

    res = Table([
        [titleleft, titleright],
        [textleft, textright]
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
