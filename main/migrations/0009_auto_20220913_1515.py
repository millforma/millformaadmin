# Generated by Django 3.1.13 on 2022-09-13 13:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0008_pdfdocument_is_signed_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formationsession',
            name='client_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.company'),
        ),
        migrations.AlterField(
            model_name='formationsession',
            name='commercial',
            field=models.ForeignKey(blank=True, limit_choices_to={'groups__name': 'commercial'}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='commercial', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='formationsession',
            name='opco_name',
            field=models.IntegerField(choices=[(1, 'AKTO Réseau Fafih'), (2, 'AFDAS'), (3, 'AFDAS (Intermittent)'), (4, 'OPCO ATLAS'), (5, 'CAISSE DES DEPOTS ET CONSIGNATIONS'), (6, 'OPCALIA'), (7, 'AGEFICE'), (8, 'FP'), (9, 'AKTO Réseau Intergros'), (10, 'OPCOMMERCE'), (11, 'OPCO EP'), (12, 'OPCOmobilité'), (13, 'OCAPIAT'), (14, 'OPCO 2I')], default=1),
        ),
        migrations.AlterField(
            model_name='formationsession',
            name='teacher_name',
            field=models.ForeignKey(blank=True, limit_choices_to={'groups__name': 'teacher'}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='formationsession',
            name='trainee',
            field=models.ManyToManyField(blank=True, null=True, to='main.Person'),
        ),
        migrations.AlterField(
            model_name='formationsession',
            name='training_site',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.address'),
        ),
    ]
