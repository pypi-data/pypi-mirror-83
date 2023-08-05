# Generated by Django 3.0.9 on 2020-08-20 17:08

from django.db import migrations, models
import edc_model.models.fields.other_charfield


class Migration(migrations.Migration):

    dependencies = [
        ("inte_lists", "0006_auto_20200812_0317"),
        ("inte_subject", "0032_auto_20200818_2017"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="carestatusbaseline",
            options={
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Clinical Review: Baseline",
                "verbose_name_plural": "Clinical Review: Baseline",
            },
        ),
        migrations.AlterModelOptions(
            name="historicalcarestatusbaseline",
            options={
                "get_latest_by": "history_date",
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Clinical Review: Baseline",
            },
        ),
        migrations.AddField(
            model_name="carestatusbaseline",
            name="diabetes_tested_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="carestatusbaseline",
            name="hiv_result_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="carestatusbaseline",
            name="hypertensive_tested_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="historicalcarestatusbaseline",
            name="diabetes_tested_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="historicalcarestatusbaseline",
            name="hiv_result_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="historicalcarestatusbaseline",
            name="hypertensive_tested_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="historicalinvestigations",
            name="diabetes_dx",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=15,
                verbose_name="As of today, was the patient <u>newly</u> diagnosed with diabetes?",
            ),
        ),
        migrations.AddField(
            model_name="historicalinvestigations",
            name="diabetes_reason_other",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AddField(
            model_name="historicalinvestigations",
            name="hiv_dx",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=15,
                verbose_name="As of today, was the patient <u>newly</u> diagnosed with HIV infection?",
            ),
        ),
        migrations.AddField(
            model_name="historicalinvestigations",
            name="hiv_reason_other",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AddField(
            model_name="historicalinvestigations",
            name="hypertension_dx",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=15,
                verbose_name="As of today, was the patient <u>newly</u> diagnosed with hypertension?",
            ),
        ),
        migrations.AddField(
            model_name="historicalinvestigations",
            name="hypertension_reason_other",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AddField(
            model_name="historicalsubjectvisit",
            name="clinic_services_other",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AddField(
            model_name="investigations",
            name="diabetes_dx",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=15,
                verbose_name="As of today, was the patient <u>newly</u> diagnosed with diabetes?",
            ),
        ),
        migrations.AddField(
            model_name="investigations",
            name="diabetes_reason",
            field=models.ManyToManyField(
                blank=True,
                related_name="diabetes_tested_reason",
                to="inte_lists.ReasonsForTesting",
                verbose_name="Why was the patient tested for diabetes?",
            ),
        ),
        migrations.AddField(
            model_name="investigations",
            name="diabetes_reason_other",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AddField(
            model_name="investigations",
            name="hiv_dx",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=15,
                verbose_name="As of today, was the patient <u>newly</u> diagnosed with HIV infection?",
            ),
        ),
        migrations.AddField(
            model_name="investigations",
            name="hiv_reason",
            field=models.ManyToManyField(
                blank=True,
                related_name="hiv_tested_reason",
                to="inte_lists.ReasonsForTesting",
                verbose_name="Why was the patient tested for HIV infection?",
            ),
        ),
        migrations.AddField(
            model_name="investigations",
            name="hiv_reason_other",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AddField(
            model_name="investigations",
            name="hypertension_dx",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=15,
                verbose_name="As of today, was the patient <u>newly</u> diagnosed with hypertension?",
            ),
        ),
        migrations.AddField(
            model_name="investigations",
            name="hypertension_reason",
            field=models.ManyToManyField(
                blank=True,
                related_name="hypertension_tested_reason",
                to="inte_lists.ReasonsForTesting",
                verbose_name="Why was the patient tested for hypertension?",
            ),
        ),
        migrations.AddField(
            model_name="investigations",
            name="hypertension_reason_other",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AddField(
            model_name="subjectvisit",
            name="clinic_services",
            field=models.ManyToManyField(
                related_name="visit_clinic_services",
                to="inte_lists.ClinicServices",
                verbose_name="Why is the patient at the clinic today?",
            ),
        ),
        migrations.AddField(
            model_name="subjectvisit",
            name="clinic_services_other",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AddField(
            model_name="subjectvisit",
            name="health_services",
            field=models.ManyToManyField(
                related_name="visit_health_services",
                to="inte_lists.HealthServices",
                verbose_name="Which health service(s) is the patient here for today?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalinvestigations",
            name="diabetes_tested",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="Include today if tested today. Select `not applicable` if previously diagnosed.",
                max_length=15,
                verbose_name="Since last seen, was the patient tested for diabetes?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalinvestigations",
            name="hiv_tested",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="Include today if tested today. Select `not applicable` if previously diagnosed.",
                max_length=15,
                verbose_name="Since last seen, was the patient tested for HIV infection?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalinvestigations",
            name="hypertension_tested",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="Include today if tested today. Select `not applicable` if previously diagnosed.",
                max_length=15,
                verbose_name="Since last seen, was the patient tested for hypertension?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalinvestigations",
            name="test_date",
            field=models.DateField(
                blank=True,
                editable=False,
                help_text="question_retired",
                null=True,
                verbose_name="Date test requested",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectvisit",
            name="reason",
            field=models.CharField(
                choices=[
                    ("scheduled", "Scheduled visit (study)"),
                    ("unscheduled", "Routine / Unschedule visit (non-study)"),
                    ("missed", "Missed visit"),
                ],
                help_text="Only baseline (0m), 6m and 12m are considered `scheduled` visits as per the INTE protocol.",
                max_length=25,
                verbose_name="What is the reason for this visit report?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectvisit",
            name="reason_unscheduled",
            field=models.CharField(
                choices=[
                    ("routine_non_study", "Routine appointment (non-study)"),
                    ("patient_unwell_outpatient", "Patient unwell"),
                    ("drug_refill", "Drug refill only"),
                    ("OTHER", "Other"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="If 'unscheduled', provide reason for the unscheduled visit",
            ),
        ),
        migrations.AlterField(
            model_name="investigations",
            name="diabetes_tested",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="Include today if tested today. Select `not applicable` if previously diagnosed.",
                max_length=15,
                verbose_name="Since last seen, was the patient tested for diabetes?",
            ),
        ),
        migrations.AlterField(
            model_name="investigations",
            name="hiv_tested",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="Include today if tested today. Select `not applicable` if previously diagnosed.",
                max_length=15,
                verbose_name="Since last seen, was the patient tested for HIV infection?",
            ),
        ),
        migrations.AlterField(
            model_name="investigations",
            name="hypertension_tested",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="Include today if tested today. Select `not applicable` if previously diagnosed.",
                max_length=15,
                verbose_name="Since last seen, was the patient tested for hypertension?",
            ),
        ),
        migrations.AlterField(
            model_name="investigations",
            name="reason",
            field=models.ManyToManyField(
                blank=True,
                editable=False,
                help_text="question_retired",
                to="inte_lists.ReasonsForTesting",
                verbose_name="Why was the patient tested?",
            ),
        ),
        migrations.AlterField(
            model_name="investigations",
            name="test_date",
            field=models.DateField(
                blank=True,
                editable=False,
                help_text="question_retired",
                null=True,
                verbose_name="Date test requested",
            ),
        ),
        migrations.AlterField(
            model_name="reasonforvisit",
            name="health_services",
            field=models.ManyToManyField(
                related_name="health_services",
                to="inte_lists.HealthServices",
                verbose_name="Which health service(s) is the patient here for today?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectvisit",
            name="reason",
            field=models.CharField(
                choices=[
                    ("scheduled", "Scheduled visit (study)"),
                    ("unscheduled", "Routine / Unschedule visit (non-study)"),
                    ("missed", "Missed visit"),
                ],
                help_text="Only baseline (0m), 6m and 12m are considered `scheduled` visits as per the INTE protocol.",
                max_length=25,
                verbose_name="What is the reason for this visit report?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectvisit",
            name="reason_unscheduled",
            field=models.CharField(
                choices=[
                    ("routine_non_study", "Routine appointment (non-study)"),
                    ("patient_unwell_outpatient", "Patient unwell"),
                    ("drug_refill", "Drug refill only"),
                    ("OTHER", "Other"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="If 'unscheduled', provide reason for the unscheduled visit",
            ),
        ),
    ]
