# Generated by Django 3.0.9 on 2020-10-02 17:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inte_subject", "0069_auto_20201002_2042"),
    ]

    operations = [
        migrations.AddField(
            model_name="clinicalreview",
            name="health_insurance_monthly_pay",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="In the last month, how much has the patient spent on health insurance",
            ),
        ),
        migrations.AddField(
            model_name="clinicalreview",
            name="patient_club_monthly_pay",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="In the last month, how much has the patient spent on club membership",
            ),
        ),
        migrations.AddField(
            model_name="clinicalreviewbaseline",
            name="health_insurance_monthly_pay",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="In the last month, how much has the patient spent on health insurance",
            ),
        ),
        migrations.AddField(
            model_name="clinicalreviewbaseline",
            name="patient_club_monthly_pay",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="In the last month, how much has the patient spent on club membership",
            ),
        ),
        migrations.AddField(
            model_name="historicalclinicalreview",
            name="health_insurance_monthly_pay",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="In the last month, how much has the patient spent on health insurance",
            ),
        ),
        migrations.AddField(
            model_name="historicalclinicalreview",
            name="patient_club_monthly_pay",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="In the last month, how much has the patient spent on club membership",
            ),
        ),
        migrations.AddField(
            model_name="historicalclinicalreviewbaseline",
            name="health_insurance_monthly_pay",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="In the last month, how much has the patient spent on health insurance",
            ),
        ),
        migrations.AddField(
            model_name="historicalclinicalreviewbaseline",
            name="patient_club_monthly_pay",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="In the last month, how much has the patient spent on club membership",
            ),
        ),
    ]
