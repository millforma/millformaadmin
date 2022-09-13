from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import ListFlowable, ListItem
from reportlab.platypus import Table, Paragraph


def genReglementInterieurFirstPageTable(width, height):
    widthList = [
        width * 0.3,
        width * 0.3,
        width * 0.3,
    ]

    res = Table([

        [_genContenuGauchefirst(widthList[0], height), _genContenuCentrefirst(widthList[1], height),
         _genContenuDroitefirst(widthList[2], height)],

    ],
        colWidths=widthList,
        rowHeights=height)
    res.setStyle([
        ('BOTTOMPADDING', (1, 0), (1, 0), 0.035 * height),
        ('BOTTOMPADDING', (2, 0), (2, 0), 0.025 * height),
        ('LEFTPADDING', (0, 0), (-1, -1), 0.05 * width),
    ])
    return res


def _genContenuGauchefirst(width, height):
    title1style = ParagraphStyle('text')
    title1style.fontSize = 9
    title1style.leading = 9.5

    title1 = Paragraph("<b>1.&nbsp;&nbsp;&nbsp; Préambule </b>", title1style)

    text1style = ParagraphStyle('text')
    text1style.fontSize = 6.75
    text1style.leading = 8

    text1 = Paragraph(
        """Mill-Forma est un organisme de formation domicilié au 35
            rue de l’annonciation 75016 PARIS, ci-après dénommé
                l’organisme de formation.""" + "<br/>" + """Le responsable de l’organisme de formation est :
                William Berdugo""" + "<br/>" + "<br/>" +
        """Le présent Règlement Intérieur a vocation à préciser certaines dispositions s’appliquant à tous les
         inscrits et participants aux différents stages organisés par l’organisme
        de formation dans le but de permettre un fonctionnement régulier des formations proposées. """ +
        "Définitions:",
        text1style)

    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontSize = 7
    style.leading = 6

    bulletlist1 = ListFlowable(
        [
            ListItem(Paragraph("Les personnes suivant le stage seront dénommées ci-après « stagiaires ».", style),
                     leftIndent=45),
        ],
        bulletType='bullet',
        start='bulletchar',
        bulletFontSize=7,

    )

    title2 = Paragraph("<b>2.&nbsp;&nbsp;&nbsp; Dispositions Générales </b>", title1style)

    text2 = Paragraph(
        "<u><b>Article 1</b></u>" + "<br/>" +
        """Conformément aux articles L6352-3 et suivants et R6352-1 et suivants du Code du travail, 
        le présent Règlement Intérieur a pour objet de définir les règles générales et permanentes et
        de préciser la réglementation en matière d’hygiène et de sécurité ainsi que les règles relatives à la
         discipline, notamment les sanctions applicables aux stagiaires et les
        droits de ceux-ci en cas de sanction. """ + "<br/>"
        ,
        text1style)

    title3 = Paragraph("<b>3. &nbsp;&nbsp;&nbsp;Champ d’application</b>", title1style)
    text3 = Paragraph(
        "<u><b>Article 2 : Personnes concernées</b></u>" + "<br/>" +
        """Le présent Règlement s’applique à tous les stagiaires inscrits à une session dispensée par l’organisme de 
        formation et ce, pour toute la durée de la formation suivie.""" + "<br/>" + """Chaque stagiaire est considéré
         comme ayant accepté lestermes du présent règlement lorsqu'il suit une formation dispensée par l’organisme de
          formation et accepte que des mesures soient prises à son égard en cas d'inobservation de ce dernier. """
        + "<br/>" + "<u><b>Article 3 : Lieu de la formation</b></u>" + "<br/>" +
        """La formation aura lieu soit dans les locaux de l’organisme de formation, soit dans des locaux extérieurs.
         Les dispositions du présent Règlement sont applicables non seulement au sein des locaux de l’organisme de
          formation, mais également dans tout local ou espace accessoire à l’organisme. """
        ,
        text1style)
    title4 = Paragraph("<b>4. &nbsp;&nbsp;&nbsp;Hygiène et sécurité</b>", title1style)
    text4 = Paragraph(
        "<u><b>Article 4 : Règles générales</b></u>" + "<br/>" +
        """Chaque stagiaire doit veiller à sa sécurité personnelle et à celle des autres en respectant les
         consignes générales et particulières de sécurité et d’hygiène en vigueur sur le lieu de
           formation. """ + "<br/>" +
        """Toutefois, conformément à l'article R6352-1 du Code du travail, lorsque la formation se déroule dans 
        une entreprise ou un établissement déjà doté d'un règlement intérieur, les mesures de sécurité et 
        d'hygiène applicables aux stagiaires sont celles de ce dernier règlement.  """ + "<br/>" +
        "<u><b>Article 5 : Boissons alcoolisées</b></u>" + "<br/>" +
        """Il est interdit aux stagiaires de pénétrer ou de séjourner dans l’établissement en état d’ivresse ainsi
         que d’y introduire des boissons alcoolisées. """ + "<br/>" +
        "<u><b>Article 6 :  Interdiction de fumer </b></u>" + "<br/>" +
        """En application du décret n° 92-478 du 29 mai 1992 fixant les conditions d'application de l'interdiction
         de fumer dans les lieux affectés à un usage collectif, il est interdit de fumer dans les locaux de formation,
          sauf dans les lieux réservés à cet usage.""" + "<br/>" +
        "<u><b>Article 7 :  Lieux de restauration </b></u>" + "<br/>" +
        """L’accès aux lieux de restauration n’est autorisé que pendant les heures fixées pour les repas. 
        Il est interdit, sauf autorisation spéciale, donnée par le responsable de l’organisme de formation,
         de prendre ses repas dans les salles où se déroulent les stages. """ + "<br/>"
        , text1style)

    res = Table([
        [title1],
        [text1],
        [bulletlist1],
        [title2],
        [text2],
        [title3],
        [text3],
        [title4],
        [text4]

    ],
        colWidths=width,
    )

    res.setStyle([
        ('LINEBELOW', (0, 0), (0, 0), 1, colors.black),
        ('LINEBELOW', (0, 3), (0, 3), 1, colors.black),
        ('LINEBELOW', (0, 5), (0, 5), 1, colors.black),
        ('LINEBELOW', (0, 7), (0, 7), 1, colors.black),

    ])
    return res


