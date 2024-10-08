# Generated by Django 5.0.7 on 2024-09-15 18:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('patients', '0001_initial'),
        ('procedures', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='ClinicProcedure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinics.clinic')),
                ('procedure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='procedures.procedure')),
            ],
            options={
                'unique_together': {('clinic', 'procedure')},
            },
        ),
        migrations.CreateModel(
            name='PatientClinicAffiliation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinics.clinic')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.patient')),
            ],
            options={
                'unique_together': {('patient', 'clinic')},
            },
        ),
    ]
