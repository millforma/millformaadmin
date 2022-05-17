# Generated by Django 3.1.13 on 2022-05-11 14:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import main.models.file.base
import main.utils


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0005_auto_20220511_1511'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('date_last_update', models.DateTimeField(auto_now=True, verbose_name='Last changed')),
                ('date_v_start', models.DateTimeField(default=django.utils.timezone.now, verbose_name='V. start')),
                ('date_v_end', models.DateTimeField(blank=True, default=None, null=True, verbose_name='V. end')),
                ('name', models.IntegerField(blank=True, choices=[(1, 'Emargement'), (2, 'Contrat de partenariat formateur'), (3, 'Convocation'), (4, 'Qcm'), (5, 'Reglement interieur'), (6, 'Compte Rendu de formation'), (7, 'Ordre de mission'), (8, 'Attestation de fin de stage'), (10, 'Bon de commande'), (11, 'Kbis'), (12, 'Rib'), (13, 'Declaration Insee')], null=True)),
            ],
            options={
                'ordering': ['date_v_start'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VideoChat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('date_last_update', models.DateTimeField(auto_now=True, verbose_name='Last changed')),
                ('date_v_start', models.DateTimeField(default=django.utils.timezone.now, verbose_name='V. start')),
                ('date_v_end', models.DateTimeField(blank=True, default=None, null=True, verbose_name='V. end')),
                ('session', models.IntegerField(blank=True, default=1, null=True)),
                ('date_link_sent', models.DateField(auto_now_add=True)),
                ('link', models.URLField(error_messages={'invalid': 'A user with that display name already exists.'})),
                ('date_start', models.DateField(default=None)),
                ('time_start', models.TimeField(default=None)),
                ('date_end', models.DateField(default=None)),
                ('time_end', models.TimeField(default=None)),
                ('message', models.TextField(blank=True, default='', null=True)),
                ('title', models.CharField(blank=True, default='', max_length=200, null=True, unique=True)),
                ('finished_session', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('formation_session', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='main.formationsession')),
            ],
            options={
                'ordering': ['date_v_start'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(blank=True, default='', max_length=200, null=True, unique=True)),
                ('description', models.TextField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('formation_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.formationsession')),
                ('teacher', models.ForeignKey(blank=True, default=None, limit_choices_to={'groups__name': 'teacher'}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('trainee', models.ManyToManyField(related_name='trainee', to='main.Person')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to=settings.AUTH_USER_MODEL)),
                ('video_chat', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.videochat')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DocumentFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('date_last_update', models.DateTimeField(auto_now=True, verbose_name='Last changed')),
                ('date_v_start', models.DateTimeField(default=django.utils.timezone.now, verbose_name='V. start')),
                ('date_v_end', models.DateTimeField(blank=True, default=None, null=True, verbose_name='V. end')),
                ('informations', models.TextField(blank=True, default=None, null=True)),
                ('original_filename', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('actual_file', models.FileField(blank=True, default=None, null=True, upload_to=main.models.file.base.BaseFile.generate_filename)),
                ('creator', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.entity')),
                ('type', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.documenttype')),
            ],
            options={
                'abstract': False,
            },
            bases=(main.utils.UidMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PdfDocument',
            fields=[
                ('documentfile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.documentfile')),
                ('is_signed', models.BooleanField(default=False)),
                ('numb_of_signed_trainees', models.IntegerField(default=0)),
                ('verification_code', models.IntegerField(default=1658)),
                ('formation_session', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.formationsession')),
                ('type_of_document', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.documenttype')),
            ],
            options={
                'abstract': False,
            },
            bases=('main.documentfile',),
        ),
        migrations.CreateModel(
            name='EventMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='main.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_members', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('event', 'user')},
            },
        ),
    ]