def _genContenuCentrefirst(width, height):
    text1style = ParagraphStyle('text')
    text1style.fontSize = 6.75
    text1style.leading = 8
    text1 = Paragraph(
        "<u><b>Article 8 : Consignes d’incendie</b></u>" + "<br/>" +
        """Conformément aux articles R.4227-37 et suivants du Code du travail, les consignes d'incendie et notamment 
        un plan de localisation des extincteurs et des issues de secours sont affichés dans les locaux de formation
         de manière à être connus de tous les stagiaires. """ + "<br/>"
        ,
        text1style)

    text2 = Paragraph(
        "<u><b>Article 9 : Accident </b></u>" + "<br/>" +
        """Tout accident ou incident survenu à l'occasion ou en cours de formation doit être immédiatement déclaré par
         le stagiaire accidenté ou les personnes témoins de l'accident, au responsable de l'organisme.""" + "<br/>" +
        """CConformément à l'article R.6342-3 du Code du travail, l'accident survenu au stagiaire pendant qu'il 
        se trouve sur le lieu de formation ou pendant qu'il s'y rend ou en revient, fait l'objet d'une déclaration 
        par le responsable de l’organisme auprès de la caisse de sécurité sociale.""" + "<br/>" + """Les consignes de 
        sécurité sanitaires sont appliquées selon les recommandations gouvernementales""" + "<br/>"
        ,
        text1style)

    title1style = ParagraphStyle('text')
    title1style.fontSize = 9
    title1style.leading = 9.5

    title1 = Paragraph("<b>5. &nbsp;&nbsp;&nbsp;Discipline</b>", title1style)
    text3 = Paragraph(
        "<u><b>Article 10 : Tenue et comportement </b></u>" + "<br/>" +
        """Les stagiaires sont invités à se présenter au lieu de formation en tenue décente et à avoir un 
        comportement correct à l'égard de toute personne présente dans l'organisme ou leslocaux mis à disposition de 
        l’organisme. """ + "<br/>" +

        "<u><b>Article 11 : Horaires de stage</b></u>" + "<br/>" +
        """Les horaires de stage sont fixés par l’organisme de formation et portés à la connaissance des stagiaires
         soit par la convocation adressée par courrier (postal ou électronique), soit à l'occasion de la remise aux 
        stagiaires du programme de formation. Les stagiaires sont tenus de respecter ces horaires.""" + "<br/>" +
        """L’organisme de formation se réserve, dans les limites imposées par des dispositions en vigueur, le droit de
         modifier les horaires de stage en fonction des nécessités de service. Les stagiaires doivent se conformer
          aux modifications apportées par l’organisme de formation aux horaires d’organisation du stage.""" +
        "<br/>" + """En cas d'absence ou de retard au stage, il est préférable pour le stagiaire d’en avertir 
        le formateur. Par ailleurs, une feuille d’émargement doit être signée par le stagiaire. """ + "<br/>" +
        "<u><b>Article 12 : Accès au lieu de formation</b></u>" + "<br/>" +
        """Sauf autorisation expresse de l’organisme de formation, les stagiaires ayant accès au lieu de formation 
        pour suivre leur stage ne peuvent :""" + "<br/>"
        , text1style)
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontSize = 7
    style.leading = 8

    bulletlist1 = ListFlowable(
        [
            ListItem(Paragraph("y entrer ou y demeurer à d'autres fins ;", style), leftIndent=45),
            ListItem(Paragraph("faciliter l'introduction de tierces personnes à l’organisme. ", style), leftIndent=45),
        ],
        bulletType='bullet',
        start='bulletchar',
        bulletFontSize=7,

    )
    text4 = Paragraph(
        "<u><b>Article 13 : Usage du matériel</b></u>" + "<br/>" +
        """Chaque stagiaire a l'obligation de conserver en bon état le matériel qui lui est confié en vue de sa
         formation. Les stagiaires sont tenus d'utiliser le matériel conformément à son objet. L’utilisation du 
         matériel à d'autres fins, notamment personnelles est interdite, sauf pour le matériel mis à disposition 
         à cet effet.""" + "<br/>" + """A la fin du stage, le stagiaire est tenu de restituer tout matériel et
          document en sa possession appartenant à l’organisme de formation, sauf les documents pédagogiques distribués
           en cours de formation.""" + "<br/>" +

        "<u><b>Article 14 : Enregistrements</b></u>" + "<br/>" +
        """Il est formellement interdit, sauf dérogation expresse, d’enregistrer ou de filmer les sessions de 
        formation.""" + "<br/>" + "<u><b>Article 15 : Documentation pédagogique</b></u>" + "<br/>" +
        """La documentation pédagogique remise lors des sessions de formation est protégée au titre des droits d’auteur
         et ne peut être réutilisée autrement que pour un strict usage personnel. Il est formellement interdit de se
          procurer une copie électronique (fichier) des documents pédagogiques distribués en cours de formation."""
        + "<br/>"

        , text1style)

    res = Table([

        [text1],
        [text2],
        [title1],
        [text3],
        [bulletlist1],
        [text4],

    ],
        colWidths=width,
    )

    res.setStyle([
        ('LINEBELOW', (0, 2), (0, 2), 1, colors.black),

        # ('BOTTOMPADDING', (0, 0), (0, 0), 0.03 * height),
        # ('BOTTOMPADDING', (0, 1), (0, -1), 0.09* height),
    ])
    return res


