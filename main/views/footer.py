from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.platypus import Table


def genFooterTable(width, height):

    widthList = [
        width*0.1,
        width*0.8,
        width*0.1,
    ]
    height=height
    textstyle= ParagraphStyle('tex1')
    textstyle.fontSize = 7.1

    text = Paragraph("""MILL-FORMA | SAS au capital de 6000 euros – RCS de Paris - 35 rue de l’annonciation 
                        PARIS 75016 | Numéro SIRET : 84127900300013 | Déclaration d’activité n°: 11755769175 
                        enregistrée auprès du préfet de la région ILE DE France Cet enregistrement ne vaut pas agrément 
                        de l’Etat MILL-FORMA vous souhaite une excellente formation !""", textstyle)

    res=Table([
        ['',text,'']],
        colWidths=widthList,
        rowHeights=height,
        )

    res.setStyle([

        ('BOTTOMPADDING', (0, 0), (-1, -1), 0.35* height),


    ])

    return res