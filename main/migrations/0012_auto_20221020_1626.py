# Generated by Django 3.1.13 on 2022-10-20 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_formationsession_objectifs_peda'),
    ]

    operations = [
        migrations.CreateModel(
            name='Objectifs_peda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='formationsession',
            name='objectifs_peda',
        ),
        migrations.AddField(
            model_name='formationsession',
            name='objectifs_peda',
            field=models.ManyToManyField(blank=True, null=True, to='main.Objectifs_peda'),
        ),
    ]