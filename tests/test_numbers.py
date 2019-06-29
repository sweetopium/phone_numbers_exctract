import numbers_worker as nw
import pytest

phone_number_pattern = r'\+?\d[\( -]?\d{3}[\) -]?\d{3}[ -]?\d{2}[ -]?\d{2}'

class TestNumbersWorker:
    def test_extract_numbers_from_broken_site(self):
        result = nw.extract_numbers_from_site('https://hhds.sk', phone_number_pattern)
        assert(result is False)

    def test_extract_numbers_from_working_site(self):
        result = nw.extract_numbers_from_site('https://repetitors.info', phone_number_pattern)
        assert(isinstance(result, list))

    def test_normalize_number(self):
        control = ['89253220000']
        numbers_list = ['89253220000', '8(925)3220000', '8(925)322-00-00', '+89253220000', '+8(925)3-2-2-0 0-00']
        normalized_numbers = nw.normalize_numbers(numbers_list)
        result = list(set(normalized_numbers))
        assert (control == result)

    def test_correct_validate_number(self):
        control = sorted(['89253230000', '84953230001'])
        numbers_list = ['911', '79253230000', '89253230000', '3230001', '123']
        validated_numbers = nw.validate_numbers(numbers_list)
        result = sorted(list(validated_numbers))
        assert (control == result)

    def test_validate_number_empty_list(self):
        numbers_list = []
        validated_numbers = nw.validate_numbers(numbers_list)
        assert (validated_numbers is False)
