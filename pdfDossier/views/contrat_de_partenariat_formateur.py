from django.utils import timezone
from reportlab.platypus import Table, Paragraph, Image
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import ListFlowable, ListItem
from main.models.company import Company
from main.models.formationsession import FormationSession


def genContratFormateurFirstPageTable(width, height, formation_id):
    widthList = [
        width * 0.1,
        width * 0.8,
        width * 0.1,
    ]
    heightList = [
        height * 0.112,
        height * 0.888,

    ]

    res = Table([

        ['', _genTitle(widthList[1], heightList[0]), ''],
        ['', _genEntre(widthList[1], heightList[1], formation_id), ''],

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

    text = Paragraph("<para alignment='center'>Contrat de partenariat Formateur</para>",
                     textstyle)
    res = Table([
        [text]
    ],
        width,
    )

    res.setStyle([
        ('ALIGN', (0, 1), (0, 1), 'CENTER'),

        ('GRID', (0, 0), (-1, -1), 1, 'black'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0.2 * height),
    ])
    return res


def _genEntre(width, height, formation_id):
    heightList = [
        height * 0.9,
        height * 0.1,

    ]

    formation_session = FormationSession.objects.get(id=formation_id)
    text1style = ParagraphStyle('texttwo')
    text1style.fontSize = 11
    text1style.leading = 15
    teacher_company=None
    try:
        teacher_company=Company.objects.get(contact=formation_session.teacher_name)
    except Company.DoesNotExist:
        print("Add message")
    if teacher_company != None :

        teacher_company_address=teacher_company.adresse.string()
    else:
        teacher_company_address="Non renseignée"
    text1 = Paragraph(
        "<b>Entre :</b>" + "<br/>" + "<br/>" +
        """La société Mill-Forma, sous le numéro de SIRET 84127900300013 dont
            le siège social est situé 35 rue de l’annonciation, 75016 PARIS
            représentée par William Berdugo en sa qualité de Président, ci-après
            dénommée « Mill Forma » ;""" + "<br/>" + "<br/>" + "D’une part," + "<br/>" + "<br/>"
        + "<b>Et :</b>" +
        "<br/>"  + formation_session.teacher_name.last_name + " " + formation_session.teacher_name.first_name +
        " - situé au  " + teacher_company_address + "<br/>"
        + "N° Siret : " + formation_session.teacher_name.company.num_siret+ "<br/>" + "<br/>" +
        "Ci-après dénommé le prestataire" + "<br/>" + "<br/>" + "<br/>" +
        "Ci-après collectivement désignées « les parties »" + "<br/>" + "<br/>" + "<br/>" +
        "<u><b>1) Objet :</b></u>" + "<br/>" + "<br/>" +
        "Le présent contrat a pour objet de déterminer les conditions générales selon lesquelles le prestataire "
        "s’engage à dispenser les actions de formation qui lui seront confiées par Mill Forma." + "<br/>" + "<br/>" +
        "Ce présent contrat ne garantit pas de volumes de formation minimum auprès du prestataire." + "<br/>" + "<br/>"
        +"<u><b>2) La durée :</b></u>" + "<br/>" + "<br/>" +
        "Le contrat de partenariat est conclu à durée indéterminée à partir de sa date de signature. Toutefois,"
        " au minimum, un entretien annuel sera organisé afin de faire le point sur le partenariat entre Mill Forma "
        "et le prestataire." + "<br/>" + "<br/>" +
        "En cas de manquement par l’une des parties de toute ou partie de ces obligations le contrat pourra être "
        "résilié sans indemnité du fait de sa résiliation." + "<br/>" + "<br/>" +
        "<u><b>3) Les engagements de Mill-Forma :</b></u>" + "<br/>" + "<br/>" +
        "Mill-Forma s’engage à :",
        text1style)

    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontSize = 11

    text2 = ListFlowable(
        [
            ListItem(Paragraph("Mettre à disposition tous les moyens nécessaires à la bonne exécution des prestations.",
                               style), leftIndent=45),
        ],
        bulletType='bullet',
        start='bulletchar',
        bulletFontSize=11,

    )

    res = Table([
        [text1],
        [text2],
    ],
        width,
        heightList)

    res.setStyle([
        ('BOTTOMPADDING', (0, 0), (0, 0), 0.03 * height),
        ('BOTTOMPADDING', (0, 1), (0, -1), 0.09 * height),
    ])
    return res


def genContratFormateurSecondPageTable(width, height):
    widthList = [
        width * 0.1,
        width * 0.8,
        width * 0.1,
    ]
    heightList = [
        height * 0.112,
        height * 0.888,

    ]

    res = Table([
        ['', '', ''],
        ['', _genPagetwoMain(widthList[1], heightList[1]), ''],

    ],
        colWidths=widthList,
        rowHeights=heightList)
    res.setStyle([
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('BOTTOMPADDING', (1, 1), (1, 1), 0.1 * heightList[1]),
    ])
    return res


def _genPagetwoMain(width, height):
    textstyle = ParagraphStyle('text')
    textstyle.fontSize = 11
    textstyle.leading = 15

    text = Paragraph("<u><b>4) Les engagements du prestataire :</b></u>" + "<br/>" + "<br/>" +
                     "Le prestataire s'engage à :",
                     textstyle)

    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontSize = 11
    style.leading = 15

    text2 = ListFlowable(
        [
            ListItem(Paragraph(
                "Mettre tout en œuvre pour garantir l’exécution de la prestation dans les règles de l’art de"
                " la profession.",
                style), leftIndent=45),
            ListItem(Paragraph(
                "Fournir à Mill-Forma tous les éléments d’ordre administratif et pédagogique indiqués dans "
                "le livret d’accueil.",
                style), leftIndent=45),
            ListItem(Paragraph(
                "Respecter la charte et le règlement intérieur de Mill Forma annexés au présent contrat et à respecter "
                "l’ordre de mission transmis avant chaque début de formation.",
                style), leftIndent=45),
            ListItem(Paragraph(
                "Faire valider auprès de Mill Forma les supports pédagogiques élaborés pour chaque formation.", style),
                     leftIndent=45),
            ListItem(Paragraph(
                "Porter dans le cadre de ses interventions une stricte tenue correcte, propre et adaptée. "
                "Compte tenu de la nature de ses interventions comportant un contact permanent avec la clientèle "
                "et de la nécessité pour Mill Forma de conserver une bonne image de marque.",
                style), leftIndent=45),
            ListItem(Paragraph(
                "S’engager à respecter les exigences du référentiel Qualiopi, selon les directives du donneur d’ordre.",
                style), leftIndent=45),
        ],
        bulletType='bullet',
        start='bulletchar',
        bulletFontSize=11,

    )

    text3style = ParagraphStyle('texttwo')
    text3style.fontSize = 11
    text3style.leading = 15

    text3 = Paragraph(

        "<br/>" + "<u><b>5) Prix et délais :</b></u>" + "<br/>" + "<br/>" +
        """La prestation est facturée sur la base du devis établi par le prestataire et annexé au présent contrat. 
        Le prestataire pourra prétendre au paiement de sa facture 30 jours après avoir remis à Mill Forma l’ensemble
         des documents d’ordre administratif et pédagogique (cf. livret d’accueil en annexe).""" + "<br/>" + "<br/>" +

        "<u><b>6) Confidentialité :</b></u>" + "<br/>" + "<br/>" +
        """Les parties s’engagent à traiter et garder de manière strictement confidentielle toutes informations
         commerciales, financières ou techniques quelles qu’en soit la nature, la forme ou le support, dont elles
          pourraient avoir connaissance du fait de l’exécution du contrat ainsi que toute information dont elles 
          pourraient avoir connaissance du fait de l’exécution du présent contrat.""" + "<br/>" + "<br/>" +

        "<u><b>7)  Responsabilité-assurance :</b></u>" + "<br/>" + "<br/>" +
        """Le prestataire déclare être assuré auprès d’une compagnie d’assurance. Il s’engage à fournir à Mill Forma 
        tous les ans une copie de son attestation d’assurance civile et professionnelle.""" + "<br/>" + "<br/>" +

        "<u><b>8)  Non-concurrence :</b></u>" + "<br/>" + "<br/>" +
        """Le prestataire s’engage à représenter la société Mill Forma et s’engage à ne pas démarcher, détourner
         ou tenter de démarcher ou de détourner les clients et les prospects à son profit ou pour le compte d’un tiers. 
         Le prestataire reconnaît que cette obligation de respect de clientèle ne porte nullement atteinte à sa liberté
          de travail en ce qu’elle ne lui interdit pas de travailler, pour le compte de sociétés concurrentes, 
          de créer lui-même une société concurrente ou encore d’exercer sous quelque forme que ce soit une activité 
          concurrente à celle de Mill Forma."""
        ,
        text3style)

    res = Table([
        [text],
        [text2],
        [text3],
    ],
        width,
    )

    res.setStyle([

        # ('BOTTOMPADDING', (0, 0), (-1, -1), 0.2* height),
    ])
    return res


def genContratFormateurThirdPageTable(width, height):
    widthList = [
        width * 0.1,
        width * 0.8,
        width * 0.1,
    ]
    heightList = [
        height * 0.112,
        height * 0.3958,
        height * 0.475,

    ]

    res = Table([
        ['', '', ''],
        ['', _genPagethreeMain(widthList[1], heightList[1]), ''],
        ['', _genPagethreeEnd(widthList[1], heightList[2]), ''],

    ],
        colWidths=widthList,
        rowHeights=heightList)
    res.setStyle([
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('BOTTOMPADDING', (1, 1), (1, 1), 0.6 * heightList[1]),
        ('BOTTOMPADDING', (1, 2), (1, 2), 0.2 * heightList[1]),

    ])
    return res


def _genPagethreeMain(width, height):
    textstyle = ParagraphStyle('texttwo')
    textstyle.fontSize = 11
    textstyle.leading = 15

    text = Paragraph(

        "<br/>" + "<u><b>9) Propriété intellectuelle :</b></u>" + "<br/>" + "<br/>" +
        """Chaque partie reste titulaire de ses droits de propriété intellectuelle respectifs détenus avant 
        l’entrée en relation d’affaires des parties. Le prestataire a la charge de fournir aux stagiaires tous 
        les supports pédagogiques utilisés en prestation et ce en quantité suffisante. Les supports de formation 
        ne pourront faire apparaître, sauf accord contraire, d’autres logos et chartes graphique que celles 
        de Mill Forma."""
        "<br/>"+"<u><b>10) Droit :</b></u>" + "<br/>" + "<br/>" +
        """Le contrat est soumis au droit français. En cas de différend concernant la formation, l'exécution ou
         la cessation du contrat, les parties s'engagent à tenter de trouver un accord amiable. A défaut d'un tel
          accord amiable entre les parties pour tout différend survenant entre elles, il est fait attribution de
           compétence aux tribunaux et ce, quel que soit le lieu d'exécution du contrat, le domicile du défendeur 
           ou le mode de règlement accepté, même dans le cas d'appel en garantie, d'une pluralité de défendeurs ou
            d'une procédure de référé."""
        ,
        textstyle)

    res = Table([
        [text],
    ],
        width,
    )

    res.setStyle([

    ])
    return res


def _genPagethreeEnd(width, height):
    widthList = [
        width * 0.537,
        width * 0.463,
    ]

    textleftstyle = ParagraphStyle('textleft')
    textleftstyle.fontSize = 12

    textleft = Paragraph("<b><u>Fait à Paris en double exemplaire :</u></b>" + "<br/>" + "<br/>" + "<br/>"
                         + "Le :" + timezone.now().strftime('%Y-%m-%d') + "<br/>" + "<br/>" + "<br/>"
                         + "Signature et paraphe sur chaque page," + "<br/>" + "<br/>" + "<br/>" + "<br/>"
                         + "Pour le prestataire" + "<br/>" + "<br/>"
                         + "« Lu et approuvé »" + "<br/>",
                         textleftstyle)

    textrightstyle = ParagraphStyle('textleft')
    textrightstyle.fontSize = 12

    textright = Paragraph(
        "Pour Mill Forma" + "<br/>" + "<br/>" +
        "« Lu et approuvé »" + "<br/>",
        textleftstyle)

    rightImgPath = 'https://mill-forma.fr/wp-content/uploads/2021/10/si_ca.png'
    rightImgWidth = widthList[1]
    rightImg = Image(
        rightImgPath, 0.25 * width, height, kind='proportional')

    res = Table([
        [textleft, rightImg, textright]
    ],
        widthList,
        height)
    res.setStyle([

        ('BOTTOMPADDING', (0, 0), (0, 0), 0.5 * height),
        ('BOTTOMPADDING', (2, 0), (2, 0), 0.49 * height),
        ('BOTTOMPADDING', (1, 0), (1, 0), 0.2 * height),
        ('LEFTPADDING', (2, 0), (2, 0), -0.75 * widthList[1]),
        ('LEFTPADDING', (1, 0), (1, 0), 0.17 * widthList[1]),

    ])

    return res
