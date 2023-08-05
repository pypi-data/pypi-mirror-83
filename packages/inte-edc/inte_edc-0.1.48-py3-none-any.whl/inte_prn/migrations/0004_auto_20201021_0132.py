# Generated by Django 3.0.9 on 2020-10-20 22:32

import django.core.validators
from django.db import migrations, models
import edc_identifier.managers
import edc_model.models.fields.other_charfield
import edc_model.models.validators.date
import edc_protocol.validators
import edc_sites.models
import edc_utils.date


class Migration(migrations.Migration):

    dependencies = [
        ("inte_prn", "0003_auto_20200818_2043"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="endofstudy",
            managers=[
                ("on_site", edc_sites.models.CurrentSiteManager()),
                ("objects", edc_identifier.managers.SubjectIdentifierManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name="losstofollowup",
            managers=[("on_site", edc_sites.models.CurrentSiteManager()),],
        ),
        migrations.AddField(
            model_name="endofstudy",
            name="ltfu_date",
            field=models.DateField(
                blank=True,
                null=True,
                validators=[edc_model.models.validators.date.date_not_future],
                verbose_name="Date lost to followup, if applicable",
            ),
        ),
        migrations.AddField(
            model_name="historicalendofstudy",
            name="ltfu_date",
            field=models.DateField(
                blank=True,
                null=True,
                validators=[edc_model.models.validators.date.date_not_future],
                verbose_name="Date lost to followup, if applicable",
            ),
        ),
        migrations.AddField(
            model_name="historicallosstofollowup",
            name="last_missed_visit_datetime",
            field=models.DateField(
                null=True, verbose_name="Date of last missed visit report submitted"
            ),
        ),
        migrations.AddField(
            model_name="historicallosstofollowup",
            name="loss_category_other",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AddField(
            model_name="historicallosstofollowup",
            name="number_consecutive_missed_visits",
            field=models.IntegerField(
                null=True, verbose_name="Number of consecutive visits missed"
            ),
        ),
        migrations.AddField(
            model_name="historicallosstofollowup",
            name="phone",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                null=True,
                verbose_name="Was contact by phone attempted",
            ),
        ),
        migrations.AddField(
            model_name="losstofollowup",
            name="last_missed_visit_datetime",
            field=models.DateField(
                null=True, verbose_name="Date of last missed visit report submitted"
            ),
        ),
        migrations.AddField(
            model_name="losstofollowup",
            name="loss_category_other",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AddField(
            model_name="losstofollowup",
            name="number_consecutive_missed_visits",
            field=models.IntegerField(
                null=True, verbose_name="Number of consecutive visits missed"
            ),
        ),
        migrations.AddField(
            model_name="losstofollowup",
            name="phone",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                null=True,
                verbose_name="Was contact by phone attempted",
            ),
        ),
        migrations.AlterField(
            model_name="historicallosstofollowup",
            name="comment",
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name="If any, please give additional details of the circumstances that led to this decision.",
            ),
        ),
        migrations.AlterField(
            model_name="historicallosstofollowup",
            name="home_visit_detail",
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name="If YES, provide any further details of the home visit",
            ),
        ),
        migrations.AlterField(
            model_name="historicallosstofollowup",
            name="home_visited",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Was a home visit attempted",
            ),
        ),
        migrations.AlterField(
            model_name="historicallosstofollowup",
            name="last_seen_datetime",
            field=models.DateField(
                validators=[edc_protocol.validators.date_not_before_study_start],
                verbose_name="Date participant last seen",
            ),
        ),
        migrations.AlterField(
            model_name="historicallosstofollowup",
            name="loss_category",
            field=models.CharField(
                choices=[
                    ("unknown_address", "Changed to an unknown address"),
                    ("never_returned", "Did not return despite reminders"),
                    ("bad_contact_details", "Inaccurate contact details"),
                    ("OTHER", "Other"),
                ],
                max_length=25,
                verbose_name="Category of loss to follow up",
            ),
        ),
        migrations.AlterField(
            model_name="historicallosstofollowup",
            name="phone_attempts",
            field=models.IntegerField(
                default=0,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name=(
                    "If YES, how many attempts were made to contact the participant by phone",
                ),
            ),
        ),
        migrations.AlterField(
            model_name="historicallosstofollowup",
            name="report_datetime",
            field=models.DateTimeField(
                default=edc_utils.date.get_utcnow,
                validators=[edc_protocol.validators.date_not_before_study_start],
                verbose_name="Report Date and Time",
            ),
        ),
        migrations.AlterField(
            model_name="losstofollowup",
            name="comment",
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name="If any, please give additional details of the circumstances that led to this decision.",
            ),
        ),
        migrations.AlterField(
            model_name="losstofollowup",
            name="home_visit_detail",
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name="If YES, provide any further details of the home visit",
            ),
        ),
        migrations.AlterField(
            model_name="losstofollowup",
            name="home_visited",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Was a home visit attempted",
            ),
        ),
        migrations.AlterField(
            model_name="losstofollowup",
            name="last_seen_datetime",
            field=models.DateField(
                validators=[edc_protocol.validators.date_not_before_study_start],
                verbose_name="Date participant last seen",
            ),
        ),
        migrations.AlterField(
            model_name="losstofollowup",
            name="loss_category",
            field=models.CharField(
                choices=[
                    ("unknown_address", "Changed to an unknown address"),
                    ("never_returned", "Did not return despite reminders"),
                    ("bad_contact_details", "Inaccurate contact details"),
                    ("OTHER", "Other"),
                ],
                max_length=25,
                verbose_name="Category of loss to follow up",
            ),
        ),
        migrations.AlterField(
            model_name="losstofollowup",
            name="phone_attempts",
            field=models.IntegerField(
                default=0,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name=(
                    "If YES, how many attempts were made to contact the participant by phone",
                ),
            ),
        ),
        migrations.AlterField(
            model_name="losstofollowup",
            name="report_datetime",
            field=models.DateTimeField(
                default=edc_utils.date.get_utcnow,
                validators=[edc_protocol.validators.date_not_before_study_start],
                verbose_name="Report Date and Time",
            ),
        ),
    ]
