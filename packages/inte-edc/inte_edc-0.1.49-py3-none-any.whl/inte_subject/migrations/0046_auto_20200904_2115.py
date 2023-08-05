# Generated by Django 3.0.9 on 2020-09-04 18:15

from django.db import migrations, models
import edc_model.models.validators.date


class Migration(migrations.Migration):

    dependencies = [
        ("inte_lists", "0006_auto_20200812_0317"),
        ("inte_subject", "0045_auto_20200904_0446"),
    ]

    operations = [
        migrations.AddField(
            model_name="diabetesinitialreview",
            name="dx_date_estimated",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                editable=False,
                max_length=15,
                verbose_name="Was the diagnosis date estimated?",
            ),
        ),
        migrations.AddField(
            model_name="diabetesinitialreview",
            name="med_start_date_estimated",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                editable=False,
                max_length=15,
                verbose_name="Was the medication start date estimated?",
            ),
        ),
        migrations.AddField(
            model_name="historicaldiabetesinitialreview",
            name="dx_date_estimated",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                editable=False,
                max_length=15,
                verbose_name="Was the diagnosis date estimated?",
            ),
        ),
        migrations.AddField(
            model_name="historicaldiabetesinitialreview",
            name="med_start_date_estimated",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                editable=False,
                max_length=15,
                verbose_name="Was the medication start date estimated?",
            ),
        ),
        migrations.AddField(
            model_name="historicalhivinitialreview",
            name="arv_initiation_date_estimated",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                editable=False,
                max_length=15,
                verbose_name="Was the date patient started ART estimated?",
            ),
        ),
        migrations.AddField(
            model_name="historicalhivinitialreview",
            name="dx_date_estimated",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                editable=False,
                max_length=15,
                verbose_name="Was the diagnosis date estimated?",
            ),
        ),
        migrations.AddField(
            model_name="historicalhypertensioninitialreview",
            name="dx_date_estimated",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                editable=False,
                max_length=15,
                verbose_name="Was the diagnosis date estimated?",
            ),
        ),
        migrations.AddField(
            model_name="historicalhypertensioninitialreview",
            name="med_start_date_estimated",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                editable=False,
                max_length=15,
                verbose_name="Was the medication start date estimated?",
            ),
        ),
        migrations.AddField(
            model_name="hivinitialreview",
            name="arv_initiation_date_estimated",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                editable=False,
                max_length=15,
                verbose_name="Was the date patient started ART estimated?",
            ),
        ),
        migrations.AddField(
            model_name="hivinitialreview",
            name="dx_date_estimated",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                editable=False,
                max_length=15,
                verbose_name="Was the diagnosis date estimated?",
            ),
        ),
        migrations.AddField(
            model_name="hypertensioninitialreview",
            name="dx_date_estimated",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                editable=False,
                max_length=15,
                verbose_name="Was the diagnosis date estimated?",
            ),
        ),
        migrations.AddField(
            model_name="hypertensioninitialreview",
            name="med_start_date_estimated",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                editable=False,
                max_length=15,
                verbose_name="Was the medication start date estimated?",
            ),
        ),
        migrations.AlterField(
            model_name="clinicalreviewbaseline",
            name="diabetes_tested_date",
            field=models.DateField(
                blank=True,
                null=True,
                validators=[edc_model.models.validators.date.date_not_future],
                verbose_name="Date of patient's most recent Diabetes test?",
            ),
        ),
        migrations.AlterField(
            model_name="clinicalreviewbaseline",
            name="hypertension_tested_date",
            field=models.DateField(
                blank=True,
                null=True,
                validators=[edc_model.models.validators.date.date_not_future],
                verbose_name="Date of patient's most recent Hypertension test?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalclinicalreviewbaseline",
            name="diabetes_tested_date",
            field=models.DateField(
                blank=True,
                null=True,
                validators=[edc_model.models.validators.date.date_not_future],
                verbose_name="Date of patient's most recent Diabetes test?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalclinicalreviewbaseline",
            name="hypertension_tested_date",
            field=models.DateField(
                blank=True,
                null=True,
                validators=[edc_model.models.validators.date.date_not_future],
                verbose_name="Date of patient's most recent Hypertension test?",
            ),
        ),
    ]
