from django.test import TestCase
from django.core.exceptions import ValidationError
from edc_constants.constants import YES, NO, OTHER, NEG
from ..form_validators import HIVInfantTestingFormValidator


class TestHIVInfantTestingFormValidator(TestCase):

    def setUp(self):
        self.clean_data = {
            'child_tested_for_hiv': YES,
            'child_test_date': '2023-01-01',
            'child_test_date_estimated': NO,
            'results_received': YES,
            'recall_result_date': YES,
            'received_date': '2023-01-03',
            'result_date_estimated': NO,
            'hiv_test_result': NEG,
            'reason_child_not_tested': None,
            'reason_child_not_tested_other': None,
            'preferred_clinic_for_testing': None,
            'additional_comments': None
        }

    def test_form_is_valid(self):
        form_validator = HIVInfantTestingFormValidator(
            cleaned_data=self.clean_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_child_not_tested_reason_required(self):
        self.clean_data.update(
            child_tested_for_hiv=NO,
            reason_child_not_tested=None)
        form_validator = HIVInfantTestingFormValidator(
            cleaned_data=self.clean_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('reason_child_not_tested', form_validator._errors)

    def test_child_tested_child_test_date_required(self):
        self.clean_data.update(
            child_tested_for_hiv=YES,
            child_test_date=None)
        form_validator = HIVInfantTestingFormValidator(
            cleaned_data=self.clean_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('child_test_date', form_validator._errors)

    def test_no_results_received_recall_result_date_not_required(self):
        self.clean_data.update(
            results_received=NO,
            recall_result_date=YES
        )
        form_validator = HIVInfantTestingFormValidator(
            cleaned_data=self.clean_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('recall_result_date', form_validator._errors)

    def test_clinic_preference_required_for_untested_child(self):
        self.clean_data.update(
            child_tested_for_hiv=NO,
            child_test_date=None,
            child_test_date_estimated=None,
            reason_child_not_tested="blah",
            preferred_clinic_for_testing=None,
        )
        form_validator = HIVInfantTestingFormValidator(
            cleaned_data=self.clean_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('preferred_clinic_for_testing', form_validator._errors)

    def test_reason_child_not_tested_other_required(self):
        self.clean_data.update(
            child_tested_for_hiv=NO,
            reason_child_not_tested=OTHER,
            child_test_date=None,
            child_test_date_estimated=None,
            reason_child_not_tested_other=None,
        )
        form_validator = HIVInfantTestingFormValidator(
            cleaned_data=self.clean_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('reason_child_not_tested_other', form_validator._errors)

    def test_no_testing_no_additional_comments_invalid(self):
        self.clean_data.update(
            child_tested_for_hiv=NO,
            preferred_clinic_for_testing='no_testing',
            additional_comments=None,
        )
        form_validator = HIVInfantTestingFormValidator(
            cleaned_data=self.clean_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('additional_comments', form_validator._errors)

