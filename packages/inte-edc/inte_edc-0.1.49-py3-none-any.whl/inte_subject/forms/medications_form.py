from django import forms
from django.conf import settings
from edc_constants.constants import NO, NOT_APPLICABLE, YES
from edc_form_validators.form_validator import FormValidator
from edc_utils import convert_php_dateformat
from inte_visit_schedule.is_baseline import is_baseline

from ..models import Medications, ClinicalReview, ClinicalReviewBaseline
from ..diagnoses import Diagnoses, InitialReviewRequired
from .mixins import CrfModelFormMixin, CrfFormValidatorMixin, model_exists_or_raise


class MedicationsFormValidator(CrfFormValidatorMixin, FormValidator):
    def clean(self):
        if not is_baseline(self.cleaned_data.get("subject_visit")):
            model_exists_or_raise(
                self.cleaned_data.get("subject_visit"), model_cls=ClinicalReview
            )
        else:
            model_exists_or_raise(
                self.cleaned_data.get("subject_visit"),
                model_cls=ClinicalReviewBaseline,
                singleton=True,
            )
        self.validate_diagnosis_before_refill()

    def validate_diagnosis_before_refill(self):
        """Assert subject has been diagnosed for the condition
        for which they require a medication refill,
        including for the current timepoint."""

        diagnoses = Diagnoses(
            subject_identifier=self.subject_identifier,
            report_datetime=self.report_datetime,
            lte=True,
        )

        try:
            diagnoses.initial_reviews
        except InitialReviewRequired as e:
            raise forms.ValidationError(e)

        options = [
            ("refill_htn", diagnoses.htn_dx, diagnoses.htn_dx_date, "hypertension"),
            ("refill_dm", diagnoses.dm_dx, diagnoses.dm_dx_date, "diabetes"),
            ("refill_hiv", diagnoses.hiv_dx, diagnoses.hiv_dx_date, "HIV"),
        ]
        for fld, dx, dx_date, label in options:
            if self.cleaned_data.get(fld) == NOT_APPLICABLE and dx:
                formatted_date = dx_date.strftime(
                    convert_php_dateformat(settings.DATE_FORMAT)
                )
                raise forms.ValidationError(
                    {
                        fld: (
                            f"Invalid. Subject was previously diagnosed with {label} "
                            f"on {formatted_date}. Expected YES/NO."
                        )
                    }
                )
            elif self.cleaned_data.get(fld) != NOT_APPLICABLE and not dx:
                raise forms.ValidationError(
                    {
                        fld: (
                            "Invalid. Subject has not been diagnosed with "
                            f"{label}. Expected N/A. See also the "
                            f"`{ClinicalReview._meta.verbose_name}` CRF."
                        )
                    }
                )


class MedicationsForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = MedicationsFormValidator

    class Meta:
        model = Medications
        fields = "__all__"