def _genContenuDroitefirst(width, height):
    text1style = ParagraphStyle('text')
    text1style.fontSize = 6.75
    text1style.leading = 8
    text1 = Paragraph(
        "<u><b>Article 16 : Responsabilité de l'organisme en cas de vol ou endommagement de biens personnels des "
        "stagiaires </b></u>" + "<br/>" + """L’organisme de formation décline toute responsabilité en cas de perte, 
        vol ou détérioration des objets personnels de toutes natures déposés par les stagiaires dans les locaux de 
        formation.""" + "<br/>" + "<u><b>Article 17 : Sanctions</b></u>" + "<br/>" +
        """Tout manquement du stagiaire à l'une des dispositions du présent Règlement Intérieur pourra faire 
        l'objet d'une sanction. """ + "<br/>" +
        """Constitue une sanction au sens de l'article R6352-3 du Code du travail toute mesure, autre que les
         observations verbales, prise par le responsable de l'organisme de formation ou son représentant, à la
          suite d'un agissement du stagiaire considéré par lui comme fautif, que cette mesure soit de nature à affecter
           immédiatement ou non la présence de l'intéressé dans le stage ou à mettre en cause la continuité de la 
           formation qu'il reçoit.""" + "<br/>" +
        "<br/>" + """"Selon la gravité du manquement constaté, la sanction pourra consister :"""
        ,
        text1style)

    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontSize = 7
    style.leading = 8

    bulletlist1 = ListFlowable(
        [
            ListItem(Paragraph("Soit en un avertissement ; ", style), leftIndent=45),
            ListItem(Paragraph("Soit en un blâme ;", style), leftIndent=45),
            ListItem(Paragraph("Soit en une mesure d'exclusion définitive. ", style), leftIndent=45),
        ],
        bulletType='bullet',
        start='bulletchar',
        bulletFontSize=7,

    )
    text2 = Paragraph(

        """Les amendes ou autres sanctions pécuniaires sont interdites. Le responsable de l'organisme de formation 
        doit informer de la sanction prise :""" + "<br/>"
        ,
        text1style)
    bulletlist2 = ListFlowable(
        [
            ListItem(Paragraph(
                """L'employeur, lorsque le stagiaire est un salarié bénéficiant d'un stage dans le cadre du plan de
                 formation en entreprise ; """,
                style)),
            ListItem(Paragraph(
                """L'employeur et l'organisme paritaire qui a pris à sa charge les dépenses de la formation, lorsque
                 le stagiaire est un salarié bénéficiant d'un stage dans le cadre d'un congé de formation ;""",
                style)),
            ListItem(Paragraph(
                """L'organisme qui a assuré le financement de l'action de formation dont a bénéficié le stagiaire.""",
                style)),
        ],
        bulletType='bullet',
        start='bulletchar',
        bulletFontSize=7,

    )

    text3 = Paragraph(
        "<u><b>Article 18 : Procédure disciplinaire </b></u>" + "<br/>" +
        """Aucune sanction ne peut être infligée au stagiaire sans que celui-ci ait été informé au préalable des 
        griefs retenus contre lui.""" + "<br/>" +"""Lorsque le responsable de l'organisme de formation ou son 
        représentant envisage de prendre une sanction qui a une incidence, immédiate ou non, sur la présence d'un 
        stagiaire dans une formation, il est procédé ainsi qu'il suit : """

        , text1style)

    bulletlist3 = ListFlowable(
        [
            ListItem(Paragraph(
                """Le responsable de l'organisme de formation ou son représentant convoque le stagiaire en lui 
                indiquant l'objet de cette convocation.""",
                style)),
            ListItem(Paragraph(
                """Celle-ci précise la date, l'heure et le lieu de l'entretien. Elle est écrite et est adressée par 
                lettre recommandée ou remise à l'intéressé contre décharge.""",
                style)),
            ListItem(Paragraph(
                """Au cours de l'entretien, le stagiaire peut se faire assister par une personne de son choix, 
                stagiaire ou salarié de l'organisme de formation.""",
                style), ),
            ListItem(Paragraph(
                """La convocation mentionnée à l'alinéa précédent fait état de cette faculté. Le responsable de 
                l'organisme de formation ou son représentant indique le motif de la sanction envisagée et recueille 
                les explications du stagiaire. Dans le cas où une exclusion définitive du stage est envisagée, une
                 commission de discipline est constituée, où siègent des représentants des stagiaires.""",
                style)),
            ListItem(Paragraph(
                """Elle est saisie par le responsable de l'organisme de formation ou son représentant après 
                l'entretien susvisé et formule un avis sur la mesure d'exclusion envisagée.""",
                style)),

        ],
        bulletType='bullet',
        start='bulletchar',
        bulletFontSize=7,

    )

    res = Table([

        [text1],
        [bulletlist1],
        [text2],
        [bulletlist2],
        [text3],
        [bulletlist3],

    ],
        colWidths=width,
    )

    res.setStyle([

    ])
    return res


