from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Table, Image, Paragraph


def genHeaderTable(width, height):
    current_file = "https://ik.imagekit.io/cp2syebk8zv/mill-forma_9E3IB0RzI.png?ik-sdk-version=" \
                   "javascript-1.4.3&updatedAt=1644934271988"
    imgPath = current_file
    img = Image(imgPath)

    res = Table([
        [img]
    ],
        width,
        height)
    res.setStyle([

        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ])

    return res


def genHeaderReglementTable(width, height):
    widthList = [
        width * 56 / 100,  # col 1 - left image
        width * 40 / 100,  # col 2 - right image
        0
    ]

    leftImgPath = 'https://mill-forma.fr/wp-content/uploads/2021/10/mill-forma.png'
    leftImgWidth = widthList[0]
    leftImg = Image(leftImgPath, leftImgWidth, height, kind='proportional')

    text1style = ParagraphStyle('texttwo')
    text1style.fontSize = 16
    text1style.leading = 15

    rightText = Paragraph("<b>Règlement intérieur</b>", text1style)

    res = Table([
        [leftImg, rightText]
    ],
        widthList,
        height)

    res.setStyle([

        ('BOTTOMPADDING', (0, 0), (0, 0), 0.2 * height),
        ('LEFTPADDING', (0, 0), (0, 0), width * 0.05),
        ('LEFTPADDING', (1, 0), (1, 0), width * 0.1),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),  # horizontal
        ('VALIGN', (1, 0), (1, 0), 'MIDDLE'),  # vertical

        ('BOTTOMPADDING', (2, 0), (2, 0), 40),
    ])

    return res
