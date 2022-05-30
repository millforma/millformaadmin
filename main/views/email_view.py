from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from main.models.videochat import VideoChat
from main.decorators import auth_user_should_not_access
from main.utils import generate_token, EmailThread


def send_activation_email(user, request):
    current_site = request.get_host()
    email_subject = 'Activate your account'
    email_body = render_to_string('auth/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.DEFAULT_FROM_EMAIL,
                         to=[user.email]
                         )
    EmailThread(email).start()

def send_email_verification_code(subject, request,code):
    current_site = request.get_host()
    user=request.user
    email_subject = subject
    email_body = render_to_string('auth/signature_verification_code.html', {
        'user': user,
        'domain': current_site,
        'code': code,

    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.DEFAULT_FROM_EMAIL,
                         to=[settings.EMAIL_HOST_USER]
                         )
    EmailThread(email).start()

def send_videochatlink(videochat_instance_id, request):
    videochat_instance = VideoChat.objects.get(id=videochat_instance_id)
    current_site = request.get_host()
    teacher = videochat_instance.formation_session.teacher_name
    formation_session = videochat_instance.formation_session
    email_subject = 'Link for videochat'
    email_body = render_to_string('auth/videochat_link.html', {
        'teacher': teacher.last_name,
        'domain': current_site,
        'date_start_chat': formation_session,
        'link': videochat_instance.link,
    })
    emails =[]
    for trainee in formation_session.trainee.all():
        emails.append(trainee.user.email)
    #emails=trainees.values_list('user',flat=True)
    email = EmailMessage(subject=email_subject, body=email_body,
                        from_email=teacher.email,
                         to=emails
                         )
    EmailThread(email).start()

def send_attendance_inquiry(videochat_instance_id, request):
    videochat_instance = VideoChat.objects.get(id=videochat_instance_id)
    current_site = request.get_host()
    teacher = videochat_instance.formation_session.teacher_name
    formation_session = videochat_instance.formation_session
    email_subject = 'Please Sign your attendance'
    email_body = render_to_string('auth/attendance_inquiry.html', {
        'teacher': teacher.last_name,
        'domain': current_site,
        'date_start': videochat_instance.date_start,
        'formation':videochat_instance.formation_session,
        'link': videochat_instance.link,
    })
    emails =[]
    for trainee in formation_session.trainee.all():
        emails.append(trainee.user.email)
    #emails=trainees.values_list('user',flat=True)
    email = EmailMessage(subject=email_subject, body=email_body,
                        from_email=teacher.email,
                         to=emails
                         )
    EmailThread(email).start()


def send_formation_session_created_email(formation_session, instance):
    #    trainees = Person
    # for trainee in instance.trainee.all :

    #   email_subject = 'Your formation session is successfully created'
    #   email_body = render_to_string('email/formation_session_created.html', {
    #       'user': trainee,
    #   })

    #   email = EmailMessage(subject=email_subject, body=email_body,
    #                        from_email=settings.DEFAULT_FROM_EMAIL,
    #                        to=[trainee.email]
    #                        )
    #   EmailThread(email).start()
    # email_subject = 'Your formation session is successfully created'
    # email_body = render_to_string('email/formation_session_created.html', {
    #    'user': formation_session.teacher_name,
    # })

    # email = EmailMessage(subject=email_subject, body=email_body,
    #                     from_email=settings.DEFAULT_FROM_EMAIL,
    #                     to=[formation_session.teacher_name.email]
    #                     )
    # EmailThread(email).start()
    return None


@auth_user_should_not_access
def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))

        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.add_message(request, messages.SUCCESS,
                             'Email verified, you can now login')
        return redirect(reverse('login'))

    return render(request, 'auth/activate-failed.html', {"user": user})
