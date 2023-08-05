# Generated by Django 3.0.9 on 2020-10-06 17:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inte_lists", "0008_auto_20201002_0403"),
        ("inte_subject", "0070_auto_20201002_2055"),
    ]

    operations = [
        migrations.AlterField(
            model_name="clinicalreview",
            name="health_insurance_monthly_pay",
            field=models.IntegerField(
                blank=True,
                help_text="amount in local currency",
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="In the last month, how much has the patient spent on health insurance",
            ),
        ),
        migrations.AlterField(
            model_name="clinicalreview",
            name="patient_club_monthly_pay",
            field=models.IntegerField(
                blank=True,
                help_text="amount in local currency",
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="In the last month, how much has the patient spent on club membership",
            ),
        ),
        migrations.AlterField(
            model_name="clinicalreviewbaseline",
            name="health_insurance_monthly_pay",
            field=models.IntegerField(
                blank=True,
                help_text="amount in local currency",
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="In the last month, how much has the patient spent on health insurance",
            ),
        ),
        migrations.AlterField(
            model_name="clinicalreviewbaseline",
            name="patient_club_monthly_pay",
            field=models.IntegerField(
                blank=True,
                help_text="amount in local currency",
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="In the last month, how much has the patient spent on club membership",
            ),
        ),
        migrations.AlterField(
            model_name="historicalclinicalreview",
            name="health_insurance_monthly_pay",
            field=models.IntegerField(
                blank=True,
                help_text="amount in local currency",
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="In the last month, how much has the patient spent on health insurance",
            ),
        ),
        migrations.AlterField(
            model_name="historicalclinicalreview",
            name="patient_club_monthly_pay",
            field=models.IntegerField(
                blank=True,
                help_text="amount in local currency",
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="In the last month, how much has the patient spent on club membership",
            ),
        ),
        migrations.AlterField(
            model_name="historicalclinicalreviewbaseline",
            name="health_insurance_monthly_pay",
            field=models.IntegerField(
                blank=True,
                help_text="amount in local currency",
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="In the last month, how much has the patient spent on health insurance",
            ),
        ),
        migrations.AlterField(
            model_name="historicalclinicalreviewbaseline",
            name="patient_club_monthly_pay",
            field=models.IntegerField(
                blank=True,
                help_text="amount in local currency",
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="In the last month, how much has the patient spent on club membership",
            ),
        ),
    ]
