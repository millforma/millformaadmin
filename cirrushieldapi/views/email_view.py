from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.core.mail import send_mail
from electronicSignature import settings
from main.models.formationsession import FormationSession
from django.contrib import messages
from django.contrib.sites.models import Site


# function which is called on button télécharger on home view
def send_convention(request, formation_id):
    session = FormationSession.objects.get(id=formation_id)
    current_site = Site.objects.get_current()
    # links for email purpose
    link = current_site.domain + '/learner/' + str(session.id)
    teacher = session.teacher_name

    email_subject = 'Signature convention de formation'
    email_body = render_to_string('email/send_convention.html', {
        'teacher': teacher,
        'domain': current_site,
        'formation': session,
        'link': link,
    })
    send_mail(
        email_subject,
        email_body,
        settings.EMAIL_SENDER,
        [teacher.email]
    )

    # success
    messages.success(request, "La convention de formation a bien été envoyée")

    return redirect('main:home')


def send_emargement_trainees(request, formation_id, date):
    final_session = FormationSession.objects.get(id=formation_id)
    current_site = Site.objects.get_current()
    link_learner = current_site.domain + '/learner/' + str(final_session.id)
    send_emargementlearnerlink(link_learner, final_session, current_site, date)




# function which is called on button télécharger on home view
def send_links_for_formation(request, formation_id):
    final_session = FormationSession.objects.get(id=formation_id)
    current_site = Site.objects.get_current()

    # links for email purpose
    link_teacher = current_site.domain + '/teacher/' + str(final_session.id)
    link_reset_passwd = current_site.domain + '/password-reset/'

    send_id(link_reset_passwd, final_session, current_site)

    send_emargementteacherlink(link_teacher, final_session, current_site)
    # success
    messages.success(request, "La lien a bien été envoyé")

    return redirect('main:home')


# send emargement link for teacher
def send_emargementteacherlink(link, formation, current_site):
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



# send emargement link for all trainees of the Formationsession
def send_emargementlearnerlink(link, formation, current_site, date):
    teacher = formation.teacher_name

    email_subject = 'Lien pour signer vos émargements'
    email_body = render_to_string('email/send_emargement_trainee.html', {
        'teacher': teacher,
        'domain': current_site,
        'formation': formation,
        'date': date,
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


# send verification code for pdf signature
def send_email_verification_code(request, code):
    user = request.request.user
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


# sent for 1st connexion puprose
def send_id(link, formation, current_site):
    email_subject = 'Bienvenue sur Mill Forma'

    emails = []
    for trainee in formation.trainee.all():
        email_body = render_to_string('email/send_id.html', {
            'domain': current_site,
            'link': link,
            'username': trainee.user.username,
            'email': trainee.user.email,
        })
        send_mail(
            email_subject,
            email_body,
            settings.EMAIL_SENDER,
            [trainee.user.email]
        )

    email_body = render_to_string('email/send_id.html', {
        'domain': current_site,
        'link': link,
        'username': formation.teacher_name.username,
        'email': formation.teacher_name.email,
    })
    send_mail(
        email_subject,
        email_body,
        settings.EMAIL_SENDER,
        [formation.teacher_name.email],
    )


def resend_username(user):
    email_subject = 'Votre username de connexion Mill Forma'
    email_body = render_to_string('email/resend_username.html', {
        'username': user.username,
    })

    send_mail(
        email_subject,
        email_body,
        settings.EMAIL_SENDER,
        user.email,
    )
