# Generated by Django 5.0.7 on 2024-09-15 18:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clinics', '0001_initial'),
        ('patients', '0001_initial'),
        ('procedures', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('npi', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='DoctorClinicAffiliation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('office_address', models.TextField()),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinics.clinic')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctors.doctor')),
            ],
            options={
                'unique_together': {('doctor', 'clinic')},
            },
        ),
        migrations.CreateModel(
            name='DoctorProcedure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctors.doctor')),
                ('procedure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='procedures.procedure')),
            ],
            options={
                'unique_together': {('doctor', 'procedure')},
            },
        ),
        migrations.CreateModel(
            name='PatientDoctorAffiliation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctors.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.patient')),
            ],
            options={
                'unique_together': {('patient', 'doctor')},
            },
        ),
    ]
