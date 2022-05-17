from django.core.mail import EmailMessage
from django.template.loader import render_to_string

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

    email = EmailMessage(subject=email_subject, body=email_body,
                        from_email=settings.EMAIL_HOST_USER,
                         to=[teacher.email]
                         )
    EmailThread(email).start()


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
    email = EmailMessage(subject=email_subject, body=email_body,
                        from_email=settings.EMAIL_HOST_USER,
                         to=emails
                         )
    EmailThread(email).start()