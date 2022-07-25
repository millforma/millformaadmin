"""electronicSignature URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.views.static import serve

from electronicSignature import settings
from electronicSignature.MySetPasswordForm import MySetPasswordForm
from main.views.login_view import CustomLoginView

app_name = 'electronicsignature'

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('signature.urls', namespace='signature')),
    path("", include('cirrushieldapi.urls', namespace='cirrushieldapi')),
    path("", include('main.urls', namespace='main')),
    re_path(
        r"^public/(?P<path>.*)$",
        serve,
        {"document_root": settings.MEDIA_ROOT},
        name="url_public",
    ),
    path(
        "login/",
        CustomLoginView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="login"),
        name="logout",
    ),
path(
        "change-password/",
        auth_views.PasswordChangeView.as_view(
            template_name="auth/change-password.html", success_url="/"
        ),
        name="change-password",
    ),
    # Forget Password
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(

        ),
        name="password_change",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            form_class=MySetPasswordForm
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
        ),
        name="password_reset_complete",
    ),

]
handler404 = "main.views.page_not_found_view"