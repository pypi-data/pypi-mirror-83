# Generated by Django 3.0.9 on 2020-09-14 15:58
from django.core.exceptions import ObjectDoesNotExist
from django.db import migrations
from django.db.models.signals import pre_save
from edc_constants.constants import NO, NOT_APPLICABLE, YES
from edc_utils import DisableSignals
from inte_subject.diagnoses import ClinicalReviewBaselineRequired, Diagnoses


def update_medications(apps, schema_editor):
    medications_model_cls = apps.get_model("inte_subject.medications")
    refill_hiv_model_cls = apps.get_model("inte_subject.drugrefillhiv")
    refill_htn_model_cls = apps.get_model("inte_subject.drugrefillhtn")
    refill_dm_model_cls = apps.get_model("inte_subject.drugrefilldm")

    subject_visit_model_cls = apps.get_model("inte_subject.subjectvisit")
    for subject_visit in subject_visit_model_cls.objects.filter(
        visit_code_sequence__gt=0
    ).order_by("subject_identifier", "visit_code", "visit_code_sequence"):
        try:
            diagnoses = Diagnoses(subject_visit=subject_visit)
        except ClinicalReviewBaselineRequired:
            print(
                f"   * {subject_visit.subject_identifier}: ClinicalReviewBaselineRequired (skipping) [0060]"
            )
        else:
            medications = get_obj(medications_model_cls, subject_visit)
            opts = [
                ("hiv_dx", "refill_hiv", refill_hiv_model_cls),
                ("htn_dx", "refill_htn", refill_htn_model_cls),
                ("dm_dx", "refill_dm", refill_dm_model_cls),
            ]
            if medications:
                for dx_attr, refill_attr, refill_model_cls in opts:
                    if getattr(diagnoses, dx_attr):
                        obj = get_obj(refill_model_cls, subject_visit)
                        if obj:
                            setattr(medications, refill_attr, YES)
                        else:
                            setattr(medications, refill_attr, NO)
                    else:
                        setattr(medications, refill_attr, NOT_APPLICABLE)
                    with DisableSignals([pre_save]):
                        medications.save()
    print("\nDone. Remember to run the INTE managment command to update metadata.")


def get_obj(model_cls, subject_visit):
    obj = None
    try:
        obj = model_cls.objects.get(subject_visit=subject_visit)
    except ObjectDoesNotExist:
        pass
    return obj


class Migration(migrations.Migration):

    dependencies = [
        ("inte_subject", "0059_auto_20200913_2356"),
    ]

    operations = [migrations.RunPython(update_medications)]