def genReglementInterieurSecondPageTable(width, height):
    widthList = [
        width * 0.3,
        width * 0.3,
        width * 0.3,
    ]

    res = Table([

        [_genContenuGauche(widthList[0], height), _genContenuCentre(widthList[1], height),
         _genContenuDroite(widthList[2], height)],

    ],
        colWidths=widthList,
        rowHeights=height)
    res.setStyle([
        ('BOTTOMPADDING', (0, 0), (0, 0), 0.71 * height),
        ('BOTTOMPADDING', (1, 0), (1, 0), 0.55 * height),
        ('BOTTOMPADDING', (2, 0), (2, 0), 0.84 * height),
        ('LEFTPADDING', (0, 0), (-1, -1), 0.05 * width),
        ('LINEBELOW', (-1, -1), (-1, -1), 1, colors.black),

    ])
    return res


def _genContenuGauche(width, height):
    title1style = ParagraphStyle('text')
    title1style.fontSize = 9
    title1style.leading = 9.5

    text1style = ParagraphStyle('text')
    text1style.fontSize = 6.75
    text1style.leading = 8

    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontSize = 7
    style.leading = 6

    bulletlist1 = ListFlowable(
        [
            ListItem(Paragraph(
                """Le stagiaire est avisé de cette saisine. Il est entendu sur sa demande par la commission de 
                discipline. Il peut, dans ce cas, être assisté par une personne de son choix, stagiaire ou salarié 
                de l'organisme. La commission de discipline transmet son avis au Directeur de l'organisme dans le 
                délai d'un jour franc après sa réunion.""",
                style)),
            ListItem(Paragraph(
                """La sanction ne peut intervenir moins d'un jour franc ni plus de quinze jours après l'entretien ou,
                 le cas échéant, après la transmission de l'avis de la commission de discipline. Elle fait l'objet
                  d'une décision écrite et motivée, notifiée au stagiaire sous la forme d'une lettre qui lui est 
                  remise contre décharge ou d'une lettre recommandée.""",
                style)),
        ],
        bulletType='bullet',
        start='bulletchar',
        bulletFontSize=7,

    )
    text1 = Paragraph(
        """Lorsque l'agissement a donné lieu à une mesure conservatoire d’exclusion temporaire à effet immédiat, 
        aucune sanction définitive, relative à cet agissement, ne peut être prise sans que le stagiaire ait été 
        informé au préalable des griefs retenus contre lui et éventuellement que la procédure ci-dessus décrite ait 
        été respectée.""" + "<br/>",
        text1style)

    res = Table([

        [bulletlist1],
        [text1],

    ],
        colWidths=width,
    )

    res.setStyle([

    ])
    return res


