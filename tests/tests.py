# -*- coding: utf-8 -*-
# Author: Jakub Kubik
# Date: 11.03.2019

import pytest
# CLI
import sys  # 1
from shared.arguments import parse_arguments
from shared.arguments import adjust_from_to_currency  # 2
from shared.conversion import convert  # 3


# ===================================================
# CLI application testing
# ===================================================
class TestCliProgramArgumentsBadInput:
    """ #1 Check program arguments validity - bad input.
        ------------------------------------------------
        # 1.1 -> no parameters
        # 1.2 ->invalid parameter
        # 1.3 -> without amount parameter
        # 1.4 -> without input_currency parameter
        # 1.5 -> amount value 'str' type
    """
    def check_exit(self, argv):
        """ argv is used by argparse.ArgumentParser class inside parse_arguments function. """
        with pytest.raises(SystemExit) as e:
            parse_arguments()
            assert e.value.code == 2  # 2 is exit code for ArgumentsParser error

    def test_no_parameters(self):
        sys.argv = ['']
        self.check_exit(sys.argv)

    def test_invalid_parameter(self):
        sys.argv = ['', 'invalid_parameter']
        self.check_exit(sys.argv)

    def test_no_amount_parameter(self):
        sys.argv = ['', '--input_currency', 'USD', '--output_currency', 'EUR']
        self.check_exit(sys.argv)

    def test_no_input_currency_parameter(self):
        sys.argv = ['', '--amount', '42', '--output_currency', 'EUR']
        self.check_exit(sys.argv)

    def test_amount_parameter_is_string(self):
        sys.argv = ['', '--amount', 'two', '--input_currency', 'USD', '--output_currency', 'EUR']
        self.check_exit(sys.argv)


class TestCliConversionFromSymbolTo3LetterName:
    """ #2 Check conversion from symbol to 3 letter name.
        -------------------------------------------------
        2.1 -> input currency EUR and output currency $ -> Tuple[EUR, USD]
        2.2 -> input currency ₪ and output currency CZK -> Tuple[ILS, CZK]
        2.3 -> input currency ₩ and output currency ฿ -> Tuple[KRW, THB]
    """
    def test_name_and_symbol_to_names(self):
        input_currency, output_currency = adjust_from_to_currency('EUR', '$')
        assert (input_currency, output_currency) == ('EUR', 'USD')

    def test_symbol_and_name_to_names(self):
        input_currency, output_currency = adjust_from_to_currency('₪', 'CZK')
        assert (input_currency, output_currency) == ('ILS', 'CZK')

    def test_symbols_to_names(self):
        input_currency, output_currency = adjust_from_to_currency('₩', '฿')
        assert (input_currency, output_currency) == ('KRW', 'THB')


class TestCliCurrencyConversion:
    """ #3 Check currency conversion.
        -----------------------------
        # 3.1 -> output currency is string
        # 3.2 -> output currency is tuple
    """
    def test_convert_one_currency(self):
        currency = convert(100, 'EUR', 'CZK', {'CZK': 25, 'EUR': 1})
        assert currency['CZK'] == 2500

    def test_convert_multiple_currencies(self):
        currency = convert(100, 'EUR', ('CZK', 'USD', 'CAD'), {'CZK': 25, 'USD': 1.1, 'CAD': 1.5, 'EUR': 1})
        assert (currency['CZK'], currency['USD'], currency['CAD']) == (2500, 110, 150)


# =================================================
# web API application testing
# =================================================
class TestApiInvalidGetParametersAndPageRequest:
    """ #1 Check invalid pages requests and invalid GET request method parameters (response code 404).
        ----------------------------------------------------------------------------------------------
        # 1.1 -> GET page request - localhost:5000/
        # 1.2 -> GET page request - bad_page
        # 1.3 -> GET method param - no parameters
        # 1.4 -> GET method param - bad parameter
        # 1.5 -> GET method param - without amount parameter
        # 1.6 -> GET method param - without input_currency parameter
        # 1.7 -> GET method param - amount value 'string' type
    """
    def test_get_index_page(self, client):
        response = client.get('/')
        assert response.status_code == 404

    def test_get_bad_page(self, client):
        response = client.get('/')
        assert response.status_code == 404

    def test_get_no_parameters(self, client):
        resp = client.get('/currency_converter')
        assert resp.status_code == 404

    def test_get_bad_parameter(self, client):
        resp = client.get('/currency_converter/param')
        assert resp.status_code == 404

    def test_get_no_amount_parameter(self, client):
        resp = client.get('/currency_converter?&input_currency=¥')
        assert resp.status_code == 404

    def test_get_no_input_currency_parameter(self, client):
        resp = client.get('/currency_converter?&amount=42')
        assert resp.status_code == 404

    def test_get_amount_parameter_is_string(self, client):
        resp = client.get('/currency_converter?amount=dva&input_currency=¥')
        assert resp.status_code == 404


class TestApiValidGetParameters:
    """ #2 Check GET request method with valid parameters.
        --------------------------------------------------
        # 1.1 -> GET method param - all parameters
        # 1.2 -> GET method param - no output currency parameters
    """
    def test_get_all_parameters(self, client):
        resp = client.get('/currency_converter?amount=20&input_currency=¥&output_currency=CZK')
        assert resp.status_code == 200

    def test_get_no_output_currency_parameter(self, client):
        resp = client.get('/currency_converter?amount=99.44&input_currency=¥')
        assert resp.status_code == 200
