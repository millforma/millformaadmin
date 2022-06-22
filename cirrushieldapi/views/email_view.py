from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.mail import send_mail
from electronicSignature import settings
from main.models.videochat import VideoChat
from main.utils import EmailThread


def send_emargementteacherlink(link, formation, request):

    current_site = request.get_host()
    teacher = formation.teacher_name

    email_subject = 'Lien pour émargements'
    email_body = render_to_string('email/send_emargement.html', {
        'teacher': teacher,
        'domain': current_site,
        'formation': formation,
        'link': link,
    })
    send_mail(
        email_subject,
        email_body,
        settings.EMAIL_SENDER,
        [teacher.email]
    )

def send_email_verification_code(code, request):


    user=request.user
    email_subject = 'Code de vérification pour signature'
    email_body = render_to_string('email/send_verif_code.html', {

        'code': code,
    })
    send_mail(
        email_subject,
        email_body,
        settings.EMAIL_SENDER,
        [user.email]
    )



def send_id(link,formation, request):

    current_site = request.get_host()


    email_subject = 'Vos Informations de connexion'
    email_body = render_to_string('email/send_id.html', {

        'domain': current_site,
        'link': link,
    })
    emails = []
    for trainee in formation.trainee.all():
        emails.append(trainee.user.email)
    emails.append(formation.teacher_name.email)
    send_mail(
        email_subject,
        email_body,
        settings.EMAIL_SENDER,
        emails
    )

def send_emargementlearnerlink(link, formation, request):

    current_site = request.get_host()
    teacher = formation.teacher_name

    email_subject = 'Lien pour émargements'
    email_body = render_to_string('email/send_emargement_trainee.html', {
        'teacher': teacher,
        'domain': current_site,
        'formation': formation,
        'link': link,
    })
    emails = []
    for trainee in formation.trainee.all():
        emails.append(trainee.user.email)
    send_mail(
        email_subject,
        email_body,
        settings.EMAIL_SENDER,
        emails
    )