def _genContenuCentre(width, height):
    text1style = ParagraphStyle('text')
    text1style.fontSize = 6.75
    text1style.leading = 8

    title1style = ParagraphStyle('text')
    title1style.fontSize = 9
    title1style.leading = 9.5

    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontSize = 7
    style.leading = 8

    title1 = Paragraph("<b>6.&nbsp;&nbsp;&nbsp; Représentation des stagiaires</b>", title1style)

    text2 = Paragraph(

        """Conformément aux articles R6352-9 à 12 du code du travail, concernant les stages collectifs, l’organisme 
        de formation organisera l’élection d’un délégué titulaire et d’un délégué suppléant. L’élection des 
        représentants des stagiaires aura lieu pendant les heures de cours entre la 20eme et la 40eme heure. 
        Le scrutin sera uninominal à deux tours. Tous les stagiaires sont électeurs et éligibles. S’il y a carence
         de représentant des stagiaires, un procès-verbal de carence sera établi par le responsable de l’organisme 
         de formation.""" + "<br/>" +
        """Conformément aux articles R6352-13 à 15 du code du travail, les délégués sont élus pour la durée du stage.
         Leurs fonctions prennent fin lorsqu'ils cessent de participer au stage. Lorsque le délégué titulaire et le
          délégué suppléant ont cessé leurs fonctions avant la fin du stage, il est procédé à une nouvelle élection, 
          dans les conditions prévues au paragraphe précédent.""" + "<br/>" +

        """Les délégués font toute suggestion pour améliorer le déroulement des stages et les conditions de vie des
         stagiaires dans l'organisme de formation. Ils présentent les réclamations individuelles ou collectives 
         relatives à ces matières, aux conditions de santé et de sécurité au travail et à l'application du règlement 
         intérieur.""" + "<br/>" +

        """Les dispositions de la présente section ne sont pas applicables aux détenus admis à participer à une action
         de formation professionnelle.""" + "<br/>" +"""Si la formation de l’organisme de formation est incluse à une 
         formation de plus longue durée dispensée par une autre entreprise, le règlement intérieur de cette dernière
          sera appliqué.""" + "<br/>"
        , text1style)
    res = Table([

        [title1],
        [text2],

    ],
        colWidths=width,
    )

    res.setStyle([
        ('LINEBELOW', (0, 0), (0, 0), 1, colors.black),

        # ('BOTTOMPADDING', (0, 1), (0, -1), 0.09* height),
    ])
    return res


def _genContenuDroite(width, height):
    text1style = ParagraphStyle('text')
    text1style.fontSize = 6.75
    text1style.leading = 8

    title1style = ParagraphStyle('text')
    title1style.fontSize = 9
    title1style.leading = 9.5

    title1 = Paragraph("<b>7.&nbsp;&nbsp;&nbsp; Publicité et date d’entrée en vigueur</b>", title1style)

    text1 = Paragraph(
        "<u><b>Article 19 : Publicité </b></u>" + "<br/>" +
        """Le présent règlement est porté à la connaissance de chaque stagiaire.""" + "<br/>" +
        """Un exemplaire du présent règlement est disponible dans les locaux de l’organisme de formation. """
        + "<br/>" +"<u><b>Article 20 : Date d’entrée en vigueur</b></u>" + "<br/>" +
        """Ce règlement rentre en vigueur au 14/04/2021."""
        ,
        text1style)

    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontSize = 7
    style.leading = 8

    res = Table([

        [title1],
        [text1],

    ],
        colWidths=width,
    )

    res.setStyle([
        ('LINEBELOW', (0, 0), (0, 0), 1, colors.black),
    ])
    return res
